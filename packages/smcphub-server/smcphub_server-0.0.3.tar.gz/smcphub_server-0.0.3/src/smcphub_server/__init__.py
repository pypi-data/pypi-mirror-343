from .server import SmcphubServer


def main():
    """MCP Server, by SMCPHUB."""
    import asyncio
    smcphubServer = SmcphubServer()

    asyncio.run(smcphubServer.serve())


if __name__ == "__main__":
    main()