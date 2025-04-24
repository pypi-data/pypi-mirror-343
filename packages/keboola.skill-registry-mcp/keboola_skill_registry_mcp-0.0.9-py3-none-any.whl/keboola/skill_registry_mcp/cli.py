"""Command-line interface for the Keboola MCP server."""

import argparse
import logging
import os
import sys
from typing import List, Optional

from .config import Config
from .server import create_server

logger = logging.getLogger(__name__)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        args: Command line arguments. If None, uses sys.argv[1:].

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description="Keboola MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport to use for MCP communication",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level",
    )
    parser.add_argument(
        "--api-url", default="http://localhost:8888", help="Skill Registry API URL"
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> None:
    """Run the MCP server.

    Args:
        args: Command line arguments. If None, uses sys.argv[1:].
    """
    parsed_args = parse_args(args)

    # Configure logging
    logging.basicConfig(
        format="%(asctime)s %(name)s %(levelname)s: %(message)s",
        level=parsed_args.log_level,
        stream=sys.stderr,
    )

    # Create config from the CLI arguments
    config = Config(skill_registry_url=parsed_args.api_url,
                    skill_registry_token=os.environ.get("SKILL_REGISTRY_TOKEN"), )

    try:
        # Create and run server
        mcp = create_server(config)
        mcp.run(transport=parsed_args.transport)
    except Exception as e:
        logger.error(f"Server failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
