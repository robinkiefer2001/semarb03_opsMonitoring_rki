from pydantic import BaseModel, Field


class Service(BaseModel):
	name: str = Field(..., min_length=1)
	owner: str = ""
	criticality: str = "medium"
	status: str = "unknown"

