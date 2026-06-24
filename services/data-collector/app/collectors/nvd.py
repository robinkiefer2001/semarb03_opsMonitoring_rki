from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
	project_root = Path(__file__).resolve().parents[2]
	if str(project_root) not in sys.path:
		sys.path.insert(0, str(project_root))

from app.collectors.base import BaseCollector
from app.utils.http_utils import get_json


class NVDCollector(BaseCollector):
	source = "nvd"
	_endpoint = "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=5"

	@staticmethod
	def _severity_from_metrics(metrics: dict[str, Any]) -> str:
		for key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
			items = metrics.get(key, [])
			if not items:
				continue
			base = items[0].get("cvssData", {})
			severity = str(base.get("baseSeverity", "")).lower().strip()
			if severity:
				return severity
		return "high"

	def collect(self, limit: int = 100) -> list[dict[str, Any]]:
		payload = get_json(self._endpoint)
		vulnerabilities = []
		if isinstance(payload, dict):
			vulnerabilities = payload.get("vulnerabilities", [])


		if not vulnerabilities:
			return []

		records: list[dict[str, Any]] = []
		for item in vulnerabilities[:limit]:
			cve = item.get("cve", {})
			severity = self._severity_from_metrics(cve.get("metrics", {}))
			cve_id = cve.get("id", "")
			descriptions = cve.get("descriptions", [])
			summary = ""
			if descriptions:
				summary = descriptions[0].get("value", "")

			records.append(
				{
					"source": self.source,
					"vendor": "NVD",
					"title": cve_id or "NVD CVE",
					"summary": summary,
					"url": f"https://nvd.nist.gov/vuln/detail/{cve_id}" if cve_id else "https://nvd.nist.gov",
					"published": cve.get("published", ""),
					"severity": severity,
					"cves": [cve_id] if cve_id else [],
				}
			)

		return records