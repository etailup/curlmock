from __future__ import annotations

import json
import re
import shlex
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse


@dataclass
class CurlRequest:
    method: str = "GET"
    url: str = ""
    path: str = "/"
    headers: dict[str, str] = field(default_factory=dict)
    body: str | None = None


def parse_curl(command: str) -> CurlRequest:
    tokens = shlex.split(command.strip())
    if not tokens or tokens[0] != "curl":
        raise ValueError("Command must start with curl")

    req = CurlRequest()
    index = 1
    while index < len(tokens):
        token = tokens[index]

        if token in ("-X", "--request"):
            index += 1
            req.method = tokens[index].upper()
        elif token in ("-H", "--header"):
            index += 1
            key, _, value = tokens[index].partition(":")
            req.headers[key.strip()] = value.strip()
        elif token in ("-d", "--data", "--data-raw", "--data-binary"):
            index += 1
            req.body = tokens[index]
            if req.method == "GET":
                req.method = "POST"
        elif token.startswith("http://") or token.startswith("https://"):
            req.url = token
        elif token in ("-s", "-S", "-L", "-k", "--silent", "--show-error", "--location", "--insecure"):
            pass
        elif token.startswith("-"):
            raise ValueError(f"Unsupported curl flag: {token}")
        else:
            req.url = token

        index += 1

    if not req.url:
        raise ValueError("No URL found in curl command")

    parsed = urlparse(req.url)
    req.path = parsed.path or "/"
    if parsed.query:
        req.path = f"{req.path}?{parsed.query}"
    return req


def load_response(path: str | None) -> Any:
    if not path:
        return {"ok": True, "message": "Mock response from curlmock"}
    text = open(path, encoding="utf-8").read()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def normalize_path(path: str) -> str:
    return re.sub(r"/+$", "", path) or "/"
