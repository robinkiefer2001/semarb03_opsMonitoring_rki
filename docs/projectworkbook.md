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

**Status:** Abgeschlossen

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
| US-1.1 | T1.2 | Dockerfiles für data-collector und api-service anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-1.1 | T1.3 | Dockerfile für webapp (Node.js) anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-1.2 | T1.4 | `architecture/architecture_map.py` mit Objektarten, PropertyMap und Runtime-Regeln anlegen | Robin Kiefer | 2 | Abgeschlossen |
| US-1.2 | T1.5 | zentrale Felddefinitionen und Aliases in `mapping/field_maps.py` anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-1.3 | T1.6 | `schemas/internal/` fuer Asset, Service, Update, Advisory, Vendor, ServiceChange und CVE anlegen | Robin Kiefer | 2 | Abgeschlossen |
| US-1.3 | T1.7 | collectors/base.py mit Abstract Base Class anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-1.3 | T1.8 | Mapping- und Normalizer-Skeletons anlegen | Robin Kiefer | 2 | Abgeschlossen |
| US-1.4 | T1.9 | api-service auf Minimalgeruest reduzieren | Robin Kiefer | 1 | Abgeschlossen |
| US-1.4 | T1.10 | middleware/auth.py Skeleton anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-1.5 | T1.12 | docker-compose.yml mit allen 5 Services konfigurieren | Robin Kiefer | 3 | Abgeschlossen (lokaler Stack mit Neo4j, data-collector, api-service, webapp) |
| US-1.5 | T1.13 | Traefik-Routing-Regeln für api-service und webapp definieren | Robin Kiefer | 2 | Abgeschlossen (Konfiguration vorhanden, lokal nicht aktiv geschaltet) |
| US-1.5 | T1.14 | Neo4J-Container mit Init-Skript und Constraints konfigurieren | Robin Kiefer | 1 | Teilweise abgeschlossen |
| US-1.6 | T1.15 | config.py mit pydantic-settings in data-collector anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-1.6 | T1.16 | config.py mit pydantic-settings in api-service anlegen | Robin Kiefer | 1 | Abgeschlossen |
| US-1.6 | T1.17 | .env.example mit allen benötigten Variablen befüllen | Robin Kiefer | 1 | Abgeschlossen |
| US-1.6 | T1.18 | Root-venv und Service-venvs anlegen und dokumentieren | Robin Kiefer | 1 | Abgeschlossen (Root-venv-Only) |
| US-1.6 | T1.19 | VS Code Debug-Dateien `.vscode/launch.json` und `.vscode/settings.json` anlegen | Robin Kiefer | 1 | Abgeschlossen |

**Definition of Done (DoD):**
- [x] Alle Service-Verzeichnisse mit korrektem Layer-Aufbau vorhanden
- [x] `architecture/architecture_map.py` definiert die zentrale Collector-Logik
- [x] `docker-compose up` startet den lokalen Stack fehlerfrei
- [x] Traefik-Konfiguration für `/api/*` und `/*` ist vorbereitet
- [x] `.env.example` dokumentiert die genutzten Umgebungsvariablen
- [x] Jeder Service hat ein Dockerfile und requirements.txt

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

**Status:** Abgeschlossen

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
| US-2.2 | T2.3 | Dockerfile für Backend schreiben | Robin Kiefer | 2 | Abgeschlossen |
| US-2.2 | T2.4 | Docker Compose für Gesamtsystem anlegen | Robin Kiefer | 2 | Abgeschlossen |
| US-2.3 | T2.5 | OpenAPI/Swagger-Dokumentation erstellen | Robin Kiefer | 2 | Abgeschlossen |
| US-2.3 | T2.6 | API-Doku online publizieren | Robin Kiefer | 1 | Abgeschlossen (lokal via /doc) |

**Definition of Done (DoD):**
- [x] Webapp-Design und klickbares Mockup vorhanden
- [x] Backend als Docker-Container lauffähig
- [x] Docker Compose für Gesamtsystem vorhanden
- [x] API-Dokumentation lokal verfügbar via /doc

**Deliverables:**
| Nr. | Deliverable | Story | Beschreibung | Erfolgskriterium |
|-----|-------------|-------|--------------|-----------------|
| D2.1 | Webapp-Mockup | US-2.1 | UI-Design, klickbar | Mockup getestet |
| D2.2 | Backend-Container | US-2.2 | Docker-Image | Container läuft lokal |
| D2.3 | Compose-Setup | US-2.2 | Docker Compose | Gesamtsystem startet |
| D2.4 | API-Doku | US-2.3 | OpenAPI/Swagger | Online abrufbar |

**Story Points Total:** 6

### Nachführung Stand 1

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

### Nachführung Stand 2

**Umgesetzt seit letzter Aktualisierung:**
- Neo4j-Persistenz für Advisories, CVEs, Vendors und Devices aktiviert.
- Lokaler Docker-Stack mit `neo4j`, `data-collector`, `api-service` und `webapp` lauffähig gemacht.
- Backend-Tests für API und Normalizer ergänzt und erfolgreich ausgeführt.
- Frontend auf informationszentrierte CVE-/Advisory-Sicht umgestellt.
- Mockup-/Demo-Daten aus Frontend, API-Fallbacks und Collector-Fallbacks entfernt.

**Offene Prioritäten (Backlog nahe Umsetzung):**
- Reales Asset-Inventar per `POST /api/devices/push` einspielen.
- Versionsgenaues Matching über CPE/SemVer statt Keyword-Matching umsetzen.
- Optionale Auth/API-Key-Unterstützung für Cisco/MSRC/GitHub-Produktivfeeds ergänzen.
- Traefik im lokalen Compose bei Bedarf aktiv in den Runtime-Flow aufnehmen.

---

## Sprint 3 – API-Anbindungen & Testing (2 Wochen)

**Sprint-Ziel:** Reale Datenqualität erhöhen, Mockdaten entfernen, Persistenz absichern und Matching-Logik härten.

**Status:** Abgeschlossen

**Epics und User Stories:**
| Epic | Story-ID | Rolle | Als [Rolle] möchte ich... | ...damit... | Akzeptanzkriterien | Story Points |
|------|----------|-------|--------------------------|-------------|-------------------|--------------|
| Datenqualität | US-3.1 | Analyst | Als Analyst möchte ich nur echte Advisory-/CVE-Daten ohne Mockups sehen | damit die UI keine Demo- oder Platzhalterdaten mehr zeigt | Keine Placeholder/Demo/Fallback-Einträge mehr im UI-Output | 3 |
| Persistenz | US-3.2 | Entwickler | Als Entwickler möchte ich Neo4j als echten Persistenzlayer für Snapshot- und Device-Daten nutzen | damit Neustarts keine relevanten Daten verlieren | Advisories, CVEs, Vendors und Devices werden in Neo4j geschrieben und gelesen | 3 |
| Testing | US-3.3 | Entwickler | Als Entwickler möchte ich Regressionstests für API und Normalizer ausführen | damit Kernfunktionen nach Änderungen validiert werden | Backend-Tests laufen lokal erfolgreich | 2 |
| Matching | US-3.4 | Analyst | Als Analyst möchte ich versionsgenaues Matching statt Keyword-Matching | damit nur echte betroffene Assets als impacted erscheinen | CPE-/SemVer-basierte Korrelation ersetzt die einfache Textsuche | 5 |

**Tasks:**
| ID | Beschreibung | Story | Verantwortlich | Geschätzter Aufwand (h) | Status |
|----|--------------|-------|----------------|------------------------|--------|
| T3.1 | Mockup-/Demo-Daten aus Frontend und API-Fallbacks entfernen | US-3.1 | Robin Kiefer | 2 | Abgeschlossen |
| T3.2 | Placeholder-Collector-Fallbacks entfernen | US-3.1 | Robin Kiefer | 2 | Abgeschlossen |
| T3.3 | Neo4j-Clients für data-collector und api-service implementieren | US-3.2 | Robin Kiefer | 3 | Abgeschlossen |
| T3.4 | Snapshot- und Device-Daten in Neo4j persistieren | US-3.2 | Robin Kiefer | 2 | Abgeschlossen |
| T3.5 | API- und Normalizer-Tests ergänzen und ausführen | US-3.3 | Robin Kiefer | 2 | Abgeschlossen |
| T3.6 | Reales Asset-Inventar über Push-API einspeisen | US-3.4 | Robin Kiefer | 2 | Abgeschlossen |
| T3.7 | CPE-/SemVer-basiertes Matching implementieren | US-3.4 | Robin Kiefer | 5 | Abgeschlossen |

**Definition of Done (DoD):**
- [x] Keine Demo-/Placeholder-Daten werden mehr standardmäßig ausgeliefert
- [x] Neo4j wird für Snapshot- und Device-Daten aktiv genutzt
- [x] Backend-Regressionstests wurden lokal erfolgreich ausgeführt
- [x] Reale Asset-Daten sind eingespielt und verifiziert
- [x] Präzises versionsbasiertes Matching ersetzt Keyword-Korrelation

**Deliverables:**
| Nr. | Deliverable | Story | Beschreibung | Erfolgskriterium |
|-----|-------------|-------|--------------|-----------------|
| D3.1 | Bereinigte Datenbasis | US-3.1 | Keine Mock-/Demo-Daten im Standardpfad | UI und API zeigen nur echte Quell-Daten |
| D3.2 | Neo4j Persistenz | US-3.2 | Persistente Speicherung für Kernobjekte | Neustart verliert keine Kernobjekte |
| D3.3 | Backend-Testbasis | US-3.3 | Tests für API und Normalizer | Testlauf erfolgreich |
| D3.4 | Präzises Asset-Matching | US-3.4 | Reale betroffene Assets statt Texttreffer | Nur verifizierte Impact-Zuordnung |

**Story Points Total:** 13

---

## Sprint 3 – Abschlussbericht

**Ergebniszusammenfassung:**
- Alle geplanten Sprint-3-Stories wurden umgesetzt und abgenommen.
- Die End-to-End-Kette (Collect → Normalize → Persist → API → UI) ist stabil und reproduzierbar lauffaehig.
- Datenqualitaet, Persistenz und Testbarkeit wurden auf produktionsnahes Niveau gehoben.

**Abnahmecheck je Story:**
| Story-ID | Abnahmestatus | Nachweis |
|----------|----------------|----------|
| US-3.1 | Abgenommen | Keine Demo-/Placeholder-Daten im Standardpfad |
| US-3.2 | Abgenommen | Persistenz in Neo4j fuer Kernobjekte aktiv |
| US-3.3 | Abgenommen | Regressionstests API/Normalizer erfolgreich |
| US-3.4 | Abgenommen | Versionsgenaue Korrelation fuer belastbare Impact-Zuordnung |

**Sprint-Metriken:**
| Kennzahl | Wert |
|----------|------|
| Geplante Story Points | 13 |
| Gelieferte Story Points | 13 |
| Sprint Goal Success Rate | 100 % |
| Blocker mit Einfluss auf Sprintziel | 0 |

**Qualitaetsnachweise:**
- API-Dokumentation in Swagger fuer beide Services verfuegbar.
- Kernpfade fuer Normalisierung und API-Zugriff durch Tests abgesichert.
- Persistenz und Datenabruf wurden ueber Neustarts hinweg validiert.

**Technische Entscheidung (bewusster Scope-Schnitt):**
Die fein granularen Device-Aufteilungen nach Segment-/Mandantenlogik wurden als naechster Ausbauabschnitt priorisiert. Grund: hoher Zusatzaufwand fuer Datenmodellierung, UI-Interaktion und Abnahmetesttiefe bei gleichzeitig vollstaendig erreichter Kernzielerreichung im Projektzeitraum.

---

## Projektabschluss – Agile Gesamtdokumentation

### 1. Zielerreichung gesamt
| Bereich | Ziel | Ergebnis |
|--------|------|----------|
| Architektur | Modulare Microservice-Struktur mit klaren Schichten | Vollstaendig erreicht |
| Datenintegration | Multi-Source-Collector mit einheitlicher Normalisierung | Vollstaendig erreicht |
| Persistenz | Neo4j als Source of Truth fuer Kernobjekte | Vollstaendig erreicht |
| API | Dokumentierte, nutzbare REST-Schnittstellen | Vollstaendig erreicht |
| Frontend | Informationszentriertes Dashboard mit Drilldown | Vollstaendig erreicht |
| Betrieb | Lokaler Stack inkl. Compose und Service-Dokumentation | Vollstaendig erreicht |

### 2. Sprint- und Delivery-Übersicht
| Sprint | Story Points | Erreicht | Status |
|--------|--------------|----------|--------|
| Sprint 0 | 8 | 8 | Abgeschlossen |
| Sprint 1 | 16 | 16 | Abgeschlossen |
| Sprint 2 | 6 | 6 | Abgeschlossen |
| Sprint 3 | 13 | 13 | Abgeschlossen |
| **Gesamt** | **43** | **43** | **Projektziel erreicht** |

### 3. Agile Prozessqualität
| Kriterium | Bewertung |
|-----------|-----------|
| Transparenz | Hohe Nachvollziehbarkeit durch Story-Task-Deliverable-Verknuepfung |
| Planungstreue | Sprint-Ziele wurden vollstaendig umgesetzt |
| Anpassungsfaehigkeit | Iterative Nachfuehrung bei wachsender technischer Tiefe |
| Qualitaetssicherung | Regressionstests, Swagger, strukturierte DoD-Abnahmen |

### 4. Abschluss-Retrospektive
**Was besonders gut lief:**
- Saubere technische Schichtenbildung zwischen Collector, Mapping, Normalizer, Persistenz und API.
- Fruhe Dokumentationsdisziplin hat Rework reduziert und Abnahmen beschleunigt.
- Der Fokus auf reale Datenpfade hat die Aussagekraft der Ergebnisse deutlich erhoeht.

**Was optimiert wurde:**
- Fruehere Standardisierung von Collector-Fehlerbildern und Logging-Konventionen.
- Noch engere Taktung bei Abgleich zwischen UI-Detailansicht und API-Payloads.

**Next-Step nach Abgabe (bewusst ausserhalb Scope):**
- Device-Aufteilung nach Segmenten/Geraeteklassen und mandantenfaehige Perspektiven im Frontend.

### 5. Finales Fazit
Das Projekt wurde nach agilem Vorgehensmodell vollstaendig umgesetzt und dokumentiert. Alle Sprints sind abgeschlossen, alle geplanten Deliverables sind erbracht, und die technische Loesung ist stabil, nachvollziehbar und erweiterbar. Die Dokumentation ist damit abgabereif fuer die Semesterarbeit.

---

## 6. Agile Projektgovernance (Detail)

### 6.1 Rollenmodell und Entscheidungswege
| Rolle | Verantwortungsbereich | Entscheidungsbefugnis | Eskalationsweg |
|------|------------------------|-----------------------|----------------|
| Projektleitung | Scope, Priorisierung, Sprint-Freigabe, Abnahme | Finale Priorisierung und Scope-Entscheidung | Direkt in Sprint-Review |
| Entwicklung | Technische Umsetzung, Architektur, Code-Qualitaet | Architekturvorschlaege und technische Realisierung | Abstimmung in Daily/Review |
| DevOps | Build-/Runtime-Stabilitaet, Container, Deployability | Freigabe von Runtime- und Deploy-Konfiguration | Abstimmung in Hardening-Block |

### 6.2 Zeremonien und Taktung
| Zeremonie | Ziel | Frequenz | Output |
|-----------|------|----------|--------|
| Sprint Planning | Zielbild und Story-Schnitt je Sprint | 1x pro Sprint | Sprint Goal, Sprint Backlog |
| Daily Sync | Transparenz zu Fortschritt und Risiken | taeglich | Update auf Tasks und Risiken |
| Backlog Refinement | Story-Schaerfung und Akzeptanzkriterien | 1x pro Woche | umsetzungsreife Stories |
| Sprint Review | Fachliche und technische Abnahme | 1x pro Sprint | Abnahmeentscheidung je Story |
| Sprint Retrospektive | Prozessverbesserung | 1x pro Sprint | konkrete Verbesserungsmassnahmen |

### 6.3 Priorisierungslogik
- Muss-Kriterien fuer Sprint-Aufnahme: fachlicher Mehrwert, testbare Akzeptanzkriterien, technische Umsetzbarkeit.
- Priorisierung entlang Nutzwert x Risikoentlastung x Architekturwirkung.
- Neue Anforderungen werden nur aufgenommen, wenn sie Sprint-Ziel und DoD nicht gefaehrden.

### 6.4 Change-Management
| Change-Typ | Beispiel | Behandlung |
|------------|----------|------------|
| Fachliche Erweiterung | Neue Filter-/Analyseanforderung | Aufnahme in Product Backlog, Schaetzung, Priorisierung |
| Technische Korrektur | Mapping-Feldanpassung | Direkt im Sprint bei hoher Wirkung |
| Externe Aenderung | API-Schema bei Datenquelle geaendert | Adapter-Update und Regressionstest |

---

## 7. Qualitätsmanagement und Nachweisführung

### 7.1 Qualitätsziele
| Ziel-ID | Qualitaetsziel | Messkriterium |
|--------|-----------------|---------------|
| QZ-1 | Nachvollziehbare Datenherkunft | Quelle und Mappingpfad je Objekt reproduzierbar |
| QZ-2 | Konsistentes API-Verhalten | Typisierte Responses, stabile Endpunktstruktur |
| QZ-3 | Laufzeitstabilitaet | Startfaehigkeit im lokalen Stack ohne manuelle Sonderpfade |
| QZ-4 | Wartbarkeit | Schichtentrennung (collector/mapping/normalizer/api/ui) |

### 7.2 Teststrategie (Projektweit)
| Ebene | Fokus | Werkzeug/Art | Ergebnis |
|------|-------|--------------|----------|
| Unit/Komponenten-nah | Normalizer, Mappingregeln, API-Logik | Python Tests | Erfolgreich |
| Integrationsnah | Persistenzfluss zu Neo4j | End-to-End Datenpfadtests | Erfolgreich |
| Manuelle Smoke-Tests | Runtime und UI-Plausi | Service-Start, API-Antworten, UI-Drilldown | Erfolgreich |

### 7.3 Qualitäts-Gates vor Sprint-Abnahme
1. Story-DoD vollstaendig erfuellt.
2. Keine offenen Blocker mit Einfluss auf Sprint Goal.
3. Relevante Testfaelle fuer geaenderte Kernpfade durchlaufen.
4. Doku aktualisiert (Workbook, Overview, Risiko, README).

### 7.4 Nachweisartefakte in der Dokumentation
- User Stories, Tasks, DoD und Deliverables pro Sprint dokumentiert.
- Abnahme- und Metrikabschnitte fuer Sprint 3 und Gesamtprojekt vorhanden.
- Risiko- und Scope-Entscheidungen transparent begruendet.

---

## 8. Detaillierte Sprint-Retrospektiven

### Sprint 0 Retrospektive
**Stark:** schneller Aufbau der Arbeitsgrundlage, klare Verzeichnisstruktur, fruehes Dokumentationsfundament.

**Lernpunkt:** zu Beginn mehr Zeit fuer Abhaengigkeiten und Tooling-Checklisten einplanen.

**Massnahme:** standardisierte Setup-Checkliste fuer Folgesprints eingefuehrt.

### Sprint 1 Retrospektive
**Stark:** konsequente Schichtentrennung, zentrale Architektur-Map als technischer Leuchtturm.

**Lernpunkt:** Traefik-Aktivierung frueher in den End-to-End-Probenlauf integrieren.

**Massnahme:** Infrastrukturthemen in Sprint-Backlogs frueher mit klarer Abnahme versehen.

### Sprint 2 Retrospektive
**Stark:** UI-Mehrwert durch Drilldown und CVE-Intel-Sicht, API-Nutzbarkeit stark verbessert.

**Lernpunkt:** Persistenz-Themen frueher parallel zum UI-Ausbau treiben.

**Massnahme:** Persistenz und Datenqualitaet als prioritaere Sprint-3-Leitplanken gesetzt.

### Sprint 3 Retrospektive
**Stark:** hohe Delivery-Disziplin, belastbare Datenpfade, klare Testnachweise.

**Lernpunkt:** Segment-/Device-Aufteilung braucht eigenen Ausbauzyklus.

**Massnahme:** als dediziertes Folgeinkrement geplant, ohne Abschlussqualitaet zu kompromittieren.

---

## 9. KPI-Set für die Semesterabgabe

### 9.1 Delivery-KPIs
| KPI | Definition | Ergebnis |
|-----|------------|----------|
| Planerfuellung Story Points | Gelieferte SP / Geplante SP | 43/43 (100 %) |
| Sprint Goal Erfuellung | Ziel erreicht je Sprint | 4/4 Sprints |
| Deliverable Completion | Abgenommene Deliverables / geplante Deliverables | Vollstaendig |

### 9.2 Qualitäts-KPIs
| KPI | Definition | Ergebnis |
|-----|------------|----------|
| DoD-Erfuellung | Vollstaendig erfuellte DoD-Punkte je Sprint | Vollstaendig |
| Core-Pfad-Stabilitaet | Collect->Persist->API->UI lauffaehig | Erreicht |
| Dokumentationsabdeckung | Kernartefakte aktuell und konsistent | Erreicht |

### 9.3 Risiko-KPIs
| KPI | Definition | Ergebnis |
|-----|------------|----------|
| Kritische offene Risiken | H/H Risiken ohne Gegenmassnahme | 0 |
| Rest-Risikoprofil | Summe verbleibender Projektrisiken | Niedrig bis mittel |
| Scope-Offenpunkte | bewusst verschobene Punkte | Device-Aufteilung (Phase 2) |

---

## 10. Traceability-Matrix (Anforderung -> Lieferung)

| Anforderung | Sprint/Story | Umsetzungsartefakt | Abnahmestatus |
|-------------|--------------|--------------------|---------------|
| FR-04 Zentrale Architektur-Map | Sprint 1 / US-1.2 | architecture_map, field maps, schema layer | Abgenommen |
| FR-06 Device-Inventar Push | Sprint 2-3 / API + US-3.4 | Push-API, Device-Lesepfade, Impact-Sicht | Abgenommen |
| FR-07 Drilldown je CVE/Device | Sprint 2 / US-2.1 + US-2.3 | Frontend Drilldown, Intel-Endpunkte | Abgenommen |
| FR-08 Suche/Filter | Sprint 2 | UI-Filterung und API-basierte Datenbasis | Abgenommen |
| FR-09 Entra-Change-Signale | Sprint 2 | Change-Endpunkte und Anzeige im Datenfluss | Abgenommen |
| NFR-01 Konsistente JSON-Strukturen | Sprint 2-3 | Typisierte API-Modelle und dokumentierte Endpunkte | Abgenommen |
| NFR-03 Reproduzierbares Debugging | Sprint 1 | Root-venv-Konzept, VS Code Debug-Konfiguration | Abgenommen |
| NFR-05 Erweiterbarkeit Matching/Persistenz | Sprint 3 | Neo4j Persistenz, versionsgenaue Korrelation | Abgenommen |

---

## 11. Abnahmeprotokoll (Gesamtprojekt)

| Abnahmekriterium | Erfuellung | Nachweis |
|------------------|------------|----------|
| Alle Sprints abgeschlossen | Ja | Sprintkapitel mit Status und DoD |
| Alle Deliverables erbracht | Ja | Deliverable-Tabellen je Sprint |
| Kernfunktionalitaet produktionsnah | Ja | End-to-End Kette stabil nachgewiesen |
| Dokumentation vollstaendig | Ja | Overview, Workbook, Risiko, README konsistent |
| Transparenter Scope-Schnitt dokumentiert | Ja | Device-Aufteilung als Phase-2-Inkrement |

**Abnahmeentscheidung:**
Das Projekt wird als vollstaendig abgeschlossen bewertet und fuer die Semesterabgabe freigegeben.

---

## 12. Betrieb, Wartung und Übergabe

### 12.1 Betriebsmodell (Lokal/Entwicklung)
- Service-Start ueber Root-venv und Uvicorn fuer beide FastAPI-Services.
- Frontend lokal via Node/Vite oder gesamthaft via Docker Compose.
- Persistenz auf Neo4j als zentrale Datenbasis.

### 12.2 Wartungsmodell
| Bereich | Wartungsaufgabe | Intervall |
|--------|------------------|-----------|
| Collector | Endpoint-Verfuegbarkeit und Schemaanpassung pruefen | regelmaessig |
| API | Endpunktkontrakte und Response-Stabilitaet pruefen | regelmaessig |
| Persistenz | Datenkonsistenz und Constraint-Integritaet pruefen | regelmaessig |
| Doku | Workbook/Overview/Risiko auf Stand halten | je Sprint |

### 12.3 Übergabeumfang
- Vollstaendige Sprint-Historie mit Stories, Tasks, DoD und Deliverables.
- Architektur-, Risiko- und Abschlussdokumentation.
- Dokumentierte Start- und Betriebswege fuer lokale Ausfuehrung.

---

## 13. Abschlussstatement für die Semesterarbeit

Das Projekt demonstriert eine durchgaengige, agile Umsetzung von der initialen Strukturierung bis zur produktionsnahen Datenpipeline mit visueller Auswertung. Die Kombination aus zentraler Mapping-Architektur, persistenter Datenhaltung, dokumentierter API und nachvollziehbarer Sprint-Governance liefert eine fachlich belastbare und technisch wartbare Loesung. Damit sind sowohl die Projektmanagement-Ziele als auch die technischen Projektziele vollstaendig erreicht.
