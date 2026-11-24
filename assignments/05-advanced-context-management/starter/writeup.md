# Week 5 Writeup: Data Explorer MCP Server

## 1. Transcript: an agent calling both tools

<!-- TODO: paste your Claude Desktop (or IDE) chat here once the server is registered.
     Suggested prompt: "Which countries border Germany, and what currency does it use?
     Then look up 'Atlantis'." Add a screenshot if you can. -->

**Programmatic MCP client run** (`python demo_client.py server.py`; the full output is in
[`transcript.txt`](transcript.txt)). This is a real MCP session over STDIO:
`initialize`, then `tools/list`, then `tools/call`.

```
TOOLS: ['search_countries', 'get_country_details']

> search_countries({"query": "united", "limit": 3})
  United Arab Emirates / United Kingdom / Mexico   (Mexico matches its official name, "United Mexican States")

> get_country_details({"name": "Germany"})
  currencies: EUR (Euro, €) · languages: German
  borders: Austria, Belgium, Czechia, Denmark, France, Luxembourg, Netherlands, Poland, Switzerland
  flag_url: .../data/deu.svg

> get_country_details({"name": "JP"})          -> Japan, JPY, borders: []
> search_countries({"query": "   "})           -> {"error": "query must be a non-empty string"}
> search_countries({"query": "a", "limit": 0}) -> {"error": "limit must be an integer between 1 and 50"}
> search_countries({"query": "zzzz"})          -> []
> get_country_details({"name": ""})            -> {"error": "name must be a non-empty string"}
> get_country_details({"name": "Atlantis"})    -> {"error": "no single country matches 'Atlantis'",
                                                   "hint": "use search_countries to find the exact name"}
```

**Upstream failures**, simulated by pointing `DATA_URL` at broken targets:
```
HTTP 404 -> {'error': 'upstream request failed: dataset server returned HTTP 404'}
timeout  -> {'error': 'upstream request failed: timed out after 2s fetching the dataset'}
DNS fail -> {'error': 'upstream request failed: network error fetching the dataset: [Errno 11001] getaddrinfo failed'}
```

## 2. How I handled errors

- **Input validation first.** Each tool checks its input before any network call: blank or
  non-string input, input over 100 characters, and a `limit` outside 1–50 (booleans
  rejected too). Bad input never costs a fetch.
- **One place for upstream failures.** `load_countries()` turns every failure (timeout,
  HTTP status, other network error, invalid JSON, wrong shape) into a single
  `UpstreamError` with a human-readable reason. Both tools catch only that one exception
  and return `{"error": ...}`. A failed fetch isn't cached, so the next call retries.
- **Defensive parsing.** Records are read with `.get()` and defaults, so a country with
  no capital, currencies or borders gives `null` or `[]` instead of a `KeyError`.
- **Model-friendly outcomes.** "No results" from search is an empty list, not an error,
  because nothing went wrong. "Not found" from details is an error with a `hint` that
  points the agent at `search_countries`. An ambiguous partial name such as "united" is
  refused rather than guessed.

## 3. What I learned

An MCP server is effectively a boundary around what an agent can see and do. The agent
reaches only the tools I register, with the parameters I allow, and gets back the fields
I choose. Returning shaped, compact results (border *names* rather than codes, a short
list instead of the whole 250-country dataset) keeps the context window small and makes
the model's next step easier. Errors are context too: a clear message with a hint lets
the agent recover by itself, while a raw traceback or a crashed server stalls the whole
loop. Validating input on the server side also means I don't have to trust the model to
send well-formed arguments.
