"""Flask routes, refresh orchestration and local development startup."""

import logging
import os
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler

from fund_radar.seeds import SEED_FUNDS, SEED_NEWS
from fund_radar.scrapers import scrape_edgar, scrape_nfa, scrape_news
from fund_radar.storage import _load, _save, _merge_funds, _merge_news

DATA_DIR = Path(os.environ.get("DATA_DIR", Path(__file__).parent / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
FUNDS_FILE = DATA_DIR / "funds.json"
NEWS_FILE  = DATA_DIR / "news.json"
STATUS_FILE = DATA_DIR / "status.json"

REFRESH_INTERVAL_MINUTES = 60  # how often to scrape

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

app = Flask(__name__, static_folder="static")
CORS(app)

def refresh_all():
    log.info("=== Starting refresh cycle ===")
    status = {"edgar": "ok", "nfa": "ok", "news": "ok", "last_run": datetime.now().isoformat()}

    # Load existing
    funds = _load(FUNDS_FILE, list(SEED_FUNDS))
    news  = _load(NEWS_FILE,  list(SEED_NEWS))

    # Scrape
    try:
        edgar_funds = scrape_edgar()
        funds = _merge_funds(funds, edgar_funds)
    except Exception as e:
        log.error(f"EDGAR scrape error: {e}")
        status["edgar"] = "error"

    try:
        nfa_funds = scrape_nfa()
        funds = _merge_funds(funds, nfa_funds)
    except Exception as e:
        log.error(f"NFA scrape error: {e}")
        status["nfa"] = "error"

    try:
        news_items = scrape_news()
        news = _merge_news(news, news_items)
    except Exception as e:
        log.error(f"News scrape error: {e}")
        status["news"] = "error"

    # Save
    _save(FUNDS_FILE, funds)
    _save(NEWS_FILE, news)
    _save(STATUS_FILE, status)
    log.info(f"=== Refresh done: {len(funds)} funds, {len(news)} news items ===")


# ── API Routes ─────────────────────────────────────────────────────────────────

@app.route("/api/funds")
def api_funds():
    funds = _load(FUNDS_FILE, SEED_FUNDS)
    return jsonify({"funds": funds, "count": len(funds)})


@app.route("/api/news")
def api_news():
    news = _load(NEWS_FILE, SEED_NEWS)
    return jsonify({"news": news, "count": len(news)})


@app.route("/api/status")
def api_status():
    status = _load(STATUS_FILE, {"last_run": None, "edgar": "unknown", "nfa": "unknown", "news": "unknown"})
    return jsonify(status)


@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    """Trigger a manual refresh."""
    import threading
    threading.Thread(target=refresh_all, daemon=True).start()
    return jsonify({"message": "Refresh started", "started_at": datetime.now().isoformat()})


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# ── Startup ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Run initial scrape if no data yet
    if not FUNDS_FILE.exists():
        log.info("No data found — running initial scrape...")
        refresh_all()
    else:
        log.info("Existing data found, serving immediately.")

    # Schedule background refresh
    scheduler = BackgroundScheduler()
    scheduler.add_job(refresh_all, "interval", minutes=REFRESH_INTERVAL_MINUTES, id="refresh")
    scheduler.start()
    log.info(f"Scheduler started — refreshing every {REFRESH_INTERVAL_MINUTES} minutes")

    print("\n" + "="*55)
    print("  MACRO/CTA FUND RADAR — Backend Running")
    print("  Dashboard: http://localhost:5000")
    print("  API:       http://localhost:5000/api/funds")
    print("="*55 + "\n")

    app.run(host="0.0.0.0", port=5000, debug=False)

