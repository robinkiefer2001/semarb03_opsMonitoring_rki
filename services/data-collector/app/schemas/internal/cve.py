from pydantic import BaseModel, Field


class CVE(BaseModel):
	cve_id: str = Field(..., min_length=1)
	source: str = ""
	severity: str = "unknown"
	score: float | None = None
	description: str = ""
	vendors: list[str] = Field(default_factory=list)

