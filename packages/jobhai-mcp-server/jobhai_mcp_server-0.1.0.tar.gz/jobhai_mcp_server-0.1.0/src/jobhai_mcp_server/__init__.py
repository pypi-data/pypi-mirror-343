import asyncio
import logging
import sys

import click

from jobhai_mcp_server.server_safe import serve as serve_safe

@click.command()
@click.option("-v", "--verbose", count=True, help="Increase verbosity")
def main(verbose: int) -> None:
    """MCP server for Job Hai"""
    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stderr)

    asyncio.run(serve_safe())


if __name__ == "__main__":
    main()