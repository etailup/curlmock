from __future__ import annotations

import unittest

from curlmock.parser import parse_curl


class ParseCurlTests(unittest.TestCase):
    def test_get_request(self) -> None:
        req = parse_curl("curl https://api.example.com/users")
        self.assertEqual(req.method, "GET")
        self.assertEqual(req.path, "/users")

    def test_post_with_body(self) -> None:
        req = parse_curl('curl -X POST https://api.example.com/users -H "Content-Type: application/json" -d "{\\"name\\":\\"Alex\\"}"')
        self.assertEqual(req.method, "POST")
        self.assertEqual(req.path, "/users")
        self.assertEqual(req.headers["Content-Type"], "application/json")
        self.assertIn("Alex", req.body or "")

    def test_query_string_preserved(self) -> None:
        req = parse_curl("curl 'https://api.example.com/search?q=hello'")
        self.assertEqual(req.path, "/search?q=hello")


if __name__ == "__main__":
    unittest.main()
