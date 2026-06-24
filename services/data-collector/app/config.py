from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Settings:
	app_name: str
	docs_url: str
	neo4j_uri: str
	neo4j_user: str
	neo4j_password: str
	neo4j_database: str


def get_settings() -> Settings:
	return Settings(
		app_name=getenv("DATA_COLLECTOR_APP_NAME", "Data Collector Service"),
		docs_url=getenv("DATA_COLLECTOR_DOCS_URL", "/doc"),
		neo4j_uri=getenv("NEO4J_URI", "bolt://localhost:7687"),
		neo4j_user=getenv("NEO4J_USER", "neo4j"),
		neo4j_password=getenv("NEO4J_PASSWORD", "changeme123"),
		neo4j_database=getenv("NEO4J_DATABASE", "neo4j"),
	)

