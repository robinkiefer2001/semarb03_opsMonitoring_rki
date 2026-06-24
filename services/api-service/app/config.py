from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Settings:
	app_name: str
	docs_url: str
	data_collector_base_url: str
	neo4j_uri: str
	neo4j_user: str
	neo4j_password: str
	neo4j_database: str


def get_settings() -> Settings:
	return Settings(
		app_name=getenv("API_SERVICE_APP_NAME", "Ops API Service"),
		docs_url=getenv("API_SERVICE_DOCS_URL", "/doc"),
		data_collector_base_url=getenv("DATA_COLLECTOR_BASE_URL", "http://localhost:8001"),
		neo4j_uri=getenv("NEO4J_URI", "bolt://localhost:7687"),
		neo4j_user=getenv("NEO4J_USER", "neo4j"),
		neo4j_password=getenv("NEO4J_PASSWORD", "changeme123"),
		neo4j_database=getenv("NEO4J_DATABASE", "neo4j"),
	)

