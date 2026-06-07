def paginate(items: list, page: int = 1, page_size: int = 20) -> dict:
	page = max(page, 1)
	page_size = max(min(page_size, 100), 1)
	start = (page - 1) * page_size
	end = start + page_size
	return {
		"page": page,
		"page_size": page_size,
		"total": len(items),
		"items": items[start:end],
	}

