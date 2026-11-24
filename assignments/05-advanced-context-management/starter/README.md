# Starter — Data Explorer MCP Server

A `FastMCP` server over the open, no-key **[mledoze/countries](https://github.com/mledoze/countries)**
dataset (the data REST Countries was built on). `search_countries` is a worked example;
you implement a second tool and harden both.

> REST Countries' free v3.1 API was retired in October 2026 and its replacement needs an
> API key, so this starter fetches the dataset directly from GitHub instead. It is still
> an HTTPS call with real failure modes (timeouts, HTTP errors) to handle.

## Setup
```bash
pip install -r requirements.txt
```

## Run (STDIO)
```bash
python server.py
```
This speaks MCP over STDIO. It prints nothing and waits for a client; that is normal.
Register the command in an MCP client (Claude Desktop or an MCP-aware IDE), then invoke
the tools from the client's chat.

## Register in Claude Desktop (example)
Add to your client's MCP config:
```json
{
  "mcpServers": {
    "data-explorer": { "command": "python", "args": ["/absolute/path/to/server.py"] }
  }
}
```

## Your job
- Implement `get_country_details(name)` (currencies, languages, borders, flag URL).
- Make both tools handle empty/invalid input, HTTP errors, timeouts, and no results.
