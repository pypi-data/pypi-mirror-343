from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP("test-server")

@mcp_server.tool()
def test_tool(name: str) -> str:
    return f"Hello {name}, this message is from test_tool" 
