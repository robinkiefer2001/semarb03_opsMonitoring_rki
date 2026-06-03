# OpsMonitoring RKI

![Project Status](https://img.shields.io/badge/status-in%20progress-yellow)


## Dokumentation
| Datei | Beschreibung |
|-------|-------------|
| [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) | Projektübersicht, Ziele, User Stories, Struktur |
| [docs/projectworkbook.md](docs/projectworkbook.md) | Sprint-Dokumentation, User Stories & Tasks (hierarchisch) |
| [docs/risikotabelle.md](docs/risikotabelle.md) | Risikotabelle |

## Quick Start
```bash
# Backend starten
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Webapp starten
cd ../webapp
python app.py

# Infrastruktur (Docker Compose)
cd ../infrastructure
docker-compose up -d
```

## Repository-Struktur
```
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── api_clients/
│   └── requirements.txt
├── webapp/
│   └── app.py
├── infrastructure/
│   ├── docker-compose.yml
│   ├── Dockerfile.backend
│   └── Dockerfile.webapp
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── projectworkbook.md
│   └── risikotabelle.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
└── README.md
```

## Technologie-Stack
| Komponente | Technologie | Beschreibung |
|------------|-------------|--------------|
| Backend    | FastAPI     | Python Web-API |
| Datenbank  | Neo4J       | Graphdatenbank |
| Frontend   | FastAPI | Webapp & API |
| Webserver  | NGINX   | Statisches Web, Serving |
| Infrastruktur | Docker, Docker Compose | Containerisierung |
| Reverse Proxy | Traefik | Routing & SSL Management |
| CI/CD      | GitHub Actions | Automatisiertes Deployment |
| Cloud      | Hetzner Cloud | Hosting |

## Projekt-Status
| Sprint | Zeitraum | Status |
|--------|----------|--------|
| Sprint 0 | Initialisierung | Geplant |
| Sprint 1 | Infrastruktur & IaC | Geplant |
| Sprint 2 | Backend & Webapp | Geplant |
| Sprint 3 | API-Anbindungen & Testing | Geplant |

## Projektmanagement
Das Projektmanagement erfolgt nach dem Muster:
- Sprint (Phase) → User Story → Task
Siehe [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) und [docs/projectworkbook.md](docs/projectworkbook.md) für Details zur Hierarchie und Zuordnung.

## Features
- Monitoring-Portal für Security Advisories
- CVE-Tracking (mehrere Hersteller)
- Containerisierte Microservices
- Webzugriff & Datenvisualisierung
- Automatisiertes Deployment (IaC, CI/CD)

## Architektur (ASCII)
```
+-------------------+      +-------------------+
|    Webapp         |<---->|   FastAPI Backend |
+-------------------+      +-------------------+
	   |                        |
	   v                        v
   [User/Browser]           +-----------+
				    |  Neo4J DB |
				    +-----------+
```

## Development
1. Repo clonen & Python-Umgebung einrichten
2. Abhängigkeiten installieren (`pip install -r requirements.txt`)
3. Backend & Webapp lokal starten
4. Infrastruktur via Docker Compose testen

## Deployment
- CI/CD Pipeline via GitHub Actions
- Automatisiertes Deployment auf Hetzner Cloud
- Secrets & Umgebungsvariablen via GitHub Secrets