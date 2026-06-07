from app.schemas.internal.cve import CVE


def normalize_cve(cve: CVE) -> CVE:
	cve.cve_id = cve.cve_id.strip().upper()
	cve.severity = cve.severity.lower().strip() or "unknown"
	cve.vendors = sorted({v.strip() for v in cve.vendors if v.strip()})
	return cve

