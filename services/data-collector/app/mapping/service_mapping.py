from app.schemas.internal.service import Service


def map_service(raw: dict) -> Service:
	return Service(
		name=str(raw.get("name", "unknown-service")),
		owner=str(raw.get("owner", "")),
		criticality=str(raw.get("criticality", "medium")),
		status=str(raw.get("status", "unknown")),
	)

