from app.schemas.internal.cve import CVE


def map_cve(cve_id: str, source: str, severity: str, vendor_name: str) -> CVE:
	return CVE(
		cve_id=cve_id,
		source=source,
		severity=severity,
		score=None,
		description="",
		vendors=[vendor_name],
	)

