from pydantic import BaseModel, Field


class Vendor(BaseModel):
	name: str = Field(..., min_length=1)
	source: str = Field(..., min_length=1)

