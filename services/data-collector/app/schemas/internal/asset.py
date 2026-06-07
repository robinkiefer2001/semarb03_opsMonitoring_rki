from pydantic import BaseModel, Field


class Asset(BaseModel):
	asset_id: str = Field(..., min_length=1)
	hostname: str = ""
	vendor: str = ""
	product: str = ""
	version: str = ""
	environment: str = "prod"

