from __future__ import annotations

from typing import Any

from app.collectors.base import BaseCollector


class CiscoCollector(BaseCollector):
	source = "cisco"

	def collect(self, limit: int = 10) -> list[dict[str, Any]]:
		# Cisco PSIRT often requires API credentials.
		return [
			{
				"source": self.source,
				"vendor": "Cisco",
				"title": "Cisco PSIRT Placeholder Advisory",
				"summary": "Konfiguriere API-Key fuer produktive Abfragen.",
				"url": "https://sec.cloudapps.cisco.com/security/center/publicationListing.x",
				"published": "",
				"severity": "high",
				"cves": [],
			}
		][:limit]

