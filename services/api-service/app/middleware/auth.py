from fastapi import Header, HTTPException


def optional_api_key(x_api_key: str | None = Header(default=None)) -> str | None:
	# Placeholder: keep endpoint open when no key is configured.
	if x_api_key is not None and not x_api_key.strip():
		raise HTTPException(status_code=401, detail="Invalid API key")
	return x_api_key

