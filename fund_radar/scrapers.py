"""Best-effort collection from public search results and RSS feeds."""

import hashlib
import logging
import re
import time
from datetime import datetime

import feedparser
import requests

log = logging.getLogger(__name__)

MACRO_KEYWORDS = [
    "global macro", "macro fund", "CTA", "commodity trading advisor",
    "managed futures", "systematic macro", "discretionary macro",
    "trend following", "macro hedge fund"
]

HEADERS = {"User-Agent": "FundRadar/1.0 (allocator research tool; contact@example.com)"}


def scrape_edgar() -> list:
    """Query SEC EDGAR full-text search for recent macro/CTA Form ADV filings."""
    results = []
    seen = set()

    queries = ["global macro hedge fund", "commodity trading advisor", "merger arbitrage fund", "commodity hedge fund"]
    for q in queries:
        try:
            url = (
                "https://efts.sec.gov/LATEST/search-index"
                f"?q={requests.utils.quote(q)}"
                "&forms=ADV"
                "&dateRange=custom&startdt=2022-01-01"
            )
            r = requests.get(url, headers=HEADERS, timeout=15)
            r.raise_for_status()
            data = r.json()
            hits = data.get("hits", {}).get("hits", [])
            for h in hits[:10]:
                src = h.get("_source", {})
                name = (src.get("display_names") or [None])[0] or src.get("entity_name", "")
                if not name or name in seen:
                    continue
                seen.add(name)
                results.append({
                    "id": f"edgar-{hashlib.md5(name.encode()).hexdigest()[:8]}",
                    "name": name,
                    "strategy": _infer_strategy(src.get("file_description", "") + " " + name),
                    "aum": None,
                    "perf": None,
                    "date": src.get("file_date", "")[:10] or src.get("period_of_report", "")[:10],
                    "source": "edgar",
                    "cik": src.get("entity_id", ""),
                    "founders": "",
                    "prior": "",
                })
            time.sleep(0.5)  # be polite
        except Exception as e:
            log.warning(f"EDGAR query '{q}' failed: {e}")

    log.info(f"EDGAR: {len(results)} results")
    return results


def scrape_nfa() -> list:
    """
    NFA BASIC blocks direct API calls. We use their public CSV bulk data export
    which lists all registered CPOs/CTAs — available at nfa.futures.org.
    """
    results = []
    try:
        # NFA provides a downloadable CSV of all CTA registrations
        url = "https://www.nfa.futures.org/BasicNet/basicnet-registration-list.aspx"
        r = requests.get(url, headers=HEADERS, timeout=20)
        # Parse whatever we can from the response
        text = r.text
        # Extract firm names from the HTML table if present
        names = re.findall(r'<td[^>]*>([A-Z][A-Za-z\s,\.]+(?:Capital|Fund|Management|Advisors|Partners|Trading|CTA)[A-Za-z\s,\.]*)</td>', text)
        for name in names[:15]:
            name = name.strip()
            if len(name) < 5 or len(name) > 80:
                continue
            results.append({
                "id": f"nfa-{hashlib.md5(name.encode()).hexdigest()[:8]}",
                "name": name,
                "strategy": _infer_strategy(name),
                "aum": None,
                "perf": None,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "source": "nfa",
                "founders": "",
                "prior": "",
            })
    except Exception as e:
        log.warning(f"NFA scrape failed: {e}")

    log.info(f"NFA: {len(results)} results")
    return results


def scrape_news() -> list:
    """Pull macro/CTA fund news from public RSS feeds."""
    feeds = [
        ("Hedgeweek",           "https://www.hedgeweek.com/feed/"),
        ("Hedge Fund Journal",  "https://thehedgefundjournal.com/feed/"),
        ("HedgeNordic",         "https://hedgenordic.com/feed/"),
        ("Institutional Inv.",  "https://www.institutionalinvestor.com/rss/articles.aspx"),
    ]

    kw_pattern = re.compile(
        r'\b(macro|CTA|managed futures|trend.follow|commodity trading|spin.?out|hedge fund launch|new fund|merger arb|merger arbitrage|event.driven|commodity fund|energy fund|agricultural fund)\b',
        re.IGNORECASE
    )

    items = []
    seen_headlines = set()

    for source_name, feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:20]:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                combined = title + " " + summary
                if not kw_pattern.search(combined):
                    continue
                if title in seen_headlines:
                    continue
                seen_headlines.add(title)

                published = entry.get("published", "")
                try:
                    pub_dt = datetime(*entry.published_parsed[:6]) if entry.get("published_parsed") else datetime.now()
                    time_str = pub_dt.strftime("%b %d %Y")
                except:
                    time_str = published[:10] if published else "Recent"

                tags = _extract_tags(combined)
                items.append({
                    "id": f"news-{hashlib.md5(title.encode()).hexdigest()[:8]}",
                    "headline": title[:140],
                    "source": source_name,
                    "time": time_str,
                    "tag": " ".join(tags[:4]),
                    "fundRef": None,
                    "url": entry.get("link", ""),
                })
        except Exception as e:
            log.warning(f"RSS feed {source_name} failed: {e}")

    log.info(f"News: {len(items)} relevant items")
    return items


def _infer_strategy(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["merger", "arbitrage", "arb", "event.driven", "m&a"]):  return "merger-arb"
    if any(w in t for w in ["commodity", "energy", "agriculture", "metals", "natural resource"]): return "commodity"
    if any(w in t for w in ["cta", "commodity trading", "managed futures"]): return "cta"
    if any(w in t for w in ["systematic", "quant", "algorithmic", "trend"]):  return "systematic"
    if "discretionary" in t: return "discretionary"
    if "multi" in t:         return "multi"
    return "macro"


def _extract_tags(text: str) -> list:
    kws = ["macro", "CTA", "spin-out", "launch", "systematic", "Brevan", "Millennium",
           "Citadel", "Bridgewater", "trend", "allocator", "emerging",
           "merger", "arbitrage", "commodity", "energy", "agriculture"]
    found = [f"#{w.lower()}" for w in kws if re.search(w, text, re.IGNORECASE)]
    return found[:4]


