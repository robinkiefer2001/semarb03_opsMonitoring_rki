import re

from app.schemas.internal.advisory import Advisory


_SEVERITY_MAP = {
	"critical": "critical",
	"crit": "critical",
	"high": "high",
	"important": "high",
	"medium": "medium",
	"moderate": "medium",
	"low": "low",
	"unknown": "unknown",
	"none": "unknown",
}


def _normalize_severity(severity: str) -> str:
	key = (severity or "").strip().lower()
	return _SEVERITY_MAP.get(key, "unknown")


def _extract_cves(text: str) -> list[str]:
	return sorted(set(match.upper() for match in re.findall(r"CVE-\d{4}-\d{4,7}", text, flags=re.IGNORECASE)))


def normalize_advisory(advisory: Advisory) -> Advisory:
	advisory.source = advisory.source.strip().lower() or "unknown"
	advisory.vendor.name = advisory.vendor.name.strip() or "unknown"
	advisory.vendor.source = advisory.vendor.source.strip().lower() or advisory.source
	advisory.title = advisory.title.strip()
	advisory.summary = advisory.summary.strip()
	advisory.severity = _normalize_severity(advisory.severity)

	normalized_cves = sorted({cve.strip().upper() for cve in advisory.cves if cve.strip()})
	if not normalized_cves:
		normalized_cves = _extract_cves(f"{advisory.title} {advisory.summary}")
	advisory.cves = normalized_cves
	return advisory

