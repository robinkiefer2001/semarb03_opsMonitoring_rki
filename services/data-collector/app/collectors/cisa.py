from __future__ import annotations

from typing import Any

from app.collectors.base import BaseCollector
from app.utils.http_utils import get_json


class CISACollector(BaseCollector):
    source = "cisa"
    _endpoint = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

    def collect(self, limit: int = 100) -> list[dict[str, Any]]:
        payload = get_json(self._endpoint)
        vulnerabilities = []
        if isinstance(payload, dict):
            vulnerabilities = payload.get("vulnerabilities", [])

        if not vulnerabilities:
            return []

        records: list[dict[str, Any]] = []
        for item in vulnerabilities[:limit]:
            cve_id = str(item.get("cveID", "")).strip()
            records.append(
                {
                    "source": self.source,
                    "vendor": "CISA",
                    "title": item.get("vulnerabilityName", cve_id or "CISA Advisory"),
                    "summary": item.get("shortDescription", ""),
                    "url": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
                    "published": item.get("dateAdded", ""),
                    "severity": "critical",
                    "cves": [cve_id] if cve_id else [],
                }
            )
        return records
