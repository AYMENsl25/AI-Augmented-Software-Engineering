"""Minimal MCP client: spawns server.py over STDIO, lists tools, calls each with good and bad input.
Usage: python demo_client.py server.py"""
import asyncio, sys, json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
calls = [("search_countries",{"query":"united","limit":3}),("get_country_details",{"name":"Germany"}),
("get_country_details",{"name":"JP"}),("search_countries",{"query":"   "}),("search_countries",{"query":"a","limit":0}),
("search_countries",{"query":"zzzz"}),("get_country_details",{"name":""}),("get_country_details",{"name":"Atlantis"}),("get_country_details",{"name":"guinea"})]
async def main():
    env = None
    p = StdioServerParameters(command=sys.executable, args=[sys.argv[1]])
    async with stdio_client(p) as (r,w):
        async with ClientSession(r,w) as s:
            await s.initialize()
            print("TOOLS:", [t.name for t in (await s.list_tools()).tools])
            for n,a in (calls if len(sys.argv)<3 else calls[:2]):
                res = await s.call_tool(n,a)
                print(f"\n> {n}({json.dumps(a)})\n" + "\n".join(c.text for c in res.content))
asyncio.run(main())
