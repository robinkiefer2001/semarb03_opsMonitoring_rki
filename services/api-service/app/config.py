from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Settings:
	app_name: str
	docs_url: str
	data_collector_base_url: str


def get_settings() -> Settings:
	return Settings(
		app_name=getenv("API_SERVICE_APP_NAME", "Ops API Service"),
		docs_url=getenv("API_SERVICE_DOCS_URL", "/doc"),
		data_collector_base_url=getenv("DATA_COLLECTOR_BASE_URL", "http://localhost:8001"),
	)

