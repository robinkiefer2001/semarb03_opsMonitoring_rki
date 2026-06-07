from pydantic import BaseModel, Field


class Update(BaseModel):
	update_id: str = Field(..., min_length=1)
	title: str = ""
	product: str = ""
	release_date: str = ""
	severity: str = "unknown"

