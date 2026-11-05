from __future__ import annotations

from urllib.error import HTTPError
import unittest
from unittest.mock import patch

from scripts.audit_links import check_url, collect_urls, load_entries


class LinkAuditTests(unittest.TestCase):
    def test_collect_urls_covers_papers_and_code(self) -> None:
        urls = collect_urls(load_entries())
        usage_types = {usage["type"] for usages in urls.values() for usage in usages}
        self.assertIn("paper", usage_types)
        self.assertIn("code", usage_types)
        self.assertTrue(all(url.startswith("https://") for url in urls))

    @patch("scripts.audit_links._request")
    def test_head_404_is_confirmed_with_get(self, request) -> None:
        url = "https://example.com/paper"
        head_error = HTTPError(url, 404, "Not Found", {}, None)
        request.side_effect = [
            head_error,
            (200, url),
        ]
        result = check_url(url, retries=0)
        request.side_effect = None
        head_error.close()
        self.assertEqual("ok", result["status"])
        self.assertEqual("not-applicable", result["github_archive_status"])
        self.assertEqual(["HEAD", "GET"], [call.args[1] for call in request.call_args_list])

    @patch("scripts.audit_links._github_archived", return_value=None)
    @patch("scripts.audit_links._request")
    def test_github_archive_api_failure_remains_unknown(self, request, archived) -> None:
        url = "https://github.com/example/project"
        request.return_value = (200, url)
        result = check_url(url, retries=0)
        self.assertEqual("ok", result["status"])
        self.assertEqual("unknown", result["github_archive_status"])
        archived.assert_called_once()


if __name__ == "__main__":
    unittest.main()
