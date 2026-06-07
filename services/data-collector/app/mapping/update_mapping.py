from app.schemas.internal.update import Update


def map_update(raw: dict) -> Update:
	return Update(
		update_id=str(raw.get("update_id", "update-unknown")),
		title=str(raw.get("title", "")),
		product=str(raw.get("product", "")),
		release_date=str(raw.get("release_date", "")),
		severity=str(raw.get("severity", "unknown")),
	)

