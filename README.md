# Fund Radar

A research dashboard for exploring macro, managed-futures, commodity and event-driven fund leads. A Flask API combines bundled sample records with best-effort collection from SEC search results, NFA pages and public news feeds.

This is the most complete Fund Radar version in this account: it includes the dashboard, API and container configuration. Earlier `take5` and `hopefully` repositories are backend snapshots.

## Run locally

Use Python 3.11.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`. On first launch, collection runs before the server starts and can take time if external services are slow. Running `app.py` directly starts an hourly background refresh.

## Source layout

| Path | Responsibility |
| --- | --- |
| `app.py` | Flask routes, refresh orchestration and development startup |
| `fund_radar/scrapers.py` | External search, HTML and RSS collection |
| `fund_radar/storage.py` | JSON cache and deduplication |
| `fund_radar/seeds.py` | Bundled sample funds and headlines |
| `static/index.html` | Browser dashboard |
| `tests/` | Offline API and merge checks |

## API

| Method | Path | Response |
| --- | --- | --- |
| GET | `/api/funds` | Funds and record count |
| GET | `/api/news` | Headlines and record count |
| GET | `/api/status` | Last refresh time and source status |
| POST | `/api/refresh` | Starts a refresh in a background thread |

Cache files are written under `data/`, or the directory supplied through `DATA_DIR`. Keep that directory on persistent storage if deploying to a container host.

## Checks

```sh
python -m unittest discover -s tests -v
```

The tests use temporary storage and do not contact external sources.

## Deployment and limitations

The Dockerfile and Procfile serve `app:app` with Gunicorn. Importing the app this way does **not** start the scheduler or an initial collection. A separate trusted refresh process is needed for scheduled collection in that deployment. The bundled records are available before the first refresh.

The refresh endpoint has no authentication or rate limiting. Restrict access before exposing writes on a public host. JSON files have no multi-process locking; overlapping refreshes are not coordinated.

Bundled AUM, performance figures and headlines are sample content and have not been independently verified. Collectors can return incomplete or empty results, and a source marked `ok` does not guarantee a successful query because some collector errors are handled internally. The NFA collector uses an HTML pattern, not a supported data API. Set a real contact identity in `HEADERS` before using the SEC collector.
