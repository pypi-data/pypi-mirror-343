from server import mcp

def main():
    # logging.info("Starting Agent Factory MCP server")
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()