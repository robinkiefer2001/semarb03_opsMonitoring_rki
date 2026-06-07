from app.schemas.internal.advisory import Advisory


def normalize_advisory(advisory: Advisory) -> Advisory:
	advisory.title = advisory.title.strip()
	advisory.summary = advisory.summary.strip()
	advisory.severity = advisory.severity.lower().strip() or "unknown"
	advisory.cves = sorted({cve.strip().upper() for cve in advisory.cves if cve.strip()})
	return advisory

