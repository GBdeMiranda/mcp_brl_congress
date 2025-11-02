import sys

from mcp_brl_congress import server


def main():
    try:
        print("Iniciando servidor MCP...", file=sys.stderr)
        server.mcp.run(transport="stdio")
    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main()
