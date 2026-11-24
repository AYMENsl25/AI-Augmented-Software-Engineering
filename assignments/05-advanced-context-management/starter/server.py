"""Data Explorer — MCP server for Week 5.

Wraps the open `mledoze/countries` dataset (the data REST Countries was built on) and
exposes it to an agent as two MCP tools over STDIO:

    search_countries(query, limit=5)  -> list of {name, capital, region, subregion}
    get_country_details(name)         -> {name, currencies, languages, borders, flag_url}

The dataset is fetched over HTTPS on the first call and cached in memory. Every failure
(bad input, timeout, HTTP error, bad JSON, no match) comes back as a structured
{"error": ...} message so the server never crashes and the model can recover.

Setup:
    pip install -r requirements.txt
Run (STDIO):
    python server.py
"""
import httpx
from mcp.server.fastmcp import FastMCP

DATA_URL = "https://raw.githubusercontent.com/mledoze/countries/master/countries.json"
FLAG_URL = "https://raw.githubusercontent.com/mledoze/countries/master/data/{cca3}.svg"
TIMEOUT_SECONDS = 15
MAX_LIMIT = 50
MAX_QUERY_LEN = 100

mcp = FastMCP("data-explorer")

_countries: list[dict] | None = None  # in-memory cache of the dataset


class UpstreamError(Exception):
    """The dataset could not be fetched or parsed."""


def load_countries() -> list[dict]:
    """Download the dataset once and cache it. Raises UpstreamError on any failure."""
    global _countries
    if _countries is None:
        try:
            resp = httpx.get(DATA_URL, timeout=TIMEOUT_SECONDS, follow_redirects=True)
            resp.raise_for_status()
            data = resp.json()
        except httpx.TimeoutException:
            raise UpstreamError(f"timed out after {TIMEOUT_SECONDS}s fetching the dataset")
        except httpx.HTTPStatusError as exc:
            raise UpstreamError(f"dataset server returned HTTP {exc.response.status_code}")
        except httpx.HTTPError as exc:
            raise UpstreamError(f"network error fetching the dataset: {exc}")
        except ValueError:
            raise UpstreamError("dataset response was not valid JSON")
        if not isinstance(data, list):
            raise UpstreamError("dataset has an unexpected shape")
        _countries = data
    return _countries


def _clean(text: object) -> str | None:
    """Return stripped text, or None if it isn't usable input."""
    if not isinstance(text, str):
        return None
    text = text.strip()
    return text or None


@mcp.tool()
def search_countries(query: str, limit: int = 5) -> list[dict]:
    """Search countries by (partial) name. Returns a list of {name, capital, region,
    subregion}. An empty list means no country matched. `limit` is 1-50."""
    q = _clean(query)
    if q is None:
        return [{"error": "query must be a non-empty string"}]
    if len(q) > MAX_QUERY_LEN:
        return [{"error": f"query is too long (max {MAX_QUERY_LEN} characters)"}]
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= MAX_LIMIT:
        return [{"error": f"limit must be an integer between 1 and {MAX_LIMIT}"}]
    try:
        countries = load_countries()
    except UpstreamError as exc:
        return [{"error": f"upstream request failed: {exc}"}]

    q = q.lower()
    results = []
    for c in countries:
        name = c.get("name") or {}
        if q in name.get("common", "").lower() or q in name.get("official", "").lower():
            results.append(
                {
                    "name": name.get("common"),
                    "capital": (c.get("capital") or [None])[0],
                    "region": c.get("region"),
                    "subregion": c.get("subregion"),
                }
            )
            if len(results) == limit:
                break
    return results


def _find_country(countries: list[dict], name: str) -> dict | None:
    """Exact match on common/official name or cca2/cca3 code, else a unique partial match."""
    key = name.lower()
    for c in countries:
        n = c.get("name") or {}
        if key in (
            n.get("common", "").lower(),
            n.get("official", "").lower(),
            c.get("cca2", "").lower(),
            c.get("cca3", "").lower(),
        ):
            return c
    partial = [c for c in countries if key in (c.get("name") or {}).get("common", "").lower()]
    return partial[0] if len(partial) == 1 else None


@mcp.tool()
def get_country_details(name: str) -> dict:
    """Get details for one country by name or ISO code (e.g. "Germany", "DE", "DEU").
    Returns {name, official_name, cca3, currencies, languages, borders, flag_url}.
    `borders` lists neighbour country names (empty for island nations)."""
    n = _clean(name)
    if n is None:
        return {"error": "name must be a non-empty string"}
    if len(n) > MAX_QUERY_LEN:
        return {"error": f"name is too long (max {MAX_QUERY_LEN} characters)"}
    try:
        countries = load_countries()
    except UpstreamError as exc:
        return {"error": f"upstream request failed: {exc}"}

    c = _find_country(countries, n)
    if c is None:
        return {
            "error": f"no single country matches '{n}'",
            "hint": "use search_countries to find the exact name",
        }

    by_code = {x.get("cca3"): (x.get("name") or {}).get("common") for x in countries}
    cca3 = c.get("cca3")
    return {
        "name": c["name"].get("common"),
        "official_name": c["name"].get("official"),
        "cca3": cca3,
        "currencies": [
            {"code": code, "name": cur.get("name"), "symbol": cur.get("symbol")}
            for code, cur in (c.get("currencies") or {}).items()
        ],
        "languages": sorted((c.get("languages") or {}).values()),
        "borders": [by_code.get(b, b) for b in c.get("borders") or []],
        "flag_url": FLAG_URL.format(cca3=cca3.lower()) if cca3 else None,
    }


if __name__ == "__main__":
    mcp.run()
