from __future__ import annotations

from typing import Any

import requests


def get_json(url: str, timeout_seconds: int = 8) -> dict[str, Any] | list[Any] | None:
	try:
		response = requests.get(url, timeout=timeout_seconds)
		response.raise_for_status()
		return response.json()
	except requests.RequestException:
		return None

