from app.schemas.internal.advisory import Advisory
from app.schemas.internal.vendor import Vendor


def map_advisory(raw: dict) -> Advisory:
	vendor = Vendor(name=str(raw.get("vendor", "unknown")), source=str(raw.get("source", "unknown")))
	return Advisory(
		source=str(raw.get("source", "unknown")),
		vendor=vendor,
		title=str(raw.get("title", "Untitled Advisory")),
		summary=str(raw.get("summary", "")),
		url=str(raw.get("url", "")),
		published_at=str(raw.get("published", "")),
		severity=str(raw.get("severity", "unknown")),
		cves=[str(cve) for cve in raw.get("cves", [])],
	)

