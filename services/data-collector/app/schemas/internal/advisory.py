from pydantic import BaseModel, Field

from app.schemas.internal.vendor import Vendor


class Advisory(BaseModel):
	source: str = Field(..., min_length=1)
	vendor: Vendor
	title: str = Field(..., min_length=1)
	summary: str = ""
	url: str = ""
	published_at: str = ""
	severity: str = "unknown"
	cves: list[str] = Field(default_factory=list)

