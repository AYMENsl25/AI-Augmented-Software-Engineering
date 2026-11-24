# Week 5 — Build a Custom MCP Server: The Data Explorer

**Estimated time: ~3 hours.**

## Overview
Agents are only as good as the context they can reach. You'll extend that reach by
building a **Model Context Protocol (MCP) server** that wraps a real API and exposes it
as agent tools. A working server skeleton is provided — you finish the second tool and
harden it, then use it from an MCP client.

## Learning goals
- Understand MCP building blocks: **tools** and **transport**.
- Implement a typed tool with real error handling.
- Register and drive an MCP server from an agent/client.

---

## Setup
The starter is in [`starter/`](starter/) — a `FastMCP` server over the open, no-key
**[mledoze/countries](https://github.com/mledoze/countries)** dataset (the data REST
Countries was built on), with `search_countries` implemented as a worked example.

> REST Countries' free v3.1 API was retired in October 2026 and its replacement needs an
> API key, so the starter fetches the dataset directly from GitHub. It is still an HTTPS
> call with real failure modes (timeouts, HTTP errors) that your tools must handle.
```bash
cd starter && pip install -r requirements.txt
python server.py   # runs over STDIO
```

## What to do
1. **Study** the provided `search_countries` tool: input validation, the data fetch,
   error handling, and the model-friendly return shape.
2. **Implement a second tool**, `get_country_details(name)`, returning currencies,
   languages, borders, and the flag URL — reusing the same error-handling pattern.
3. **Harden** both tools: empty/invalid input, HTTP errors, timeouts, and no-result cases
   should all return clean, structured messages (never crash the server).
4. **Register the server** in an MCP client (Claude Desktop or an MCP-aware IDE) and run
   each tool at least once.

> Scope note: **STDIO transport only** this week. No remote hosting or auth required.

## Deliverables
**Submit the GitHub repository link** for `starter/`, containing:
- Your finished `server.py` with **two working tools**.
- A `README.md`: how to install, run, and register the server, plus a **tool reference**
  (names, parameters, example input/output).
- A `writeup.md`: a transcript of an agent calling both tools, how you handled errors,
  and **what you learned** (3–5 sentences on controlling what context an agent can reach).

## Evaluation (100 pts)
- 40 — Second tool implemented correctly with the right return shape.
- 25 — Robust error handling on both tools (validated with bad input).
- 20 — Server registered and driven from an MCP client (transcript shown).
- 15 — Clear README tool reference + `writeup.md` reflection.

## References
- MCP server quickstart: https://modelcontextprotocol.io/quickstart/server
- Country dataset: https://github.com/mledoze/countries
