# Projektarbeitsbuch (Sprint-Dokumentation)

## Sprint 0 – Projektinitialisierung & Setup (2 Wochen)

**Sprint-Ziel:** Projektstruktur, Tools und Grundarchitektur stehen, erste Doku und CI/CD konzipiert

**Status:** Sprint abgeschlossen (alle Ziele und Deliverables erreicht)

**Epics und User Stories:**
| Epic | Story-ID | Rolle | Als [Rolle] möchte ich... | ...damit... | Akzeptanzkriterien | Story Points |
|------|----------|-------|--------------------------|-------------|-------------------|--------------|
| Setup | US-0.1 | Projektleiter | Als Projektleiter möchte ich ein zentrales GitHub-Repo anlegen | damit alle Projektdateien versioniert sind | Repo existiert, ist erreichbar, .gitignore vorhanden | 1 |
| Setup | US-0.2 | Entwickler | Als Entwickler möchte ich die Projektstruktur und Doku anlegen | damit die Entwicklung strukturiert starten kann | Verzeichnisstruktur, README, Doku-Templates vorhanden | 2 |
| Setup | US-0.3 | Projektleiter | Als Projektleiter möchte ich ein Hetzner-Projekt und Jira-Board anlegen | damit Infrastruktur und Aufgaben gemanagt werden | Hetzner-Projekt und Jira-Board existieren | 2 |
| Architektur | US-0.4 | Entwickler | Als Entwickler möchte ich die Architektur und das DB-Schema planen | damit die technische Basis klar ist | Architekturdiagramm, ERD, Tech-Stack-Tabelle vorhanden | 2 |
| CI/CD | US-0.5 | Entwickler | Als Entwickler möchte ich eine CI/CD Pipeline konzipieren | damit automatisiertes Deployment möglich ist | .github/workflows/ci.yml vorhanden | 1 |

**Tasks (hierarchisch nach User Story):**
| Parent Story | ID | Beschreibung | Verantwortlich | Geschätzter Aufwand (h) | Status |
|--------------|----|--------------|----------------|------------------------|--------|
| US-0.1 | T0.1 | GitHub Repo erstellen | Robin Kiefer | 1 | Abgeschlossen |
| US-0.1 | T0.14 | Git Initial-Commit | Robin Kiefer | 1 | Abgeschlossen |
| US-0.2 | T0.2 | Projektstruktur anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-0.2 | T0.3 | Doku-Templates anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-0.2 | T0.10 | Python venv einrichten | Robin Kiefer | 1 | Abgeschlossen |
| US-0.2 | T0.11 | requirements.txt initialisieren | Robin Kiefer | 1 | Abgeschlossen |
| US-0.2 | T0.12 | Erste Testausführung Backend | Robin Kiefer | 1 | Abgeschlossen |
| US-0.2 | T0.13 | Erste Testausführung Webapp | Robin Kiefer | 1 | Abgeschlossen |
| US-0.2 | T0.15 | README ausfüllen | Robin Kiefer | 1 | Abgeschlossen |
| US-0.2 | T0.16 | Projektstruktur im Repo dokumentieren | Robin Kiefer | 1 | Abgeschlossen |
| US-0.3 | T0.4 | Hetzner Projekt anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-0.3 | T0.5 | Jira Board einrichten | Robin Kiefer | 1 | Abgeschlossen |
| US-0.4 | T0.6 | Architekturdiagramm skizzieren | Robin Kiefer | 1 | Abgeschlossen |
| US-0.4 | T0.7 | Datenbankschema (ERD) entwerfen | Robin Kiefer | 1 | Abgeschlossen |
| US-0.4 | T0.8 | Tech-Stack festlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-0.5 | T0.9 | GitHub Actions Workflow anlegen (.github/workflows/ci.yml) | Robin Kiefer | 1 | Abgeschlossen |

**Definition of Done (DoD):**
- [x] GitHub Repo existiert und ist erreichbar
- [x] Projektstruktur und Doku-Templates angelegt
- [x] Hetzner-Projekt und Jira-Board existieren
- [x] Architekturdiagramm und ERD vorhanden
- [x] Tech-Stack und GitHub Actions Workflow erstellt

**Deliverables:**
| Nr. | Deliverable | Story | Beschreibung | Erfolgskriterium |
|-----|-------------|-------|--------------|-----------------|
| D0.1 | GitHub Repo | US-0.1 | Zentrales Repository | Repo existiert, .gitignore vorhanden |
| D0.2 | Projektstruktur & Doku | US-0.2 | Verzeichnisstruktur, README, Doku-Templates | Struktur und Templates vorhanden |
| D0.3 | Hetzner-Projekt & Jira | US-0.3 | Projekt und Board angelegt | Zugang vorhanden |
| D0.4 | Architektur & ERD | US-0.4 | Diagramm und Datenbankschema | Skizzen vorhanden |
| D0.5 | CI/CD Workflow | US-0.5 | .github/workflows/ci.yml | Datei vorhanden |

**Story Points Total:** 8

---

## Sprint 1 – Microservices-Architektur & Repo-Struktur (2 Wochen)

**Sprint-Ziel:**
Finale Monorepo-Struktur etablieren und den data-collector auf eine zentrale Architektur- und Mapping-Definition ausrichten, sodass Feldzuordnung, Aliases, Runtime-Regeln und Normalisierung zentral gepflegt werden.

**Status:** Teilweise abgeschlossen (Backend/Collector/API-Grundlagen umgesetzt, Infra-Anteile offen)

---

### Referenz-Architektur: Ziel-Repo-Struktur

```
semarb03_opsMonitoring_rki/
│
├── services/
│   │
│   ├── data-collector/              ← Python/FastAPI | Scheduler, sammelt & normalisiert
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py              ← Entrypoint, Scheduler-Start
│   │   │   ├── config.py            ← Env-Vars via pydantic-settings
│   │   │   ├── collectors/          ← ein Adapter pro externer Datenquelle
│   │   │   │   ├── base.py          ← Abstract Base Class collect()
│   │   │   │   ├── nvd.py
│   │   │   │   └── bsi.py
│   │   │   ├── architecture/        ← zentrale Architektur- und Mapping-Definition
│   │   │   │   └── architecture_map.py
│   │   │   ├── schemas/
│   │   │   │   └── internal/        ← internes Zielschema fuer normalisierte Daten
│   │   │   │       ├── asset.py
│   │   │   │       ├── service.py
│   │   │   │       ├── update.py
│   │   │   │       ├── advisory.py
│   │   │   │       ├── vendor.py
│   │   │   │       ├── service_change.py
│   │   │   │       └── cve.py
│   │   │   ├── mapping/             ← Ausfuehrungslogik fuer zentrale Feldzuordnung
│   │   │   │   ├── field_maps.py
│   │   │   │   ├── asset_mapping.py
│   │   │   │   ├── service_mapping.py
│   │   │   │   ├── update_mapping.py
│   │   │   │   ├── advisory_mapping.py
│   │   │   │   └── cve_mapping.py
│   │   │   ├── normalizers/         ← Wertvereinheitlichung nach dem Mapping
│   │   │   │   ├── asset_normalizer.py
│   │   │   │   ├── service_normalizer.py
│   │   │   │   ├── update_normalizer.py
│   │   │   │   ├── advisory_normalizer.py
│   │   │   │   └── cve_normalizer.py
│   │   │   ├── services/            ← Orchestrierung collect→map→normalize→save
│   │   │   │   └── ingest_service.py
│   │   │   ├── db/
│   │   │   │   └── neo4j_client.py  ← Verbindungs-Client zu Neo4J-Container
│   │   │   └── utils/               ← reine Hilfsfunktionen
│   │   │       ├── date_utils.py
│   │   │       └── http_utils.py
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── api-service/                 ← Python/FastAPI | spaeterer ingest/read Service, aktuell Minimalgeruest
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── config.py
│   │   │   ├── middleware/
│   │   │   │   └── auth.py
│   │   │   ├── db/
│   │   │   │   └── neo4j_client.py
│   │   │   └── utils/
│   │   │       └── pagination.py
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── webapp/                      ← Node.js | Frontend
│       ├── src/
│       │   ├── components/
│       │   ├── pages/
│       │   └── services/            ← API-Calls zum api-service
│       ├── public/
│       ├── Dockerfile
│       └── package.json
│
├── infrastructure/
│   ├── docker-compose.yml           ← lokale Entwicklung (alle 5 Container)
│   ├── docker-compose.prod.yml      ← Produktion
│   ├── traefik/
│   │   ├── traefik.yml              ← statische Konfiguration (der echte Gateway)
│   │   └── dynamic/
│   │       └── routes.yml           ← Routing-Regeln pro Service
│   └── neo4j/
│       └── init/                    ← Cypher-Constraints & Init-Skripte
│
├── .github/
│   └── workflows/
│       └── ci.yml
├── .vscode/
│   ├── launch.json
│   └── settings.json
├── .env.example
├── .gitignore
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── projectworkbook.md
│   ├── risikotabelle.md
│   └── api-spec.yaml               ← OpenAPI Spec (generiert aus FastAPI)
└── README.md
```

### Python-Umgebungen und Debugging (Windows)

- Root-venv: `.venv` fuer Skripte, Debugging und beide Services.
- Service-venvs: nicht mehr genutzt (vereinheitlicht auf Root-venv).
- Debug-Dateien in VS Code:
        - `.vscode/settings.json` setzt den Standard-Interpreter und Testkonfiguration.
        - `.vscode/launch.json` nutzt ein konsolidiertes FastAPI-Startprofil mit Root-venv.

### Container-Übersicht (docker-compose)

| Container | Image-Basis | Rolle | Ports |
|---|---|---|---|
| `ops-data-collector` | Python 3.12 slim | Scheduler, Daten sammeln & normalisieren | — (kein HTTP) |
| `ops-api-service` | Python 3.12 slim | REST-API für externe Zugriffe | intern: 8000 |
| `ops-webapp` | Node.js 20 alpine | Frontend | intern: 3000 |
| `ops-neo4j` | neo4j:5 | Graphdatenbank | intern: 7687 |
| `ops-traefik` | traefik:v3 | Reverse Proxy, SSL, Routing (echter Gateway) | 80, 443 |

### Datenfluss

```
Externe APIs (NVD, BSI, ...)
        │
        ▼
[ops-data-collector]  ←  sammelt, mappt ueber Architektur-Map, normalisiert und schreibt
        │
        ▼
   [ops-neo4j]        ←  einzige Source of Truth
        │
        ▼
[ops-api-service]    ←  spaeterer ingest/read Service, aktuell Minimalgeruest
        │
        ▼
   [ops-traefik]      ←  Routing /api/* → api-service, /* → webapp
        │
        ▼
   [ops-webapp]       ←  UI, ruft api-service via Traefik auf
```

### Hinweise und Quellen (API-Endpunkte und Doku)

| Quelle | Zweck | Doku | Endpoint/Feed | Auth/Info |
|---|---|---|---|---|
| NVD (NIST) | CVE, CPE, CVSS | https://nvd.nist.gov/developers | https://services.nvd.nist.gov/rest/json/cves/2.0 | API Key empfohlen (Rate Limits) |
| NVD CPE | Plattform-/Produktdaten | https://nvd.nist.gov/developers | https://services.nvd.nist.gov/rest/json/cpes/2.0 | API Key empfohlen |
| NVD CPE Match | CPE Match-Kriterien | https://nvd.nist.gov/developers | https://services.nvd.nist.gov/rest/json/cpematch/2.0 | API Key empfohlen |
| BSI | Warnungen/Lageinfos (DE) | https://www.bsi.bund.de | https://www.cert-bund.de | Je nach Quelle Portal/Feed statt einheitlicher REST-API |
| CISA KEV | Aktiv ausgenutzte Schwachstellen | https://www.cisa.gov/known-exploited-vulnerabilities-catalog | https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json | Öffentlicher JSON Feed |
| MSRC | Microsoft Security Updates | https://msrc.microsoft.com/update-guide | https://msrc.microsoft.com/update-guide | Teilweise Registrierung/Key erforderlich |
| Cisco PSIRT | Cisco Advisories | https://sec.cloudapps.cisco.com/security/center/publicationListing.x | https://developer.cisco.com/docs/psirt/ | API Key erforderlich |
| GitHub Advisories | Package/Ecosystem Advisories | https://docs.github.com/en/rest/security-advisories | https://api.github.com/advisories | Token empfohlen |

**Hinweis für das eigene API-Service (FastAPI):**
- Swagger UI: `/doc`
- ReDoc: deaktiviert im MVP
- OpenAPI JSON: `/openapi.json`

---

**Epics und User Stories:**
| Epic | Story-ID | Rolle | Als [Rolle] möchte ich... | ...damit... | Akzeptanzkriterien | Story Points |
|------|----------|-------|--------------------------|-------------|-------------------|--------------|
| Architektur | US-1.1 | Entwickler | Als Entwickler möchte ich die Monorepo-Struktur final anlegen | damit alle Services eine klare Heimat haben | Alle Verzeichnisse, `__init__.py`-Dateien und Dockerfiles vorhanden | 3 |
| Architektur | US-1.2 | Entwickler | Als Entwickler möchte ich eine zentrale Architektur-Map fuer den data-collector anlegen | damit Feldzuordnung, Aliases und Runtime-Regeln zentral gepflegt werden | `architecture/architecture_map.py` existiert und beschreibt die Zielobjekte | 3 |
| data-collector | US-1.3 | Entwickler | Als Entwickler möchte ich die Collector-Struktur aufbauen | damit Collector, internes Schema, Mapping und Normalisierung sauber getrennt sind | collectors/, architecture/, schemas/, mapping/, normalizers/, services/ vorhanden | 3 |
| api-service | US-1.4 | Entwickler | Als Entwickler möchte ich den api-service nur als Minimalgeruest vorbereiten | damit spaetere ingest/read Anforderungen ohne Fehlpraegung umgesetzt werden koennen | main.py, config.py, db/, middleware/, utils/ vorhanden | 1 |
| Infra | US-1.5 | DevOps | Als DevOps möchte ich docker-compose mit allen 5 Containern konfigurieren | damit das Gesamtsystem lokal startbar ist | `docker-compose up` startet alle Container fehlerfrei | 3 |
| Infra | US-1.6 | Entwickler | Als Entwickler möchte ich config.py mit pydantic-settings in jedem Service | damit alle Env-Vars zentral und typsicher geladen werden | `.env.example` vorhanden, config.py liest alle Vars | 2 |

**Tasks:**
| Parent Story | ID | Beschreibung | Verantwortlich | Geschätzter Aufwand (h) | Status |
|--------------|----|--------------|----------------|------------------------|--------|
| US-1.1 | T1.1 | Alte `backend/` und `services/` Struktur in neue Monorepo-Struktur überführen | Robin Kiefer | 2 | Abgeschlossen |
| US-1.1 | T1.2 | Dockerfiles für data-collector und api-service anlegen | Robin Kiefer | 1 | In Arbeit |
| US-1.1 | T1.3 | Dockerfile für webapp (Node.js) anlegen | Robin Kiefer | 1 | In Arbeit |
| US-1.2 | T1.4 | `architecture/architecture_map.py` mit Objektarten, PropertyMap und Runtime-Regeln anlegen | Robin Kiefer | 2 | Abgeschlossen |
| US-1.2 | T1.5 | zentrale Felddefinitionen und Aliases in `mapping/field_maps.py` anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-1.3 | T1.6 | `schemas/internal/` fuer Asset, Service, Update, Advisory, Vendor, ServiceChange und CVE anlegen | Robin Kiefer | 2 | Abgeschlossen |
| US-1.3 | T1.7 | collectors/base.py mit Abstract Base Class anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-1.3 | T1.8 | Mapping- und Normalizer-Skeletons anlegen | Robin Kiefer | 2 | Abgeschlossen |
| US-1.4 | T1.9 | api-service auf Minimalgeruest reduzieren | Robin Kiefer | 1 | Abgeschlossen |
| US-1.4 | T1.10 | middleware/auth.py Skeleton anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-1.5 | T1.12 | docker-compose.yml mit allen 5 Services konfigurieren | Robin Kiefer | 3 | Offen |
| US-1.5 | T1.13 | Traefik-Routing-Regeln für api-service und webapp definieren | Robin Kiefer | 2 | Offen |
| US-1.5 | T1.14 | Neo4J-Container mit Init-Skript und Constraints konfigurieren | Robin Kiefer | 1 | Offen |
| US-1.6 | T1.15 | config.py mit pydantic-settings in data-collector anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-1.6 | T1.16 | config.py mit pydantic-settings in api-service anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-1.6 | T1.17 | .env.example mit allen benötigten Variablen befüllen | Robin Kiefer | 1 | Offen |
| US-1.6 | T1.18 | Root-venv und Service-venvs anlegen und dokumentieren | Robin Kiefer | 1 | Abgeschlossen (Root-venv-Only) |
| US-1.6 | T1.19 | VS Code Debug-Dateien `.vscode/launch.json` und `.vscode/settings.json` anlegen | Robin Kiefer | 1 | Abgeschlossen |

**Definition of Done (DoD):**
- [x] Alle Service-Verzeichnisse mit korrektem Layer-Aufbau vorhanden
- [x] `architecture/architecture_map.py` definiert die zentrale Collector-Logik
- [ ] `docker-compose up` startet alle 5 Container fehlerfrei
- [ ] Traefik routet `/api/*` zu api-service, `/*` zu webapp
- [ ] `.env.example` dokumentiert alle Umgebungsvariablen
- [ ] Jeder Service hat ein eigenes Dockerfile und requirements.txt (Dockerfile-Inhalt noch offen)

**Deliverables:**
| Nr. | Deliverable | Story | Beschreibung | Erfolgskriterium |
|-----|-------------|-------|--------------|-----------------|
| D1.1 | Monorepo-Struktur | US-1.1 | Finale Verzeichnisstruktur | Struktur entspricht Referenz-Architektur |
| D1.2 | Architektur-Map | US-1.2 | Zentrale Objekt- und Felddefinition | Regeln sind an einer Stelle gepflegt |
| D1.3 | data-collector Skeleton | US-1.3 | Collector-Struktur vollständig | Collectors, Schemas, Mapping und Normalizer vorhanden |
| D1.4 | api-service Skeleton | US-1.4 | neutrales Basisgeruest | Keine fachlich falsche Vorpraegung mehr |
| D1.5 | docker-compose Setup | US-1.5 | Alle 5 Container | `docker-compose up` läuft |
| D1.6 | Config & Env | US-1.6 | pydantic-settings, .env.example | Alle Vars dokumentiert |

**Story Points Total:** 16

---

## Sprint 2 – Webapp, Containerisierung & API-Schnittstelle (2 Wochen)

**Sprint-Ziel:**
Webapp entwerfen, Backend containerisieren und API-Schnittstelle dokumentieren/publizieren.

**Status:** In Arbeit (Webapp/Drilldown/API-Doku umgesetzt, Containerisierung noch offen)

**Epics und User Stories:**
| Epic | Story-ID | Rolle | Als [Rolle] möchte ich... | ...damit... | Akzeptanzkriterien | Story Points |
|------|----------|-------|--------------------------|-------------|-------------------|--------------|
| Webapp | US-2.1 | Entwickler | Als Entwickler möchte ich eine Webapp entwerfen | damit Nutzer die Monitoring-Daten visualisieren können | UI-Design vorhanden, Mockup klickbar | 2 |
| Container | US-2.2 | DevOps | Als DevOps möchte ich das Backend in einen Docker-Container verpacken | damit es portabel und einfach deploybar ist | Dockerfile vorhanden, Container läuft | 2 |
| API | US-2.3 | Entwickler | Als Entwickler möchte ich die API-Schnittstelle dokumentieren und publizieren | damit andere Teams sie nutzen können | OpenAPI/Swagger verfügbar, Doku online | 2 |

**Tasks:**
| Parent Story | ID | Beschreibung | Verantwortlich | Geschätzter Aufwand (h) | Status |
|--------------|----|--------------|----------------|------------------------|--------|
| US-2.1 | T2.1 | Webapp-UI-Design entwerfen | Robin Kiefer | 2 | Abgeschlossen |
| US-2.1 | T2.2 | Mockup klickbar machen | Robin Kiefer | 1 | Abgeschlossen |
| US-2.2 | T2.3 | Dockerfile für Backend schreiben | Robin Kiefer | 2 | Offen |
| US-2.2 | T2.4 | Docker Compose für Gesamtsystem anlegen | Robin Kiefer | 2 | Offen |
| US-2.3 | T2.5 | OpenAPI/Swagger-Dokumentation erstellen | Robin Kiefer | 2 | Abgeschlossen |
| US-2.3 | T2.6 | API-Doku online publizieren | Robin Kiefer | 1 | In Arbeit |

**Definition of Done (DoD):**
- [x] Webapp-Design und klickbares Mockup vorhanden
- [ ] Backend als Docker-Container lauffähig
- [ ] Docker Compose für Gesamtsystem vorhanden
- [ ] API-Dokumentation online verfügbar (lokal vorhanden via /doc)

**Deliverables:**
| Nr. | Deliverable | Story | Beschreibung | Erfolgskriterium |
|-----|-------------|-------|--------------|-----------------|
| D2.1 | Webapp-Mockup | US-2.1 | UI-Design, klickbar | Mockup getestet |
| D2.2 | Backend-Container | US-2.2 | Docker-Image | Container läuft lokal |
| D2.3 | Compose-Setup | US-2.2 | Docker Compose | Gesamtsystem startet |
| D2.4 | API-Doku | US-2.3 | OpenAPI/Swagger | Online abrufbar |

**Story Points Total:** 6

### Nachführung Stand 2026-06-07

**Umgesetzt seit letzter Aktualisierung:**
- Data-Collector vollständig als Pipeline (collect → map → normalize) implementiert.
- Quellen integriert: BSI, NVD, CISA KEV, GitHub Advisories, Cisco, Microsoft, Entra-Change-Signal.
- API-Service erweitert um Device Inventory, Impact-Bewertung und CVE-Intel-Endpunkte.
- Frontend als interaktives Cockpit mit Drilldown, Filtern, Device-Fenster und CVE-Intel-Fenster umgesetzt.
- Swagger lokal für beide Services unter `/doc` nutzbar.

**Offene Prioritäten (Backlog nahe Umsetzung):**
- Dockerfiles und Compose produktionsreif ausarbeiten.
- Traefik-Routing finalisieren.
- Neo4j Persistenz statt In-Memory Device Store integrieren.
- Versionsgenaues Matching (SemVer/CPE) für präzisere Betroffenheit umsetzen.

---

**Sprint-Ziel:** 

**Epics und User Stories:**
| Epic | Story-ID | Rolle | Als [Rolle] möchte ich... | ...damit... | Akzeptanzkriterien | Story Points |
|------|----------|-------|--------------------------|-------------|-------------------|--------------|

**Tasks:**
| ID | Beschreibung | Story | Verantwortlich | Geschätzter Aufwand (h) | Status |
|----|--------------|-------|----------------|------------------------|--------|

**Definition of Done (DoD):**
- [ ]
- [ ]

**Deliverables:**
| Nr. | Deliverable | Story | Beschreibung | Erfolgskriterium |
|-----|-------------|-------|--------------|-----------------|

**Story Points Total:**

---

## Sprint 3 – API-Anbindungen & Testing (2 Wochen)

**Sprint-Ziel:** 

**Epics und User Stories:**
| Epic | Story-ID | Rolle | Als [Rolle] möchte ich... | ...damit... | Akzeptanzkriterien | Story Points |
|------|----------|-------|--------------------------|-------------|-------------------|--------------|

**Tasks:**
| ID | Beschreibung | Story | Verantwortlich | Geschätzter Aufwand (h) | Status |
|----|--------------|-------|----------------|------------------------|--------|

**Definition of Done (DoD):**
- [ ]
- [ ]

**Deliverables:**
| Nr. | Deliverable | Story | Beschreibung | Erfolgskriterium |
|-----|-------------|-------|--------------|-----------------|

**Story Points Total:**
