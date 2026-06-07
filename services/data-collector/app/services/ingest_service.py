from __future__ import annotations

from app.collectors.bsi import BSICollector
from app.collectors.cisa import CISACollector
from app.collectors.cisco import CiscoCollector
from app.collectors.github import GitHubAdvisoryCollector
from app.collectors.microsoft import MicrosoftCollector
from app.collectors.nvd import NVDCollector
from app.mapping.advisory_mapping import map_advisory
from app.mapping.cve_mapping import map_cve
from app.normalizers.advisory_normalizer import normalize_advisory
from app.normalizers.cve_normalizer import normalize_cve
from app.utils.date_utils import utc_now_iso

_LAST_SNAPSHOT: dict | None = None


def _build_collectors() -> list:
	return [BSICollector(), NVDCollector(), CISACollector(), CiscoCollector(), GitHubAdvisoryCollector(), MicrosoftCollector()]


def collect_and_normalize(limit_per_source: int = 10) -> dict:
	advisories = []
	cves = []

	for collector in _build_collectors():
		raw_items = collector.collect(limit=limit_per_source)
		for raw in raw_items:
			advisory = normalize_advisory(map_advisory(raw))
			advisories.append(advisory)
			for cve_id in advisory.cves:
				cve = normalize_cve(
					map_cve(
						cve_id=cve_id,
						source=advisory.source,
						severity=advisory.severity,
						vendor_name=advisory.vendor.name,
					)
				)
				cves.append(cve)

	unique_cves = {c.cve_id: c for c in cves}.values()
	snapshot = {
		"generated_at": utc_now_iso(),
		"stats": {
			"advisory_count": len(advisories),
			"cve_count": len(unique_cves),
			"sources": sorted({a.source for a in advisories}),
		},
		"advisories": [a.model_dump() for a in advisories],
		"cves": [c.model_dump() for c in unique_cves],
	}

	global _LAST_SNAPSHOT
	_LAST_SNAPSHOT = snapshot
	return snapshot


def get_latest_snapshot() -> dict:
	if _LAST_SNAPSHOT is None:
		return collect_and_normalize()
	return _LAST_SNAPSHOT

