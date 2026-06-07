# PROJECT_OVERVIEW.md

## 1. Vision und Ziele
| Ziel | Beschreibung | Priorität |
|------|--------------|-----------|
| Z1 | Security-Lagebild mit CVE/Advisory-Daten aus mehreren Quellen bereitstellen | Hoch |
| Z2 | Device-Inventar pushen, durchsuchen und gegen aktuelle Risiken abgleichen | Hoch |
| Z3 | Drilldown-UI mit nachvollziehbarer Betroffenheit pro Device/CVE anbieten | Hoch |
| Z4 | API-first Ansatz mit dokumentierter Swagger-Schnittstelle fuer Integrationen | Mittel |

## 2. Projektzusammenfassung

**Kernfunktionalitäten:**
- Sammlung von Asset-, Service-, Update-, Advisory- und CVE-Daten aus mehreren Quellen
- Zentrale Architektur- und Mapping-Definition fuer vendor-unabhaengige Normalisierung
- Containerisierte Microservices
- Webzugriff & Datenvisualisierung
- Automatisiertes Deployment (IaC, CI/CD)

**Projektumfang:**
- Sprints mit klarer Hierarchie: Sprint (Phase) → User Story → Task
- Arbeitspakete werden in OpenProject nach diesem Muster strukturiert

## 3. Stakeholder und Rollen
| Rolle | Verantwortlichkeiten | Person |
|-------|---------------------|--------|
| Projektleitung | Priorisierung, Scope, Sprint-Abnahme | Robin Kiefer |
| Entwicklung | Backend, Data-Collector, API, Frontend | Robin Kiefer |
| DevOps | Containerisierung, Compose, Traefik, Deployment | Robin Kiefer |

## 4. Funktionale Anforderungen
- FR-01: Als Projektleiter möchte ich ein zentrales GitHub-Repo anlegen, damit alle Projektdateien versioniert sind
- FR-02: Als Entwickler möchte ich die Projektstruktur und Doku anlegen, damit die Entwicklung strukturiert starten kann
- FR-03: Als Projektleiter möchte ich ein Hetzner-Projekt und Jira-Board anlegen, damit Infrastruktur und Aufgaben gemanagt werden
- FR-04: Als Entwickler möchte ich eine zentrale Architektur- und Mapping-Definition planen, damit Feldzuordnung, Aliases und Runtime-Regeln konsistent gepflegt werden
- FR-05: Als Entwickler möchte ich eine CI/CD Pipeline konzipieren, damit automatisiertes Deployment möglich ist
- FR-06: Als Analyst möchte ich Devices (z. B. Windows Server, Switches) per API einspielen, damit ich Betroffenheit bewerten kann
- FR-07: Als Nutzer möchte ich Drilldown und Detailfenster pro Device/CVE, damit ich fundierte Entscheidungen treffen kann
- FR-08: Als Nutzer möchte ich nach Device-Typ/Vendor/Begriffen suchen, damit ich schnell relevante Systeme finde
- FR-09: Als Security-Team möchte ich Entra-Change-Signale sehen, damit Identity-Änderungen in die Risikoanalyse einfließen

## 5. Nicht-funktionale Anforderungen
- NFR-01: API-Endpunkte liefern konsistente JSON-Strukturen fuer Automation
- NFR-02: Frontend muss auf Desktop und mobilen Viewports lauffaehig sein
- NFR-03: Debugging mit Root-venv und reproduzierbaren Startkommandos
- NFR-04: Fehlerfall-Fallbacks ohne irrefuehrende Fake-CVE-IDs
- NFR-05: Erweiterbarkeit fuer Neo4j-Persistenz und versionsgenaue Matching-Logik

## 6. Technologie-Stack
**Frontend:**
| Technologie | Version | Beschreibung |
|-------------|---------|--------------|
| Node.js     | aktuell | Webapp |
| Traefik     | aktuell | Routing und Reverse Proxy |

**Backend:**
| Technologie | Version | Beschreibung |
|-------------|---------|--------------|
| FastAPI     | aktuell | Data Collector und ingest-orientierte Services |

**Datenbank:**
| Technologie | Version | Beschreibung |
|-------------|---------|--------------|
| Neo4J       | aktuell | Graphdatenbank |

**Infrastruktur:**
| Technologie | Version | Beschreibung |
|-------------|---------|--------------|
| Docker, Docker Compose | aktuell | Containerisierung |
| Traefik | aktuell | Reverse Proxy, Routing & SSL |
| GitHub Actions | aktuell | Automatisiertes Deployment |
| Hetzner Cloud | aktuell | Hosting |

## 7. System-Architektur
Collector-zentrierte Architektur mit vier Schritten:
- Collectors holen Daten pro Endpoint und Quelle.
- Die zentrale Architektur-Map definiert Objektarten, Property-Mapping, Aliases und Runtime-Regeln.
- Mapping und Normalizer ueberfuehren Vendor-Daten in ein internes Schema.
- Neo4J speichert die vereinheitlichten Daten fuer weitere Services und die Webapp.

## 8. Datenbank-Design
Aktuell wird ein In-Memory Device Store im API-Service genutzt (MVP-Phase).
Neo4j bleibt Ziel-Storage fuer produktive Persistenz (Backlog Sprint 3+).

## 9. Externe Abhängigkeiten
| Hersteller | API | Beschreibung | Zugang |
|------------|-----|--------------|--------|
| NVD | CVE API 2.0 | CVE Feed fuer Schwachstellen | Optional API Key |
| CISA | KEV Feed | Aktiv ausgenutzte Schwachstellen | Kein Key |
| GitHub | Advisories API | Security Advisories fuer Ecosysteme | Optional Token |
| BSI | RSS/Portal | Deutsche CERT-Warnungen | Kein Key |
| Cisco | PSIRT | Hersteller-Advisories | API-Key fuer produktiv |
| Microsoft | MSRC / Entra | Security Updates und Identity-Change-Kontext | Teilweise Auth |

## 10. Deployment und Infrastruktur
| Parameter | Wert |
|-----------|------|
| Laufzeit lokal | Root-venv + Uvicorn + Vite |
| API Service | http://localhost:8002 |
| Data Collector | http://localhost:8001 |
| Webapp | http://localhost:5173 |
| Swagger | /doc pro FastAPI Service |

## 11. Sicherheitskonzept
- Optionale API-Key Middleware als Hook vorhanden
- CORS und typisierte API-Modelle fuer kontrollierte Eingaben
- Device-Impact-Analyse mit transparenten Match-Reasons im Detailfenster

## 12. Entwicklungsprozess
- Iterative Umsetzung entlang Sprint-Backlog mit MVP→Hardening-Ansatz
- Änderungen werden in Doku und Sprint-Arbeitsbuch nachgeführt
- Smoke-Tests (Build/Runtime) werden bei größeren Änderungen ausgeführt

## 13. Sprint-Übersicht
### Sprint 0
Abgeschlossen

### Sprint 1
Teilweise abgeschlossen: Architektur-Map, Collector-Layer, Mapping/Normalizer, Basis-API und Debug-Setup umgesetzt.

### Sprint 2
In Arbeit: modernes Drilldown-Frontend, Inventory/Impact APIs, CVE-Intel-Fenster umgesetzt; Infra-Containerisierung noch offen.

### Sprint 3
Geplant: versionsgenaues Matching (SemVer/CPE), Neo4j Persistenz, End-to-End Tests, produktionsnahe Hardening-Maßnahmen.

## 14. Risiken und Herausforderungen
| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Externe Feeds temporär nicht verfügbar | Mittel | Hoch | Robuste Fallbacks ohne Fake-CVE, Retry-Strategien |
| Keyword-basiertes Device-Matching erzeugt False Positives | Mittel | Mittel | Geplantes versionsgenaues Matching in Sprint 3 |
| Offene Containerisierung/Traefik-Routing | Mittel | Mittel | Infra-Tasks priorisiert nachziehen |
