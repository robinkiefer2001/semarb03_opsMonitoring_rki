from app.schemas.internal.asset import Asset


def map_asset(raw: dict) -> Asset:
	return Asset(
		asset_id=str(raw.get("asset_id", "asset-unknown")),
		hostname=str(raw.get("hostname", "")),
		vendor=str(raw.get("vendor", "")),
		product=str(raw.get("product", "")),
		version=str(raw.get("version", "")),
		environment=str(raw.get("environment", "prod")),
	)

