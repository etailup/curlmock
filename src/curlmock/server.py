from __future__ import annotations

import json
from typing import Any

from flask import Flask, Request, Response, request

from curlmock.parser import CurlRequest, load_response, normalize_path, parse_curl


def create_app(curl_command: str, response_data: Any, *, echo: bool = False) -> Flask:
    parsed = parse_curl(curl_command)
    app = Flask("curlmock")
    target_path = normalize_path(parsed.path.split("?", 1)[0])

    @app.route("/", defaults={"subpath": ""}, methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
    @app.route("/<path:subpath>", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])
    def mock_handler(subpath: str) -> Response:
        incoming = normalize_path(f"/{subpath}" if subpath else "/")
        if incoming != target_path and not echo:
            return Response(
                json.dumps(
                    {
                        "error": "No mock route matched",
                        "expected_path": target_path,
                        "received_path": incoming,
                    }
                ),
                status=404,
                mimetype="application/json",
            )

        payload = _build_payload(parsed, request, response_data, echo=echo)
        response = Response(json.dumps(payload, indent=2), mimetype="application/json")
        for key, value in parsed.headers.items():
            if key.lower() not in ("host", "content-length"):
                response.headers[key] = value
        return response

    return app


def _build_payload(parsed: CurlRequest, req: Request, response_data: Any, *, echo: bool) -> dict[str, Any]:
    if echo:
        body: Any
        if req.data:
            try:
                body = req.get_json(force=True)
            except Exception:
                body = req.data.decode("utf-8", errors="replace")
        else:
            body = None
        return {
            "method": req.method,
            "path": req.path,
            "query": req.query_string.decode("utf-8"),
            "headers": dict(req.headers),
            "body": body,
        }

    if isinstance(response_data, dict):
        return response_data
    return {"data": response_data, "mock": {"method": parsed.method, "path": parsed.path}}


def run_server(
    curl_command: str,
    *,
    response_file: str | None = None,
    port: int = 8787,
    host: str = "127.0.0.1",
    echo: bool = False,
) -> None:
    response_data = load_response(response_file)
    app = create_app(curl_command, response_data, echo=echo)
    parsed = parse_curl(curl_command)
    print(f"curlmock listening on http://{host}:{port}{parsed.path.split('?', 1)[0]}")
    print(f"Method: {parsed.method}")
    if response_file:
        print(f"Response: {response_file}")
    elif echo:
        print("Mode: echo (returns incoming request)")
    app.run(host=host, port=port, debug=False)
