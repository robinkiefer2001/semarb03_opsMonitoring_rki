from __future__ import annotations

from typing import Any

from app.collectors.base import BaseCollector


class MicrosoftCollector(BaseCollector):
	source = "microsoft"

	def collect(self, limit: int = 10) -> list[dict[str, Any]]:
		return [
			{
				"source": self.source,
				"vendor": "Microsoft",
				"title": "MSRC Placeholder Advisory",
				"summary": "MSRC Feed kann spaeter mit Auth angebunden werden.",
				"url": "https://msrc.microsoft.com/update-guide",
				"published": "",
				"severity": "critical",
				"cves": [],
			},
			{
				"source": "entra",
				"vendor": "Microsoft Entra",
				"title": "Conditional Access Policy Change",
				"summary": "Aenderung an Entra Conditional Access erkannt (Placeholder Event).",
				"url": "https://entra.microsoft.com",
				"published": "",
				"severity": "medium",
				"cves": [],
			},
		][:limit]

