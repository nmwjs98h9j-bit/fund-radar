"""Offline checks; no collector or scheduler is started by these tests."""

import importlib
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from fund_radar.storage import _merge_funds, _merge_news


class FundRadarTests(unittest.TestCase):
    def test_fund_merge_preserves_existing_records(self):
        existing = [{"name": "Example Capital", "aum": 100}]
        merged = _merge_funds(existing, [{"name": "EXAMPLE CAPITAL", "aum": 200}, {"name": "New Fund"}])
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0]["aum"], 100)
        self.assertEqual(len(existing), 1)

    def test_news_merge_deduplicates_and_caps_history(self):
        existing = [{"headline": f"Story {i}"} for i in range(100)]
        merged = _merge_news(existing, [{"headline": "Story 0"}, {"headline": "New story"}])
        self.assertEqual(len(merged), 100)
        self.assertEqual(merged[0]["headline"], "New story")
        self.assertEqual(sum(item["headline"] == "Story 0" for item in merged), 1)

    def test_routes_serve_samples_and_cached_records(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"DATA_DIR": directory}):
            module = importlib.import_module("app")
            module = importlib.reload(module)
            client = module.app.test_client()
            with client.get("/") as response:
                self.assertEqual(response.status_code, 200)
            funds = client.get("/api/funds").get_json()
            self.assertEqual(funds["count"], len(module.SEED_FUNDS))
            self.assertIsNone(client.get("/api/status").get_json()["last_run"])
            Path(directory, "funds.json").write_text('[{"name": "Cached fund"}]')
            self.assertEqual(client.get("/api/funds").get_json()["funds"], [{"name": "Cached fund"}])


if __name__ == "__main__":
    unittest.main()
