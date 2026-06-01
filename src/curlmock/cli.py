from __future__ import annotations

import argparse

from curlmock.server import run_server


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="curlmock",
        description="Start a mock API server from a cURL command.",
    )
    parser.add_argument(
        "curl_command",
        help='cURL command to mock, e.g. curl -X POST https://api.example.com/users -d "{\\"name\\":\\"Alex\\"}"',
    )
    parser.add_argument(
        "-r",
        "--response",
        help="JSON file (or raw text) to return as the mock response.",
    )
    parser.add_argument(
        "--echo",
        action="store_true",
        help="Echo the incoming request instead of returning a fixed response.",
    )
    parser.add_argument("--port", type=int, default=8787, help="Port to listen on (default: 8787).")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1).")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_server(
        args.curl_command,
        response_file=args.response,
        port=args.port,
        host=args.host,
        echo=args.echo,
    )


if __name__ == "__main__":
    main()
