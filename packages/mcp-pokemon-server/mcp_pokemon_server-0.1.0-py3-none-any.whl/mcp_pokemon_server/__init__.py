from .pokemon.mcp import mcp
def main() -> None:
    print("Hello from mcp-pokemon-server!")
    mcp.run(transport='stdio')
