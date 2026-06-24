from __future__ import annotations

from typing import Any

from app.collectors.base import BaseCollector
from app.utils.http_utils import get_json


class MicrosoftCollector(BaseCollector):
	source = "microsoft"
	_endpoint = "https://api.msrc.microsoft.com/cvrf/v3.0/updates"

	def collect(self, limit: int = 100) -> list[dict[str, Any]]:
		payload = get_json(self._endpoint)
		value = payload.get("value", []) if isinstance(payload, dict) else []

		records: list[dict[str, Any]] = []
		for item in value[:limit]:
			records.append(
				{
					"source": self.source,
					"vendor": "Microsoft",
					"title": item.get("Alias", "MSRC advisory"),
					"summary": item.get("DocumentTitle", ""),
					"url": f"https://msrc.microsoft.com/update-guide/en-US/advisory/{item.get('ID', '')}",
					"published": item.get("CurrentReleaseDate", ""),
					"severity": "high",
					"cves": [],
				}
			)

		return records

