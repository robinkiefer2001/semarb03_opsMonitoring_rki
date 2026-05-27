# OpsMonitoring RKI

![Project Status](https://img.shields.io/badge/status-in%20progress-yellow)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![CI/CD](https://img.shields.io/badge/ci%2Fcd-gitlab-orange)

## Dokumentation
| Datei | Beschreibung |
|-------|-------------|
| [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) | Projektübersicht & Ziele |
| [docs/projectworkbook.md](docs/projectworkbook.md) | Sprint-Dokumentation |
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
├── .gitlab-ci.yml
├── .gitignore
└── README.md
```

## Technologie-Stack
| Komponente | Technologie | Beschreibung |
|------------|-------------|--------------|
| Backend    | FastAPI     | Python Web-API |
| Datenbank  | Neo4J       | Graphdatenbank |
| Frontend   | Python (tkinter/streamlit) | Webapp |
| Infrastruktur | Docker, Docker Compose | Containerisierung |
| Reverse Proxy | Traefik | Routing & SSL Management |
| CI/CD      | GitLab CI/CD | Automatisiertes Deployment |
| Cloud      | Hetzner Cloud | Hosting |

## Projekt-Status
| Sprint | Zeitraum | Status |
|--------|----------|--------|
| Sprint 0 | Initialisierung | Geplant |
| Sprint 1 | Infrastruktur & IaC | Geplant |
| Sprint 2 | Backend & Webapp | Geplant |
| Sprint 3 | API-Anbindungen & Testing | Geplant |

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
- CI/CD Pipeline via GitLab
- Automatisiertes Deployment auf Hetzner Cloud
- Secrets & Umgebungsvariablen via GitLab CI/CD