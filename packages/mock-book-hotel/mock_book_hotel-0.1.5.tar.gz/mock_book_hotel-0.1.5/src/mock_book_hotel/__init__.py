from .fastmcp_mock_test import mcp
import argparse
def main() -> None:
    parser = argparse.ArgumentParser()  # Create argument parser
    parser.add_argument('--transport', type=str, default='stdio', help='stdio/sse (default: stdio)')  # Add transport argument
    args = parser.parse_args()  # Parse arguments

    mcp.run(transport=args.transport)  # Use the parsed transport argument
