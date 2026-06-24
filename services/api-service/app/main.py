from __future__ import annotations

from typing import Any

import requests
from fastapi import Body, Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import get_settings
from app.db.neo4j_client import neo4j_client
from app.middleware.auth import optional_api_key
from app.utils.pagination import paginate

settings = get_settings()


class DeviceRecord(BaseModel):
	device_id: str = Field(..., min_length=1)
	hostname: str = Field(..., min_length=1)
	device_type: str = "server"
	platform: str = "windows"
	vendor: str = ""
	product: str = ""
	version: str = ""
	business_unit: str = ""
	owner: str = ""
	identity_provider: str = "entra"
	tags: list[str] = Field(default_factory=list)


class DevicePushPayload(BaseModel):
	devices: list[DeviceRecord] = Field(default_factory=list)


_DEVICE_STORE: dict[str, DeviceRecord] = {}


def _hydrate_devices_from_db() -> None:
	if _DEVICE_STORE:
		return
	try:
		for row in neo4j_client.load_devices():
			device = DeviceRecord(**row)
			_DEVICE_STORE[device.device_id] = device
	except Exception:
		return

app = FastAPI(
	title=settings.app_name,
	docs_url=settings.docs_url,
	redoc_url=None,
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)


def _fallback_snapshot() -> dict[str, Any]:
	return {
		"generated_at": "",
		"stats": {"advisory_count": 0, "cve_count": 0, "sources": []},
		"advisories": [],
		"cves": [],
	}


def _fetch_snapshot() -> dict[str, Any]:
	try:
		response = requests.get(f"{settings.data_collector_base_url}/collect/snapshot", timeout=8)
		response.raise_for_status()
		return response.json()
	except requests.RequestException:
		try:
			snapshot = neo4j_client.get_latest_snapshot()
			if snapshot:
				return snapshot
		except Exception:
			pass
		return _fallback_snapshot()


def _row_text(row: dict[str, Any]) -> str:
	parts = []
	for key in ["title", "summary", "source", "severity", "cve_id"]:
		value = row.get(key)
		if isinstance(value, str):
			parts.append(value)
	vendors = row.get("vendors", [])
	if isinstance(vendors, list):
		parts.extend([str(v) for v in vendors])
	cves = row.get("cves", [])
	if isinstance(cves, list):
		parts.extend([str(c) for c in cves])
	vendor_obj = row.get("vendor")
	if isinstance(vendor_obj, dict):
		parts.extend([str(vendor_obj.get("name", "")), str(vendor_obj.get("source", ""))])
	return " ".join(parts).lower()


def _device_keywords(device: DeviceRecord) -> list[str]:
	keywords = [
		device.hostname,
		device.device_type,
		device.platform,
		device.vendor,
		device.product,
		device.version,
		device.identity_provider,
		*device.tags,
	]
	return [keyword.lower().strip() for keyword in keywords if keyword and keyword.strip()]


def _as_text(value: Any) -> str:
	return value.strip().lower() if isinstance(value, str) else ""


def _match_reasons(text: str, keywords: list[str]) -> list[str]:
	matched = [keyword for keyword in keywords if keyword and keyword in text]
	# Keep output compact and deterministic for UI rendering.
	return sorted(set(matched))[:8]


def _impact_for_device(device: DeviceRecord, advisories: list[dict[str, Any]], cves: list[dict[str, Any]]) -> dict[str, Any]:
	keywords = _device_keywords(device)
	matched_advisories = []
	matched_cves = []
	advisory_match_reasons: dict[str, list[str]] = {}
	cve_match_reasons: dict[str, list[str]] = {}

	for advisory in advisories:
		text = _row_text(advisory)
		reasons = _match_reasons(text, keywords)
		if reasons:
			matched_advisories.append(advisory)
			advisory_key = str(advisory.get("title", ""))
			advisory_match_reasons[advisory_key] = reasons

	advisory_cve_ids = {cve_id for advisory in matched_advisories for cve_id in advisory.get("cves", [])}

	for cve in cves:
		text = _row_text(cve)
		reasons = _match_reasons(text, keywords)
		if reasons or cve.get("cve_id") in advisory_cve_ids:
			matched_cves.append(cve)
			cve_key = str(cve.get("cve_id", ""))
			cve_match_reasons[cve_key] = reasons or ["linked-via-advisory"]

	risk_score = min(len(matched_advisories) * 12 + len(matched_cves) * 8, 100)
	risk_level = "low"
	if risk_score >= 65:
		risk_level = "critical"
	elif risk_score >= 40:
		risk_level = "high"
	elif risk_score >= 20:
		risk_level = "medium"

	return {
		"device": device.model_dump(),
		"risk_score": risk_score,
		"risk_level": risk_level,
		"advisory_count": len(matched_advisories),
		"cve_count": len(matched_cves),
		"matched_advisories": matched_advisories[:8],
		"matched_cves": matched_cves[:8],
		"match_reasons": {
			"advisories": advisory_match_reasons,
			"cves": cve_match_reasons,
		},
	}


@app.get("/health")
def health() -> dict[str, str]:
	return {"status": "ok", "service": "api-service"}


@app.get("/api/overview")
def overview(_: str | None = Depends(optional_api_key)) -> dict[str, Any]:
	snapshot = _fetch_snapshot()
	return {"generated_at": snapshot.get("generated_at", ""), "stats": snapshot.get("stats", {})}


@app.get("/api/advisories")
def advisories(
	page: int = Query(default=1, ge=1),
	page_size: int = Query(default=20, ge=1, le=100),
	_: str | None = Depends(optional_api_key),
) -> dict:
	snapshot = _fetch_snapshot()
	return paginate(snapshot.get("advisories", []), page=page, page_size=page_size)


@app.get("/api/cves")
def cves(
	page: int = Query(default=1, ge=1),
	page_size: int = Query(default=20, ge=1, le=100),
	_: str | None = Depends(optional_api_key),
) -> dict:
	snapshot = _fetch_snapshot()
	return paginate(snapshot.get("cves", []), page=page, page_size=page_size)


@app.get("/api/cves/{cve_id}/intel")
def cve_intel(cve_id: str, _: str | None = Depends(optional_api_key)) -> dict[str, Any]:
	_hydrate_devices_from_db()
	snapshot = _fetch_snapshot()
	cves = snapshot.get("cves", [])
	advisories = snapshot.get("advisories", [])

	target = next((cve for cve in cves if str(cve.get("cve_id", "")).upper() == cve_id.upper()), None)
	if not target:
		raise HTTPException(status_code=404, detail="CVE not found")

	related_advisories = [advisory for advisory in advisories if cve_id.upper() in [str(c).upper() for c in advisory.get("cves", [])]]

	impacted_devices = []
	for device in _DEVICE_STORE.values():
		impact = _impact_for_device(device, advisories, cves)
		if any(str(item.get("cve_id", "")).upper() == cve_id.upper() for item in impact.get("matched_cves", [])):
			impacted_devices.append(
				{
					"device": device.model_dump(),
					"risk_score": impact.get("risk_score", 0),
					"risk_level": impact.get("risk_level", "low"),
					"reasons": impact.get("match_reasons", {}).get("cves", {}).get(cve_id, []),
				}
			)

	return {
		"cve": target,
		"related_advisories": related_advisories,
		"impacted_devices": sorted(impacted_devices, key=lambda item: item["risk_score"], reverse=True),
	}


@app.post("/api/devices/push")
def push_devices(payload: DevicePushPayload = Body(...), _: str | None = Depends(optional_api_key)) -> dict[str, Any]:
	accepted = 0
	to_persist: list[dict[str, Any]] = []
	for device in payload.devices:
		_DEVICE_STORE[device.device_id] = device
		to_persist.append(device.model_dump())
		accepted += 1
	if to_persist:
		try:
			neo4j_client.save_devices(to_persist)
		except Exception:
			pass
	return {"accepted": accepted, "total_devices": len(_DEVICE_STORE)}


@app.get("/api/devices")
def list_devices(
	query: str = Query(default=""),
	device_type: str = Query(default=""),
	platform: str = Query(default=""),
	vendor: str = Query(default=""),
	page: int = Query(default=1, ge=1),
	page_size: int = Query(default=20, ge=1, le=100),
	_: str | None = Depends(optional_api_key),
) -> dict[str, Any]:
	_hydrate_devices_from_db()
	q = _as_text(query)
	target_type = _as_text(device_type)
	target_platform = _as_text(platform)
	target_vendor = _as_text(vendor)

	items = []
	for device in _DEVICE_STORE.values():
		haystack = " ".join(_device_keywords(device))
		if q and q not in haystack:
			continue
		if target_type and device.device_type.lower() != target_type:
			continue
		if target_platform and device.platform.lower() != target_platform:
			continue
		if target_vendor and device.vendor.lower() != target_vendor:
			continue
		items.append(device.model_dump())

	return paginate(items, page=page, page_size=page_size)


@app.get("/api/devices/{device_id}")
def get_device(device_id: str, _: str | None = Depends(optional_api_key)) -> dict[str, Any]:
	_hydrate_devices_from_db()
	device = _DEVICE_STORE.get(device_id)
	if not device:
		raise HTTPException(status_code=404, detail="Device not found")
	return device.model_dump()


@app.get("/api/impact/device/{device_id}")
def device_impact(device_id: str, _: str | None = Depends(optional_api_key)) -> dict[str, Any]:
	_hydrate_devices_from_db()
	device = _DEVICE_STORE.get(device_id)
	if not device:
		raise HTTPException(status_code=404, detail="Device not found")
	snapshot = _fetch_snapshot()
	return _impact_for_device(device, snapshot.get("advisories", []), snapshot.get("cves", []))


@app.get("/api/impact/summary")
def impact_summary(_: str | None = Depends(optional_api_key)) -> dict[str, Any]:
	_hydrate_devices_from_db()
	snapshot = _fetch_snapshot()
	advisories = snapshot.get("advisories", [])
	cves = snapshot.get("cves", [])
	impacts = [_impact_for_device(device, advisories, cves) for device in _DEVICE_STORE.values()]
	impacts_sorted = sorted(impacts, key=lambda item: item["risk_score"], reverse=True)
	return {
		"device_count": len(impacts_sorted),
		"critical": sum(1 for item in impacts_sorted if item["risk_level"] == "critical"),
		"high": sum(1 for item in impacts_sorted if item["risk_level"] == "high"),
		"medium": sum(1 for item in impacts_sorted if item["risk_level"] == "medium"),
		"low": sum(1 for item in impacts_sorted if item["risk_level"] == "low"),
		"items": impacts_sorted,
	}


@app.get("/api/changes/entra")
def entra_changes(_: str | None = Depends(optional_api_key)) -> dict[str, Any]:
	snapshot = _fetch_snapshot()
	advisories = snapshot.get("advisories", [])
	changes = [advisory for advisory in advisories if advisory.get("source") == "entra" or "entra" in _row_text(advisory)]
	return {"count": len(changes), "items": changes}

