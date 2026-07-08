# OpsMonitoring RKI


![Project Status](https://img.shields.io/badge/status-complete-brightgreen)


## Dokumentation
| Datei | Beschreibung |
|-------|-------------|
| [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) | Projektübersicht, Ziele, User Stories, Struktur |
| [docs/projectworkbook.md](docs/projectworkbook.md) | Sprint-Dokumentation, User Stories & Tasks (hierarchisch) |
| [docs/risikotabelle.md](docs/risikotabelle.md) | Risikotabelle |
| [docs/ABGABE_DOSSIER.md](docs/ABGABE_DOSSIER.md) | Umfangreiche Abschlussdokumentation fuer die Semesterabgabe |

## Quick Start
```bash
# Root-venv aktivieren (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Abhaengigkeiten beider Services in Root-venv installieren
python -m pip install -r services/data-collector/requirements.txt -r services/api-service/requirements.txt

# Data Collector starten (Swagger unter /doc)
python -m uvicorn app.main:app --app-dir services/data-collector --host 0.0.0.0 --port 8001 --reload

# API Service starten (neues Terminal, Swagger unter /doc)
python -m uvicorn app.main:app --app-dir services/api-service --host 0.0.0.0 --port 8002 --reload

# Frontend starten (neues Terminal)
cd services/webapp
npm install
npm run dev -- --host 0.0.0.0 --port 5173

# Infrastruktur lokal starten
cd ../../infrastructure
docker compose up -d
```

## Docker Stack (Recommended)
```bash
cd infrastructure
docker compose up -d --build

# Optional: Trigger fresh ingest
curl -X POST "http://localhost:8001/collect/run?limit_per_source=10"
```

Lokale URLs:
- Webapp: http://localhost:8080
- API Service Swagger: http://localhost:8002/doc
- Data Collector Swagger: http://localhost:8001/doc
- Neo4j Browser: http://localhost:7474

## Repository-Struktur
```
├── services/
│   ├── data-collector/
│   │   ├── app/
│   │   │   ├── architecture/
│   │   │   ├── collectors/
│   │   │   ├── schemas/
│   │   │   │   └── internal/
│   │   │   ├── mapping/
│   │   │   ├── normalizers/
│   │   │   ├── services/
│   │   │   ├── db/
│   │   │   └── utils/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── api-service/
│   │   └── app/
│   └── webapp/
│       ├── src/
│       ├── public/
│       ├── Dockerfile
│       └── package.json
├── infrastructure/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── neo4j/
│   └── traefik/
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── projectworkbook.md
│   └── risikotabelle.md
├── .github/
│   └── workflows/
│       └── ci.yml
├── .vscode/
│   ├── launch.json
│   └── settings.json
├── .gitignore
└── README.md
```

## Technologie-Stack
| Komponente | Technologie | Beschreibung |
|------------|-------------|--------------|
| Backend    | FastAPI     | Data Collector und ingest-orientierte Services |
| Datenbank  | Neo4J       | Graphdatenbank |
| Frontend   | Node.js | Webapp |
| Webserver  | Traefik | Routing und Reverse Proxy |
| Infrastruktur | Docker, Docker Compose | Containerisierung |
| Mapping-Modell | zentrale Architektur-Map | Feldzuordnung, Aliases, Runtime-Regeln |
| CI/CD      | GitHub Actions | Automatisiertes Deployment |
| Cloud      | Hetzner Cloud | Hosting |

## Projekt-Status
| Sprint | Zeitraum | Status |
|--------|----------|--------|
| Sprint 0 | Initialisierung | Abgeschlossen |
| Sprint 1 | Microservices-Architektur | Abgeschlossen |
| Sprint 2 | Webapp, API-Doku, UX | Abgeschlossen |
| Sprint 3 | Datenqualitaet, Persistenz, Testing | Abgeschlossen |

## Projektmanagement
Das Projektmanagement erfolgt nach dem Muster:
- Sprint (Phase) → User Story → Task
Siehe [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) und [docs/projectworkbook.md](docs/projectworkbook.md) für Details zur Hierarchie und Zuordnung.

## Features
- Zentrale Sammlung von Asset-, Service-, Update- und Advisory-Daten
- Vendor-unabhängige Normalisierung über zentrale Felddefinitionen
- Mehrquellen-Collector aktiv: NVD, CISA, GitHub Advisories, Microsoft; BSI/Cisco nur bei real erreichbaren Datenquellen
- Containerisierte Microservices
- Webzugriff & Datenvisualisierung mit informationszentrierter CVE-/Advisory-Sicht, Inspect-Aktionen und Device-Impact
- Automatisiertes Deployment (IaC, CI/CD)
- Neo4j Persistenz für Advisory-, CVE-, Vendor- und Device-Daten
- Keine Demo-/Mockdaten im Standard-Datenpfad
- Sprint-Dokumentation und Projektarbeitsbuch vollstaendig abgeschlossen

## API (Aktueller Stand)
- API-Service Swagger: /doc
- GET /api/overview
- GET /api/advisories
- GET /api/cves
- GET /api/cves/{cve_id}/intel
- POST /api/devices/push
- GET /api/devices
- GET /api/devices/{device_id}
- GET /api/impact/device/{device_id}
- GET /api/impact/summary
- GET /api/changes/entra

## Architektur (ASCII)
```
[ Externe APIs / Vendor Feeds ]
			  |
			  v
	 +-------------------+
	 |  data-collector   |
	 | collectors        |
	 | architecture map  |
	 | mapping           |
	 | normalizers       |
	 +-------------------+
			  |
			  v
		  +--------+
		  | Neo4J  |
		  +--------+
			  |
			  v
	 +-------------------+
	 | webapp / weitere  |
	 | ingest services   |
	 +-------------------+
```

## Development
1. Repo clonen & Python-Umgebung einrichten
2. Nur Root-venv nutzen (.venv)
3. Abhaengigkeiten fuer data-collector und api-service ins Root-venv installieren
4. Collector-Struktur in collectors, architecture, mapping und normalizers pflegen
5. Reale Asset-Daten bei Bedarf via `POST /api/devices/push` einspeisen
6. Frontend in services/webapp lokal pruefen
7. Infrastruktur via Docker Compose testen

## Debugging (Python)
- VS Code Debug-Konfiguration liegt in .vscode/launch.json.
- Standard-Interpreter liegt in .vscode/settings.json auf der Root-venv.
- Aktives Launch-Profil: FastAPI: Service Start (Root .venv).
- Swagger-UI ist fuer data-collector und api-service unter /doc erreichbar.

## Deployment
- CI/CD Pipeline via GitHub Actions
- Automatisiertes Deployment auf Hetzner Cloud
- Secrets & Umgebungsvariablen via GitHub Secrets