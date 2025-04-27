from mcp.server.fastmcp import FastMCP

mcp = FastMCP("test-server")

@mcp.tool()
def test_tool(name: str) -> str:
    return f"Hello {name}, this message is from test_tool" 
