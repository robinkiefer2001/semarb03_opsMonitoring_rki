from fastapi import FastAPI, Query

from app.config import get_settings
from app.services.ingest_service import collect_and_normalize, get_latest_snapshot

settings = get_settings()

app = FastAPI(
	title=settings.app_name,
	docs_url=settings.docs_url,
	redoc_url=None,
)


@app.get("/health")
def health() -> dict[str, str]:
	return {"status": "ok", "service": "data-collector"}


@app.api_route("/collect/run", methods=["GET", "POST"])
def run_collection(limit_per_source: int = Query(default=10, ge=1, le=50)) -> dict:
	return collect_and_normalize(limit_per_source=limit_per_source)


@app.get("/collect/snapshot")
def read_snapshot() -> dict:
	return get_latest_snapshot()
