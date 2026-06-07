from __future__ import annotations

from typing import Any

from app.collectors.base import BaseCollector
from app.utils.http_utils import get_json


class GitHubAdvisoryCollector(BaseCollector):
    source = "github"
    _endpoint = "https://api.github.com/advisories?per_page=5"

    def collect(self, limit: int = 10) -> list[dict[str, Any]]:
        payload = get_json(self._endpoint)
        advisories = payload if isinstance(payload, list) else []

        if not advisories:
            return [
                {
                    "source": self.source,
                    "vendor": "GitHub",
                    "title": "GitHub Advisory Placeholder",
                    "summary": "GitHub Advisory API aktuell nicht erreichbar.",
                    "url": "https://github.com/advisories",
                    "published": "",
                    "severity": "high",
                    "cves": [],
                }
            ][:limit]

        records: list[dict[str, Any]] = []
        for item in advisories[:limit]:
            cve_id = str(item.get("cve_id", "")).strip()
            records.append(
                {
                    "source": self.source,
                    "vendor": "GitHub",
                    "title": item.get("summary", "GitHub Advisory"),
                    "summary": item.get("description", ""),
                    "url": item.get("html_url", "https://github.com/advisories"),
                    "published": item.get("published_at", ""),
                    "severity": str(item.get("severity", "high") or "high"),
                    "cves": [cve_id] if cve_id else [],
                }
            )
        return records
