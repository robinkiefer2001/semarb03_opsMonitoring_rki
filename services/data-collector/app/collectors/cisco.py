from __future__ import annotations

from typing import Any

from app.collectors.base import BaseCollector
from app.utils.http_utils import get_json


class CiscoCollector(BaseCollector):
	source = "cisco"
	_endpoint = "https://api.cisco.com/security/advisories/all.json"

	def collect(self, limit: int = 10) -> list[dict[str, Any]]:
		payload = get_json(self._endpoint)
		items: list[dict[str, Any]] = []

		if isinstance(payload, dict):
			items = payload.get("advisories", [])

		if not items:
			return []

		records: list[dict[str, Any]] = []
		for item in items[:limit]:
			records.append(
				{
					"source": self.source,
					"vendor": "Cisco",
					"title": item.get("advisoryTitle", "Cisco Advisory"),
					"summary": item.get("sir", ""),
					"url": item.get("advisoryUrl", "https://sec.cloudapps.cisco.com/security/center/publicationListing.x"),
					"published": item.get("publicationUrl", ""),
					"severity": item.get("sir", "high"),
					"cves": item.get("cves", []),
				}
			)
		return records

