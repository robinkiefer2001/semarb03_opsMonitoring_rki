from app.schemas.internal.service import Service


def normalize_service(service: Service) -> Service:
	service.name = service.name.strip()
	service.owner = service.owner.strip()
	service.criticality = service.criticality.lower().strip() or "medium"
	service.status = service.status.lower().strip() or "unknown"
	return service

