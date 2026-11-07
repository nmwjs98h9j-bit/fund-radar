"""JSON cache loading and record deduplication."""

import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

def _load(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except:
            pass
    return default


def _save(path: Path, data):
    path.write_text(json.dumps(data, indent=2, default=str))


def _merge_funds(existing: list, new_funds: list) -> list:
    """Merge new funds into existing list, deduplicating by name."""
    by_name = {f["name"].lower(): f for f in existing}
    added = 0
    for f in new_funds:
        key = f["name"].lower()
        if key not in by_name:
            by_name[key] = f
            added += 1
    log.info(f"Merged {added} new funds (total: {len(by_name)})")
    return list(by_name.values())


def _merge_news(existing: list, new_items: list) -> list:
    seen = {n["headline"] for n in existing}
    merged = list(existing)
    for item in new_items:
        if item["headline"] not in seen:
            merged.insert(0, item)
            seen.add(item["headline"])
    return merged[:100]  # keep latest 100


