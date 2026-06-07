from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any

import requests

from app.collectors.base import BaseCollector

try:
	import feedparser
except ModuleNotFoundError:
	feedparser = None


class BSICollector(BaseCollector):
	source = "bsi"
	_rss_url = "https://wid.cert-bund.de/portal/wid/rss"

	def _fallback_parse_rss(self, limit: int) -> list[dict[str, Any]]:
		try:
			response = requests.get(self._rss_url, timeout=8)
			response.raise_for_status()
			root = ET.fromstring(response.text)
		except (requests.RequestException, ET.ParseError):
			return []

		records: list[dict[str, Any]] = []
		for item in root.findall("./channel/item")[:limit]:
			records.append(
				{
					"source": self.source,
					"vendor": "BSI",
					"title": (item.findtext("title") or "BSI Advisory"),
					"summary": (item.findtext("description") or ""),
					"url": (item.findtext("link") or ""),
					"published": (item.findtext("pubDate") or ""),
					"severity": "medium",
					"cves": [],
				}
			)

		return records

	def collect(self, limit: int = 10) -> list[dict[str, Any]]:
		entries = []
		if feedparser is not None:
			feed = feedparser.parse(self._rss_url)
			entries = feed.entries[:limit] if hasattr(feed, "entries") else []

		if not entries:
			return self._fallback_parse_rss(limit) or [
				{
					"source": self.source,
					"vendor": "BSI",
					"title": "BSI Feed derzeit nicht erreichbar",
					"summary": "Fallback-Eintrag fuer lokale Entwicklung.",
					"url": "https://www.bsi.bund.de",
					"published": "",
					"severity": "medium",
					"cves": [],
				}
			]

		normalized: list[dict[str, Any]] = []
		for entry in entries:
			normalized.append(
				{
					"source": self.source,
					"vendor": "BSI",
					"title": entry.get("title", "BSI Advisory"),
					"summary": entry.get("summary", ""),
					"url": entry.get("link", ""),
					"published": entry.get("published", ""),
					"severity": "medium",
					"cves": [],
				}
			)

		return normalized



