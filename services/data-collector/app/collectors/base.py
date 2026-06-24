from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseCollector(ABC):
	source: str

	@abstractmethod
	def collect(self, limit: int = 100) -> list[dict[str, Any]]:
		raise NotImplementedError

