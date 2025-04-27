import logging
import sys
from .server import serve

def main() -> None:
    """Futurx Brain MCP - Brain functionality for MCP"""
    import asyncio

    logging.basicConfig( stream=sys.stderr)
    asyncio.run(serve())

if __name__ == "__main__":
    main()