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

	def _run(self, query: str, params: dict[str, Any]) -> None:
		if not self.enabled:
			return
		assert self._driver is not None
		with self._driver.session(database=settings.neo4j_database) as session:
			session.run(query, params)

	def save_snapshot(self, snapshot: dict[str, Any]) -> None:
		if not self.enabled:
			return

		advisories = snapshot.get("advisories", [])
		cves = snapshot.get("cves", [])
		generated_at = str(snapshot.get("generated_at", ""))

		self._run(
			"""
			MERGE (s:Snapshot {generated_at: $generated_at})
			SET s.updated_at = datetime()
			""",
			{"generated_at": generated_at},
		)

		for advisory in advisories:
			advisory_params = {
				"id": f"{advisory.get('source', 'unknown')}::{advisory.get('title', 'untitled')}",
				"source": advisory.get("source", ""),
				"title": advisory.get("title", ""),
				"summary": advisory.get("summary", ""),
				"url": advisory.get("url", ""),
				"published_at": advisory.get("published_at", ""),
				"severity": advisory.get("severity", "unknown"),
				"generated_at": generated_at,
				"vendor_name": advisory.get("vendor", {}).get("name", "unknown"),
			}
			self._run(
				"""
				MERGE (a:Advisory {id: $id})
				SET a.source = $source,
				    a.title = $title,
				    a.summary = $summary,
				    a.url = $url,
				    a.published_at = $published_at,
				    a.severity = $severity,
				    a.generated_at = $generated_at,
				    a.updated_at = datetime()
				MERGE (v:Vendor {name: $vendor_name})
				MERGE (v)-[:PUBLISHED]->(a)
				""",
				advisory_params,
			)

			for cve_id in advisory.get("cves", []):
				self._run(
					"""
					MERGE (c:CVE {cve_id: $cve_id})
					ON CREATE SET c.created_at = datetime()
					SET c.updated_at = datetime()
					WITH c
					MATCH (a:Advisory {id: $advisory_id})
					MERGE (a)-[:REFERENCES]->(c)
					""",
					{
						"cve_id": cve_id,
						"advisory_id": advisory_params["id"],
					},
				)

		for cve in cves:
			cve_params = {
				"cve_id": cve.get("cve_id", ""),
				"source": cve.get("source", ""),
				"severity": cve.get("severity", "unknown"),
				"score": cve.get("score"),
				"description": cve.get("description", ""),
			}
			self._run(
				"""
				MERGE (c:CVE {cve_id: $cve_id})
				SET c.source = $source,
				    c.severity = $severity,
				    c.score = $score,
				    c.description = $description,
				    c.updated_at = datetime()
				""",
				cve_params,
			)

			for vendor in cve.get("vendors", []):
				self._run(
					"""
					MERGE (v:Vendor {name: $vendor})
					WITH v
					MATCH (c:CVE {cve_id: $cve_id})
					MERGE (v)-[:AFFECTED_BY]->(c)
					""",
					{"vendor": vendor, "cve_id": cve_params["cve_id"]},
				)


neo4j_client = Neo4jClient()
