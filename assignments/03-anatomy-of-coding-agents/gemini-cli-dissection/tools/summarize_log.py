"""Summarize a Gemini CLI local telemetry log.

Gemini CLI's local file exporter appends pretty-printed JSON objects (log records,
spans, metrics) one after another. This script pulls out the events that matter for
the lab and prints them in order, without emails or other account identifiers.

Usage:
    python summarize_log.py path/to/telemetry.log              # timeline + summary
    python summarize_log.py path/to/telemetry.log --out timeline.txt  # same, to a file
    python summarize_log.py path/to/telemetry.log --csv out.csv  # per-API-call token table
    python summarize_log.py path/to/telemetry.log --system out.md  # system instructions sent
    python summarize_log.py path/to/telemetry.log --context out.md  # first message the model got
    python summarize_log.py path/to/telemetry.log --tools out.md    # tool schemas the model got
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter

EVENTS = {
    "gemini_cli.user_prompt": "user_prompt",
    "gemini_cli.api_request": "api_request",
    "gemini_cli.api_response": "api_response",
    "gemini_cli.api_error": "api_error",
    "gemini_cli.tool_call": "tool_call",
}

TOKEN_KEYS = [
    "input_token_count",
    "output_token_count",
    "cached_content_token_count",
    "thoughts_token_count",
    "tool_token_count",
    "total_token_count",
]


def read_objects(path: str):
    """Yield every top-level JSON object in a file of concatenated JSON."""
    text = open(path, encoding="utf-8", errors="replace").read()
    decoder = json.JSONDecoder()
    i, n = 0, len(text)
    while i < n:
        while i < n and text[i] not in "{[":
            i += 1
        if i >= n:
            break
        try:
            obj, end = decoder.raw_decode(text, i)
        except json.JSONDecodeError:
            i += 1  # skip a truncated/corrupt fragment
            continue
        yield obj
        i = end


def find_attribute_dicts(obj):
    """Yield every dict nested in obj that has an 'event.name' key."""
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            if "event.name" in cur:
                yield cur
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)


def find_key(obj, key):
    """Yield every value stored under `key` anywhere inside obj."""
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            if key in cur:
                yield cur[key]
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)


def as_text(value) -> str:
    """Turn a payload attribute (often JSON-encoded, sometimes twice) into plain text."""
    for _ in range(3):
        if isinstance(value, str) and value[:1] in '[{"':
            try:
                value = json.loads(value)
                continue
            except json.JSONDecodeError:
                pass
        break
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        if "parts" in value:
            return as_text(value["parts"])
        return as_text(value.get("content", value.get("text", "")))
    if isinstance(value, list):
        return "".join(as_text(v) for v in value)
    return str(value)


def tool_declarations(path: str) -> list[dict]:
    """Every tool declaration (name, description, schema) sent to the model, first seen wins."""
    tools: dict[str, dict] = {}
    for obj in read_objects(path):
        for raw in find_key(obj, "gen_ai.tool.definitions"):
            try:
                groups = json.loads(raw) if isinstance(raw, str) else raw
            except json.JSONDecodeError:
                continue
            for group in groups if isinstance(groups, list) else [groups]:
                for decl in (group or {}).get("functionDeclarations", []):
                    tools.setdefault(decl.get("name"), decl)
    return sorted(tools.values(), key=lambda d: d.get("name") or "")


def first_user_message(path: str) -> str | None:
    """Text of the first user-role message sent to the model (needs telemetry traces)."""
    for obj in read_objects(path):
        for raw in find_key(obj, "gen_ai.input.messages"):
            try:
                messages = json.loads(raw) if isinstance(raw, str) else raw
            except json.JSONDecodeError:
                continue
            for m in messages if isinstance(messages, list) else []:
                if isinstance(m, dict) and m.get("role") == "user":
                    return as_text(m)
    return None


def load_events(path: str):
    events, seen = [], set()
    for obj in read_objects(path):
        for attrs in find_attribute_dicts(obj):
            name = EVENTS.get(attrs.get("event.name"))
            if not name:
                continue
            # The same record can appear twice (log + span); de-duplicate.
            key = (name, attrs.get("event.timestamp"), attrs.get("function_name"), attrs.get("prompt_id"))
            if key in seen:
                continue
            seen.add(key)
            events.append((name, attrs))
    events.sort(key=lambda e: e[1].get("event.timestamp") or "")
    return events


def fmt_tokens(attrs) -> str:
    return " ".join(
        f"{k.replace('_token_count', '').replace('_content', '')}={attrs.get(k, 0)}"
        for k in TOKEN_KEYS[:4]
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("log")
    ap.add_argument("--out", help="write the timeline + summary here (UTF-8) instead of stdout")
    ap.add_argument("--csv", help="write one row per API response (for charting context growth)")
    ap.add_argument("--system", help="write the distinct system instructions found in the log")
    ap.add_argument("--context", help="write the first message the model received (environment + GEMINI.md)")
    ap.add_argument("--tools", help="write every tool's name, description, and parameter schema as sent")
    args = ap.parse_args()

    # Always UTF-8: shell redirection (`>`) on Windows can produce UTF-16 or cp1252 files.
    if args.out:
        sys.stdout = open(args.out, "w", encoding="utf-8")
    elif hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")

    events = load_events(args.log)
    if not events:
        print("No Gemini CLI events found. Was telemetry enabled for this session?", file=sys.stderr)
        return 1

    print("# Timeline")
    call_no = 0
    rows = []
    for name, a in events:
        ts = (a.get("event.timestamp") or "")[11:19]
        if name == "user_prompt":
            prompt = (a.get("prompt") or "").replace("\n", " ")
            print(f"{ts}  USER        {prompt[:80]!r}")
        elif name == "api_request":
            print(f"{ts}  REQUEST     model={a.get('model')}")
        elif name == "api_response":
            call_no += 1
            print(f"{ts}  RESPONSE #{call_no:<3} model={a.get('model')} {fmt_tokens(a)} ms={a.get('duration_ms')}")
            rows.append({"call": call_no, "timestamp": a.get("event.timestamp"), "model": a.get("model"),
                         **{k: a.get(k, 0) for k in TOKEN_KEYS}})
        elif name == "api_error":
            print(f"{ts}  API ERROR   model={a.get('model')} {a.get('error_type') or a.get('error')}")
        elif name == "tool_call":
            ok = "ok" if a.get("success") in (True, "true") else "FAILED"
            fargs = str(a.get("function_args") or "").replace("\n", " ")
            print(f"{ts}  TOOL        {a.get('function_name')} [{ok}] decision={a.get('decision')} args={fargs[:70]}")

    counts = Counter(n for n, _ in events)
    tools = Counter(a.get("function_name") for n, a in events if n == "tool_call")
    failed = sum(1 for n, a in events if n == "tool_call" and a.get("success") not in (True, "true"))
    models = Counter(a.get("model") for n, a in events if n == "api_response")
    print("\n# Summary")
    print(f"user prompts:   {counts['user_prompt']}")
    print(f"model calls:    {counts['api_response']} (errors: {counts['api_error']})")
    print(f"tool calls:     {counts['tool_call']} (failed: {failed})")
    for tool, c in tools.most_common():
        print(f"  {tool}: {c}")
    print("models:         " + ", ".join(f"{m} x{c}" for m, c in models.most_common()))
    if rows:
        print(f"input tokens:   first call {rows[0]['input_token_count']}, last call {rows[-1]['input_token_count']}, "
              f"sum {sum(int(r['input_token_count'] or 0) for r in rows)}")

    if args.csv and rows:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"\nwrote {len(rows)} rows to {args.csv}", file=sys.stderr)

    if args.system:
        distinct = []
        for obj in read_objects(args.log):
            for raw in find_key(obj, "gen_ai.system_instructions"):
                s = as_text(raw)
                if s not in distinct:
                    distinct.append(s)
        if not distinct:
            print("\nNo system instructions in log (needs telemetry.traces and telemetry.logPrompts = true).", file=sys.stderr)
        else:
            with open(args.system, "w", encoding="utf-8") as f:
                for i, s in enumerate(distinct, 1):
                    f.write(f"<!-- variant {i} of {len(distinct)} -->\n{s}\n\n")
            print(f"\nwrote {len(distinct)} distinct system-instruction variant(s) to {args.system}", file=sys.stderr)

    if args.context:
        text = first_user_message(args.log)
        if text is None:
            print("\nNo model input in log (needs telemetry.traces and telemetry.logPrompts = true).", file=sys.stderr)
        else:
            with open(args.context, "w", encoding="utf-8") as f:
                f.write(text + "\n")
            print(f"\nwrote the first model input to {args.context}", file=sys.stderr)

    if args.tools:
        decls = tool_declarations(args.log)
        if not decls:
            print("\nNo tool definitions in log (needs telemetry.traces and telemetry.logPrompts = true).", file=sys.stderr)
        else:
            with open(args.tools, "w", encoding="utf-8") as f:
                for d in decls:
                    schema = d.get("parametersJsonSchema", d.get("parameters", {}))
                    f.write(f"## {d.get('name')}\n\n{d.get('description', '')}\n\n")
                    f.write("```json\n" + json.dumps(schema, indent=2) + "\n```\n\n")
            print(f"\nwrote {len(decls)} tool declarations to {args.tools}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
