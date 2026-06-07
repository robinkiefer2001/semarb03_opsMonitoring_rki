from app.schemas.internal.update import Update


def normalize_update(update: Update) -> Update:
	update.update_id = update.update_id.strip()
	update.title = update.title.strip()
	update.product = update.product.strip()
	update.severity = update.severity.lower().strip() or "unknown"
	return update

