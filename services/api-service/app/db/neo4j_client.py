from __future__ import annotations

from typing import Any

from neo4j import GraphDatabase

from app.config import get_settings

settings = get_settings()


class Neo4jClient:
	def __init__(self) -> None:
		self._enabled = bool(settings.neo4j_uri and settings.neo4j_password)
		self._driver = None
		if self._enabled:
			self._driver = GraphDatabase.driver(
				settings.neo4j_uri,
				auth=(settings.neo4j_user, settings.neo4j_password),
			)

	@property
	def enabled(self) -> bool:
		return self._enabled and self._driver is not None

	def close(self) -> None:
		if self._driver is not None:
			self._driver.close()

	def _run_read(self, query: str, params: dict[str, Any]) -> list[dict[str, Any]]:
		if not self.enabled:
			return []
		assert self._driver is not None
		with self._driver.session(database=settings.neo4j_database) as session:
			result = session.run(query, params)
			return [record.data() for record in result]

	def _run_write(self, query: str, params: dict[str, Any]) -> None:
		if not self.enabled:
			return
		assert self._driver is not None
		with self._driver.session(database=settings.neo4j_database) as session:
			session.run(query, params)

	def get_latest_snapshot(self) -> dict[str, Any] | None:
		if not self.enabled:
			return None

		stats_rows = self._run_read(
			"""
			MATCH (a:Advisory)
			WITH count(a) AS advisory_count, collect(DISTINCT a.source) AS sources
			MATCH (c:CVE)
			RETURN advisory_count, size(collect(c)) AS cve_count, sources
			""",
			{},
		)

		advisory_rows = self._run_read(
			"""
			MATCH (a:Advisory)
			OPTIONAL MATCH (v:Vendor)-[:PUBLISHED]->(a)
			OPTIONAL MATCH (a)-[:REFERENCES]->(c:CVE)
			RETURN a.source AS source,
			       coalesce(v.name, 'unknown') AS vendor_name,
			       a.title AS title,
			       a.summary AS summary,
			       a.url AS url,
			       a.published_at AS published_at,
			       a.severity AS severity,
			       collect(DISTINCT c.cve_id) AS cves
			ORDER BY a.updated_at DESC
			LIMIT 300
			""",
			{},
		)

		cve_rows = self._run_read(
			"""
			MATCH (c:CVE)
			OPTIONAL MATCH (v:Vendor)-[:AFFECTED_BY]->(c)
			RETURN c.cve_id AS cve_id,
			       c.source AS source,
			       c.severity AS severity,
			       c.score AS score,
			       c.description AS description,
			       collect(DISTINCT v.name) AS vendors
			ORDER BY c.updated_at DESC
			LIMIT 600
			""",
			{},
		)

		if not advisory_rows and not cve_rows:
			return None

		stats = stats_rows[0] if stats_rows else {"advisory_count": len(advisory_rows), "cve_count": len(cve_rows), "sources": []}

		advisories = [
			{
				"source": row.get("source") or "unknown",
				"vendor": {"name": row.get("vendor_name") or "unknown", "source": row.get("source") or "unknown"},
				"title": row.get("title") or "",
				"summary": row.get("summary") or "",
				"url": row.get("url") or "",
				"published_at": row.get("published_at") or "",
				"severity": row.get("severity") or "unknown",
				"cves": [c for c in (row.get("cves") or []) if c],
			}
			for row in advisory_rows
		]

		cves = [
			{
				"cve_id": row.get("cve_id") or "",
				"source": row.get("source") or "",
				"severity": row.get("severity") or "unknown",
				"score": row.get("score"),
				"description": row.get("description") or "",
				"vendors": [v for v in (row.get("vendors") or []) if v],
			}
			for row in cve_rows
		]

		return {
			"generated_at": "",
			"stats": {
				"advisory_count": int(stats.get("advisory_count", len(advisories))),
				"cve_count": int(stats.get("cve_count", len(cves))),
				"sources": sorted(set(stats.get("sources") or [])),
			},
			"advisories": advisories,
			"cves": cves,
		}

	def save_devices(self, devices: list[dict[str, Any]]) -> None:
		for device in devices:
			self._run_write(
				"""
				MERGE (d:Device {device_id: $device_id})
				SET d.hostname = $hostname,
				    d.device_type = $device_type,
				    d.platform = $platform,
				    d.vendor = $vendor,
				    d.product = $product,
				    d.version = $version,
				    d.business_unit = $business_unit,
				    d.owner = $owner,
				    d.identity_provider = $identity_provider,
				    d.tags = $tags,
				    d.updated_at = datetime()
				""",
				{
					"device_id": device.get("device_id", ""),
					"hostname": device.get("hostname", ""),
					"device_type": device.get("device_type", ""),
					"platform": device.get("platform", ""),
					"vendor": device.get("vendor", ""),
					"product": device.get("product", ""),
					"version": device.get("version", ""),
					"business_unit": device.get("business_unit", ""),
					"owner": device.get("owner", ""),
					"identity_provider": device.get("identity_provider", ""),
					"tags": device.get("tags", []),
				},
			)

	def load_devices(self) -> list[dict[str, Any]]:
		rows = self._run_read(
			"""
			MATCH (d:Device)
			RETURN d.device_id AS device_id,
			       d.hostname AS hostname,
			       d.device_type AS device_type,
			       d.platform AS platform,
			       d.vendor AS vendor,
			       d.product AS product,
			       d.version AS version,
			       d.business_unit AS business_unit,
			       d.owner AS owner,
			       d.identity_provider AS identity_provider,
			       coalesce(d.tags, []) AS tags
			""",
			{},
		)
		return rows


neo4j_client = Neo4jClient()
