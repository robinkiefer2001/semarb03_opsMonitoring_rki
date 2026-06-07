from pydantic import BaseModel, Field


class ServiceChange(BaseModel):
	service_name: str = Field(..., min_length=1)
	change_type: str = Field(..., min_length=1)
	detected_at: str = ""
	details: str = ""

