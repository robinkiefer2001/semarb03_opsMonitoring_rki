from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Settings:
	app_name: str
	docs_url: str


def get_settings() -> Settings:
	return Settings(
		app_name=getenv("DATA_COLLECTOR_APP_NAME", "Data Collector Service"),
		docs_url=getenv("DATA_COLLECTOR_DOCS_URL", "/doc"),
	)

