import re

from app.schemas.internal.cve import CVE


def _canonical_cve_id(cve_id: str) -> str:
	value = cve_id.strip().upper()
	match = re.fullmatch(r"CVE-(\d{4})-(\d{4,7})", value)
	if not match:
		return ""
	return f"CVE-{match.group(1)}-{match.group(2)}"


def normalize_cve(cve: CVE) -> CVE:
	cve.cve_id = _canonical_cve_id(cve.cve_id)
	cve.source = cve.source.strip().lower()
	cve.severity = cve.severity.lower().strip() or "unknown"
	cve.description = cve.description.strip()
	cve.vendors = sorted({v.strip() for v in cve.vendors if v.strip()})
	return cve

