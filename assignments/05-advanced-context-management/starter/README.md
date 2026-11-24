# Data Explorer — MCP Server

A `FastMCP` server (STDIO transport) over the open, no-key
[mledoze/countries](https://github.com/mledoze/countries) dataset. It gives an agent two
tools: search countries by name, and get one country's details.

## Install
Requires Python 3.10+. Use a virtual environment so the pinned `mcp<2` doesn't clash with
a global mcp 2.x install:
```bash
python -m venv .venv
.venv/Scripts/activate        # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
```

## Run
```bash
python server.py
```
It speaks MCP over STDIO, so it prints nothing and waits for a client. That is normal.

Quick check without a chat client (spawns the server, calls both tools with good and bad input):
```bash
python demo_client.py server.py
```

## Register in an MCP client
**Claude Desktop** (`%APPDATA%\Claude\claude_desktop_config.json` on Windows,
`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS). Use absolute
paths, and point `command` at the venv's Python:
```json
{
  "mcpServers": {
    "data-explorer": {
      "command": "C:/absolute/path/to/starter/.venv/Scripts/python.exe",
      "args": ["C:/absolute/path/to/starter/server.py"]
    }
  }
}
```
Restart Claude Desktop. The tools show up under the tools (🔨) icon.

**Claude Code:**
```bash
claude mcp add data-explorer -- /absolute/path/to/.venv/Scripts/python.exe /absolute/path/to/server.py
```

## Tool reference

### `search_countries(query: str, limit: int = 5) -> list[dict]`
Matches `query` as a case-insensitive substring against each country's common and official names.

| Param | Type | Rules |
|---|---|---|
| `query` | string | required, non-blank, ≤ 100 chars |
| `limit` | int | 1–50, default 5 |

Example input `{"query": "united", "limit": 2}` gives:
```json
[
  {"name": "United Arab Emirates", "capital": "Abu Dhabi", "region": "Asia", "subregion": "Western Asia"},
  {"name": "United Kingdom", "capital": "London", "region": "Europe", "subregion": "Northern Europe"}
]
```
If nothing matches, it returns `[]` (an empty list, not an error).

### `get_country_details(name: str) -> dict`
Looks up one country by its common name, official name, or ISO code (`DE` / `DEU`). If
there's no exact match, it accepts a partial name only when that partial matches exactly
one country.

Example input `{"name": "Germany"}` gives:
```json
{
  "name": "Germany",
  "official_name": "Federal Republic of Germany",
  "cca3": "DEU",
  "currencies": [{"code": "EUR", "name": "Euro", "symbol": "€"}],
  "languages": ["German"],
  "borders": ["Austria", "Belgium", "Czechia", "Denmark", "France", "Luxembourg", "Netherlands", "Poland", "Switzerland"],
  "flag_url": "https://raw.githubusercontent.com/mledoze/countries/master/data/deu.svg"
}
```
`borders` lists neighbour names, converted from cca3 codes. Island nations get `[]`.

### Errors (both tools)
Failures come back as data, never as a crash: `{"error": "..."}`. `search_countries`
wraps it in a list.

| Case | Example message |
|---|---|
| Empty or blank input | `query must be a non-empty string` |
| Bad `limit` | `limit must be an integer between 1 and 50` |
| No match (details) | `no single country matches 'Atlantis'` + a `hint` |
| HTTP error | `upstream request failed: dataset server returned HTTP 404` |
| Timeout (15 s) | `upstream request failed: timed out after 15s fetching the dataset` |
| Network / DNS | `upstream request failed: network error fetching the dataset: ...` |
| Bad JSON | `upstream request failed: dataset response was not valid JSON` |
