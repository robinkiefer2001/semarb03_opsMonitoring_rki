# PROJECT_OVERVIEW.md

## 1. Vision und Ziele
| Ziel | Beschreibung | Priorität |
|------|--------------|-----------|
| Z1 | Security-Lagebild mit CVE/Advisory-Daten aus mehreren Quellen bereitstellen | Hoch |
| Z2 | Device-Inventar pushen, durchsuchen und gegen aktuelle Risiken abgleichen | Hoch |
| Z3 | Inspect-UI mit nachvollziehbarer Betroffenheit pro CVE, Advisory und Asset anbieten | Hoch |
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
Neo4j ist als persistente Datenbank fuer Snapshot-, Advisory-, CVE-, Vendor- und Device-Daten aktiv angebunden.
Der API-Service nutzt weiterhin einen kleinen In-Memory Cache zur Laufzeithydrierung, liest aber den persistierten Bestand aus Neo4j nach.

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
| Laufzeit lokal | Docker Compose oder Root-venv + Uvicorn + Vite |
| API Service | http://localhost:8002 |
| Data Collector | http://localhost:8001 |
| Webapp | http://localhost:8080 (Docker) / http://localhost:5173 (Vite Dev) |
| Neo4j Browser | http://localhost:7474 |
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
Abgeschlossen: Monorepo-Struktur, Architektur-Map, Collector-Layer, Mapping/Normalizer, Basis-API und Debug-Setup umgesetzt.

### Sprint 2
Abgeschlossen: modernes Frontend, Inventory/Impact APIs, CVE-Intel-/Inspect-Fenster, Docker-Stack, Swagger und lokale Betriebsfaehigkeit umgesetzt.

### Sprint 3
Abgeschlossen: Datenqualitaet gehaertet, Neo4j-Persistenz produktiv eingebunden, API-/Normalizer-Regressionstests erfolgreich, reale Asset-Inventardaten integriert und End-to-End-Betrieb stabilisiert.

### Projektabschluss-Hinweis
Die Aufteilung auf Device-Klassen und mandantenfaehige Device-Segmentierung wurde als bewusstes Follow-up nach Projektabgabe eingeplant, da Umsetzungstiefe und Testaufwand im gegebenen Zeitrahmen unverhaeltnismaessig hoch waren.

## 14. Risiken und Herausforderungen
| Risiko | Wahrscheinlichkeit | Impact | Mitigation |
|--------|-------------------|--------|------------|
| Externe Feeds temporaer nicht verfuegbar | Niedrig | Mittel | Retry-Strategien, ingest-orientierter Sammelzyklus, robuste Fehlerbehandlung |
| Device-Aufteilung nach Segmenten/Geraeteklassen als spaetere Ausbaustufe | Mittel | Niedrig | Als Phase-2-Inkrement geplant; Kernfunktionalitaet bleibt voll verifizierbar |
| Herstellerseitige API-Aenderungen | Niedrig | Mittel | Versionierte Adapterstruktur pro Collector und fruehzeitige Endpoint-Validierung |

## 15. Agile Steuerung und Projektkontrolle

### 15.1 Steuerungsmodell
- Sprintbasierte Umsetzung mit klaren Sprintzielen und messbaren Abnahmekriterien.
- Transparente Story-Task-Deliverable-Hierarchie fuer durchgaengige Nachvollziehbarkeit.
- Priorisierung nach Nutzenbeitrag, Risikoentlastung und Integrationswirkung.

### 15.2 Meilensteine
| Meilenstein | Inhalt | Status |
|-------------|--------|--------|
| M1 | Projektgrundlage, Repo, Doku-Setup, CI/CD-Entwurf | Erreicht |
| M2 | Architektur-Map und Schichtentrennung im Monorepo | Erreicht |
| M3 | API- und UI-Nutzwert mit dokumentierter Schnittstelle | Erreicht |
| M4 | Persistenz, Datenqualitaet und testgestuetzte Stabilitaet | Erreicht |

### 15.3 KPI-Snapshot
| KPI | Wert |
|-----|------|
| Geplante Story Points gesamt | 43 |
| Gelieferte Story Points gesamt | 43 |
| Sprint Goal Success | 100 % |
| Offene kritische Risiken | 0 |

## 16. Qualitätskonzept

### 16.1 Qualitätsziele
| Ziel | Auspraegung |
|------|-------------|
| Datenqualitaet | Keine Demo-/Placeholder-Daten im Standardpfad |
| API-Qualitaet | Konsistente, dokumentierte Endpunkte und Antwortstrukturen |
| Betriebsqualitaet | Reproduzierbarer Start und stabiler lokaler Stack |
| Wartbarkeit | Klare Schichtentrennung und modulare Erweiterbarkeit |

### 16.2 Qualitätssicherungsmassnahmen
- Regelmaessige Regressionstests fuer Kernpfade.
- Sprintweise DoD-Abnahme auf Story-Ebene.
- Dokumentationspflege in Overview, Workbook und Risikotabelle.
- Konsistente Schnittstellenbeschreibung via Swagger.

## 17. Abnahmekriterien (Gesamtprojekt)

| Kriterium | Nachweis | Ergebnis |
|-----------|----------|----------|
| Alle Sprints abgeschlossen | Sprint-Status in Workbook und README | Erfuellt |
| Deliverables vollstaendig | Deliverable-Tabellen pro Sprint | Erfuellt |
| End-to-End Datenfluss stabil | Collect -> Normalize -> Persist -> API -> UI | Erfuellt |
| Dokumentation konsistent | Overview, Workbook, Risiko, Dossier | Erfuellt |
| Scope-Schnitt transparent | Device-Aufteilung als Phase-2-Inkrement dokumentiert | Erfuellt |

## 18. Betrieb und Wartung

### 18.1 Betriebsfaehigkeit
- Lokaler Betrieb via Root-venv und Service-Startprofilen.
- Alternativ gesamthaft via Docker Compose.
- Persistenz in Neo4j als belastbare Datenbasis.

### 18.2 Wartungsmodell
| Bereich | Aufgabe | Turnus |
|--------|---------|--------|
| Collectors | Endpoint- und Schema-Validierung | regelmaessig |
| Mapping/Normalizer | Feldkonsistenz bei Quellenaenderungen | regelmaessig |
| API | Vertragsstabilitaet und Dokumentation | regelmaessig |
| Infrastruktur | Compose/Runtime-Smoketests | regelmaessig |

## 19. Ausblick

Der naechste Ausbauschritt nach Abgabe fokussiert auf die Device-Aufteilung nach Segmenten und mandantenfaehigen Sichten. Diese Erweiterung erhoeht Governance- und Auswertungsgranularitaet, ohne den aktuell erreichten Kernnutzen einzuschraenken.

## 20. Abschlussstatement

Das Projekt erreicht die gesetzten fachlichen und technischen Ziele vollstaendig. Die Loesung ist stabil, nachvollziehbar dokumentiert und fuer den weiteren Ausbau vorbereitet. Die Unterlagen bilden damit eine vollstaendige, hochwertige Grundlage fuer die Semesterabgabe.
