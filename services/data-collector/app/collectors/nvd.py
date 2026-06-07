from __future__ import annotations

from typing import Any

from app.collectors.base import BaseCollector
from app.utils.http_utils import get_json


class NVDCollector(BaseCollector):
	source = "nvd"
	_endpoint = "https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=5"

	def collect(self, limit: int = 10) -> list[dict[str, Any]]:
		payload = get_json(self._endpoint)
		vulnerabilities = []
		if isinstance(payload, dict):
			vulnerabilities = payload.get("vulnerabilities", [])

		if not vulnerabilities:
			return [
				{
					"source": self.source,
					"vendor": "NVD",
					"title": "NVD API nicht erreichbar",
					"summary": "Fallback-Eintrag fuer lokale Entwicklung.",
					"url": "https://nvd.nist.gov",
					"published": "",
					"severity": "high",
					"cves": [],
				}
			]

		records: list[dict[str, Any]] = []
		for item in vulnerabilities[:limit]:
			cve = item.get("cve", {})
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
					"severity": "high",
					"cves": [cve_id] if cve_id else [],
				}
			)

		return records

