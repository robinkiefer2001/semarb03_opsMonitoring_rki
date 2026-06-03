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
Finale Monorepo-Struktur etablieren, alle Microservice-Verzeichnisse mit korrektem Layer-Aufbau anlegen, shared Models definieren und jeden Service als eigenständigen Docker-Container vorbereiten.

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
│   │   │   ├── models/
│   │   │   │   ├── raw/             ← Schicht 1: rohe API-Antworten (NVD, BSI, ...)
│   │   │   │   │   ├── nvd_raw.py
│   │   │   │   │   └── bsi_raw.py
│   │   │   │   ├── domain/          ← Schicht 2: internes normalisiertes Model
│   │   │   │   │   └── cve.py
│   │   │   │   └── db/              ← Schicht 3: Neo4J Node/Relation-Struktur
│   │   │   │       └── cve_node.py
│   │   │   ├── mappers/             ← Konvertierung: raw → domain → db_node
│   │   │   │   └── cve_mapper.py
│   │   │   ├── collectors/          ← ein Adapter pro externer Datenquelle
│   │   │   │   ├── base.py          ← Abstract Base Class collect()
│   │   │   │   ├── nvd.py
│   │   │   │   └── bsi.py
│   │   │   ├── services/            ← Businesslogik (orchestriert collect→map→save)
│   │   │   │   └── cve_service.py
│   │   │   ├── db/
│   │   │   │   └── neo4j_client.py  ← Verbindungs-Client zu Neo4J-Container
│   │   │   └── utils/               ← reine Hilfsfunktionen
│   │   │       ├── date_utils.py
│   │   │       └── http_utils.py
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── api-service/                 ← Python/FastAPI | externer REST-API-Endpunkt
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── config.py
│   │   │   ├── models/
│   │   │   │   ├── domain/          ← Schicht 2: via shared/ importiert
│   │   │   │   └── response/        ← Schicht 4: öffentliche API-Response-DTOs
│   │   │   │       └── cve_response.py
│   │   │   ├── mappers/             ← domain → response
│   │   │   │   └── cve_mapper.py
│   │   │   ├── routers/             ← HTTP-Layer (nur Request/Response, keine Logik)
│   │   │   │   ├── cve.py           ← GET /cves, GET /cves/{id}
│   │   │   │   └── health.py        ← GET /health
│   │   │   ├── services/            ← Businesslogik, DB-Abfragen
│   │   │   │   └── cve_service.py
│   │   │   ├── middleware/
│   │   │   │   └── auth.py          ← API-Key / JWT-Prüfung
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
├── shared/                          ← geteilte Models zwischen Services
│   └── models/
│       ├── __init__.py
│       └── cve.py                   ← CveDomain (einmal definiert, mehrfach genutzt)
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
├── .env.example
├── .gitignore
├── docs/
│   ├── PROJECT_OVERVIEW.md
│   ├── projectworkbook.md
│   ├── risikotabelle.md
│   └── api-spec.yaml               ← OpenAPI Spec (generiert aus FastAPI)
└── README.md
```

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
[ops-data-collector]  ←  sammelt, mappt raw→domain→db_node, schreibt
        │
        ▼
   [ops-neo4j]        ←  einzige Source of Truth
        │
        ▼
 [ops-api-service]    ←  liest, mappt domain→response, liefert REST
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
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

---

**Epics und User Stories:**
| Epic | Story-ID | Rolle | Als [Rolle] möchte ich... | ...damit... | Akzeptanzkriterien | Story Points |
|------|----------|-------|--------------------------|-------------|-------------------|--------------|
| Architektur | US-1.1 | Entwickler | Als Entwickler möchte ich die Monorepo-Struktur final anlegen | damit alle Services eine klare Heimat haben | Alle Verzeichnisse, `__init__.py`-Dateien und Dockerfiles vorhanden | 3 |
| Architektur | US-1.2 | Entwickler | Als Entwickler möchte ich shared/models mit dem CveDomain-Model anlegen | damit beide Services dasselbe Model nutzen | `shared/models/cve.py` existiert, wird in beiden Services importiert | 2 |
| data-collector | US-1.3 | Entwickler | Als Entwickler möchte ich die Layer-Struktur im data-collector aufbauen | damit raw→domain→db_node sauber getrennt ist | models/, mappers/, collectors/, services/, utils/ vorhanden und strukturiert | 3 |
| api-service | US-1.4 | Entwickler | Als Entwickler möchte ich die Layer-Struktur im api-service aufbauen | damit Routing, Businesslogik und DB sauber getrennt sind | routers/, services/, models/response/, middleware/ vorhanden | 3 |
| Infra | US-1.5 | DevOps | Als DevOps möchte ich docker-compose mit allen 5 Containern konfigurieren | damit das Gesamtsystem lokal startbar ist | `docker-compose up` startet alle Container fehlerfrei | 3 |
| Infra | US-1.6 | Entwickler | Als Entwickler möchte ich config.py mit pydantic-settings in jedem Service | damit alle Env-Vars zentral und typsicher geladen werden | `.env.example` vorhanden, config.py liest alle Vars | 2 |

**Tasks:**
| Parent Story | ID | Beschreibung | Verantwortlich | Geschätzter Aufwand (h) | Status |
|--------------|----|--------------|----------------|------------------------|--------|
| US-1.1 | T1.1 | Alte `backend/` und `services/` Struktur in neue Monorepo-Struktur überführen | Robin Kiefer | 2 | Offen |
| US-1.1 | T1.2 | Dockerfiles für data-collector und api-service anlegen | Robin Kiefer | 1 | Offen |
| US-1.1 | T1.3 | Dockerfile für webapp (Node.js) anlegen | Robin Kiefer | 1 | Offen |
| US-1.2 | T1.4 | `shared/models/cve.py` mit CveDomain Pydantic-Model anlegen | Robin Kiefer | 1 | Offen |
| US-1.2 | T1.5 | shared/ als Python-Package einrichten (`__init__.py`, PYTHONPATH) | Robin Kiefer | 1 | Offen |
| US-1.3 | T1.6 | models/raw/, models/domain/, models/db/ im data-collector anlegen | Robin Kiefer | 2 | Offen |
| US-1.3 | T1.7 | collectors/base.py mit Abstract Base Class anlegen | Robin Kiefer | 1 | Offen |
| US-1.3 | T1.8 | mappers/cve_mapper.py Skeleton anlegen | Robin Kiefer | 1 | Offen |
| US-1.4 | T1.9 | routers/ mit health.py und cve.py Skeleton anlegen | Robin Kiefer | 1 | Offen |
| US-1.4 | T1.10 | models/response/cve_response.py anlegen | Robin Kiefer | 1 | Offen |
| US-1.4 | T1.11 | middleware/auth.py Skeleton anlegen | Robin Kiefer | 1 | Offen |
| US-1.5 | T1.12 | docker-compose.yml mit allen 5 Services konfigurieren | Robin Kiefer | 3 | Offen |
| US-1.5 | T1.13 | Traefik-Routing-Regeln für api-service und webapp definieren | Robin Kiefer | 2 | Offen |
| US-1.5 | T1.14 | Neo4J-Container mit Init-Skript und Constraints konfigurieren | Robin Kiefer | 1 | Offen |
| US-1.6 | T1.15 | config.py mit pydantic-settings in data-collector anlegen | Robin Kiefer | 1 | Offen |
| US-1.6 | T1.16 | config.py mit pydantic-settings in api-service anlegen | Robin Kiefer | 1 | Offen |
| US-1.6 | T1.17 | .env.example mit allen benötigten Variablen befüllen | Robin Kiefer | 1 | Offen |

**Definition of Done (DoD):**
- [ ] Alle Service-Verzeichnisse mit korrektem Layer-Aufbau vorhanden
- [ ] `shared/models/cve.py` existiert und wird von beiden Services importiert
- [ ] `docker-compose up` startet alle 5 Container fehlerfrei
- [ ] Traefik routet `/api/*` zu api-service, `/*` zu webapp
- [ ] `.env.example` dokumentiert alle Umgebungsvariablen
- [ ] Jeder Service hat ein eigenes Dockerfile und requirements.txt

**Deliverables:**
| Nr. | Deliverable | Story | Beschreibung | Erfolgskriterium |
|-----|-------------|-------|--------------|-----------------|
| D1.1 | Monorepo-Struktur | US-1.1 | Finale Verzeichnisstruktur | Struktur entspricht Referenz-Architektur |
| D1.2 | Shared Models | US-1.2 | `shared/models/cve.py` | Wird fehlerfrei importiert |
| D1.3 | data-collector Skeleton | US-1.3 | Layer-Struktur vollständig | Alle Module vorhanden |
| D1.4 | api-service Skeleton | US-1.4 | Layer-Struktur vollständig | Health-Endpunkt erreichbar |
| D1.5 | docker-compose Setup | US-1.5 | Alle 5 Container | `docker-compose up` läuft |
| D1.6 | Config & Env | US-1.6 | pydantic-settings, .env.example | Alle Vars dokumentiert |

**Story Points Total:** 16

---

## Sprint 2 – Webapp, Containerisierung & API-Schnittstelle (2 Wochen)

**Sprint-Ziel:**
Webapp entwerfen, Backend containerisieren und API-Schnittstelle dokumentieren/publizieren.

**Epics und User Stories:**
| Epic | Story-ID | Rolle | Als [Rolle] möchte ich... | ...damit... | Akzeptanzkriterien | Story Points |
|------|----------|-------|--------------------------|-------------|-------------------|--------------|
| Webapp | US-2.1 | Entwickler | Als Entwickler möchte ich eine Webapp entwerfen | damit Nutzer die Monitoring-Daten visualisieren können | UI-Design vorhanden, Mockup klickbar | 2 |
| Container | US-2.2 | DevOps | Als DevOps möchte ich das Backend in einen Docker-Container verpacken | damit es portabel und einfach deploybar ist | Dockerfile vorhanden, Container läuft | 2 |
| API | US-2.3 | Entwickler | Als Entwickler möchte ich die API-Schnittstelle dokumentieren und publizieren | damit andere Teams sie nutzen können | OpenAPI/Swagger verfügbar, Doku online | 2 |

**Tasks:**
| Parent Story | ID | Beschreibung | Verantwortlich | Geschätzter Aufwand (h) | Status |
|--------------|----|--------------|----------------|------------------------|--------|
| US-2.1 | T2.1 | Webapp-UI-Design entwerfen | Robin Kiefer | 2 | Offen |
| US-2.1 | T2.2 | Mockup klickbar machen | Robin Kiefer | 1 | Offen |
| US-2.2 | T2.3 | Dockerfile für Backend schreiben | Robin Kiefer | 2 | Offen |
| US-2.2 | T2.4 | Docker Compose für Gesamtsystem anlegen | Robin Kiefer | 2 | Offen |
| US-2.3 | T2.5 | OpenAPI/Swagger-Dokumentation erstellen | Robin Kiefer | 2 | Offen |
| US-2.3 | T2.6 | API-Doku online publizieren | Robin Kiefer | 1 | Offen |

**Definition of Done (DoD):**
- [ ] Webapp-Design und klickbares Mockup vorhanden
- [ ] Backend als Docker-Container lauffähig
- [ ] Docker Compose für Gesamtsystem vorhanden
- [ ] API-Dokumentation online verfügbar

**Deliverables:**
| Nr. | Deliverable | Story | Beschreibung | Erfolgskriterium |
|-----|-------------|-------|--------------|-----------------|
| D2.1 | Webapp-Mockup | US-2.1 | UI-Design, klickbar | Mockup getestet |
| D2.2 | Backend-Container | US-2.2 | Docker-Image | Container läuft lokal |
| D2.3 | Compose-Setup | US-2.2 | Docker Compose | Gesamtsystem startet |
| D2.4 | API-Doku | US-2.3 | OpenAPI/Swagger | Online abrufbar |

**Story Points Total:** 6

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
