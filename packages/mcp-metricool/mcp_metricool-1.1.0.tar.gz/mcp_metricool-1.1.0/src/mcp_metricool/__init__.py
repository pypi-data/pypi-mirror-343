from .server import mcp

def main() -> None:
    "Run the Metricool MCP server"
    mcp.run(transport='stdio')
