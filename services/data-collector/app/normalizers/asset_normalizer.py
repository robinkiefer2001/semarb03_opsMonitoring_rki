from app.schemas.internal.asset import Asset


def normalize_asset(asset: Asset) -> Asset:
	asset.asset_id = asset.asset_id.strip()
	asset.hostname = asset.hostname.strip().lower()
	asset.vendor = asset.vendor.strip()
	asset.product = asset.product.strip()
	asset.version = asset.version.strip()
	return asset

