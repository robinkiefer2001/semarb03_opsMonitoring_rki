# Projektarbeitsbuch (Sprint-Dokumentation)

## Sprint 0 – Projektinitialisierung & Setup (2 Wochen)

**Sprint-Ziel:** Projektstruktur, Tools und Grundarchitektur stehen, erste Doku und CI/CD konzipiert

**Status:** Sprint abgeschlossen (alle Ziele und Deliverables erreicht)

**Epics und User Stories:**
| Epic | Story-ID | Rolle | Als [Rolle] möchte ich... | ...damit... | Akzeptanzkriterien | Story Points |
|------|----------|-------|--------------------------|-------------|-------------------|--------------|
| Setup | US-0.1 | Projektleiter | Als Projektleiter möchte ich ein zentrales GitLab-Repo anlegen | damit alle Projektdateien versioniert sind | Repo existiert, ist erreichbar, .gitignore vorhanden | 1 |
| Setup | US-0.2 | Entwickler | Als Entwickler möchte ich die Projektstruktur und Doku anlegen | damit die Entwicklung strukturiert starten kann | Verzeichnisstruktur, README, Doku-Templates vorhanden | 2 |
| Setup | US-0.3 | Projektleiter | Als Projektleiter möchte ich ein Hetzner-Projekt und Jira-Board anlegen | damit Infrastruktur und Aufgaben gemanagt werden | Hetzner-Projekt und Jira-Board existieren | 2 |
| Architektur | US-0.4 | Entwickler | Als Entwickler möchte ich die Architektur und das DB-Schema planen | damit die technische Basis klar ist | Architekturdiagramm, ERD, Tech-Stack-Tabelle vorhanden | 2 |
| CI/CD | US-0.5 | Entwickler | Als Entwickler möchte ich eine CI/CD Pipeline konzipieren | damit automatisiertes Deployment möglich ist | .gitlab-ci.yml Template vorhanden | 1 |

**Tasks (hierarchisch nach User Story):**
| Parent Story | ID | Beschreibung | Verantwortlich | Geschätzter Aufwand (h) | Status |
|--------------|----|--------------|----------------|------------------------|--------|
| US-0.1 | T0.1 | GitLab Repo erstellen | Robin Kiefer | 1 | Abgeschlossen |
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
| US-0.5 | T0.9 | .gitlab-ci.yml Template anlegen | Robin Kiefer | 1 | Abgeschlossen |

**Definition of Done (DoD):**
- [x] GitLab Repo existiert und ist erreichbar
- [x] Projektstruktur und Doku-Templates angelegt
- [x] Hetzner-Projekt und Jira-Board existieren
- [x] Architekturdiagramm und ERD vorhanden
- [x] Tech-Stack und .gitlab-ci.yml Template erstellt

**Deliverables:**
| Nr. | Deliverable | Story | Beschreibung | Erfolgskriterium |
|-----|-------------|-------|--------------|-----------------|
| D0.1 | GitLab Repo | US-0.1 | Zentrales Repository | Repo existiert, .gitignore vorhanden |
| D0.2 | Projektstruktur & Doku | US-0.2 | Verzeichnisstruktur, README, Doku-Templates | Struktur und Templates vorhanden |
| D0.3 | Hetzner-Projekt & Jira | US-0.3 | Projekt und Board angelegt | Zugang vorhanden |
| D0.4 | Architektur & ERD | US-0.4 | Diagramm und Datenbankschema | Skizzen vorhanden |
| D0.5 | CI/CD Template | US-0.5 | .gitlab-ci.yml | Datei vorhanden |

**Story Points Total:** 8

---

## Sprint 1 – Application Logik (2 Wochen)

**Sprint-Ziel:**
Grundlegende API-Logik und Backend-Funktionen mit Python (FastAPI) implementieren.

**Epics und User Stories:**
| Epic | Story-ID | Rolle | Als [Rolle] möchte ich... | ...damit... | Akzeptanzkriterien | Story Points |
|------|----------|-------|--------------------------|-------------|-------------------|--------------|
| Backend | US-1.1 | Entwickler | Als Entwickler möchte ich eine API-Grundstruktur mit FastAPI anlegen | damit das Backend modular erweiterbar ist | FastAPI-Projektstruktur vorhanden, lauffähig | 2 |
| Backend | US-1.2 | Entwickler | Als Entwickler möchte ich erste Endpunkte für das Monitoring implementieren | damit Daten abgerufen werden können | Mind. 1 GET-Endpunkt, Rückgabe von Testdaten | 2 |
| Backend | US-1.3 | Entwickler | Als Entwickler möchte ich Logging und Fehlerbehandlung integrieren | damit Fehler nachvollziehbar sind | Logging vorhanden, Fehler werden geloggt | 1 |
| Backend | US-1.4 | Entwickler | Als Entwickler möchte ich Unit-Tests für die API schreiben | damit die API zuverlässig ist | Mind. 1 Testfall pro Endpunkt | 1 |

**Tasks:**
| Parent Story | ID | Beschreibung | Verantwortlich | Geschätzter Aufwand (h) | Status |
|--------------|----|--------------|----------------|------------------------|--------|
| US-1.1 | T1.1 | FastAPI-Projektstruktur anlegen | Robin Kiefer | 2 | Offen |
| US-1.2 | T1.2 | Endpunkt für Health-Check implementieren | Robin Kiefer | 1 | Offen |
| US-1.2 | T1.3 | Endpunkt für Monitoring-Daten schreiben | Robin Kiefer | 2 | Offen |
| US-1.3 | T1.4 | Logging und Fehlerbehandlung integrieren | Robin Kiefer | 1 | Offen |
| US-1.4 | T1.5 | Unit-Tests für API schreiben | Robin Kiefer | 2 | Offen |

**Definition of Done (DoD):**
- [ ] FastAPI-Projektstruktur vorhanden und lauffähig
- [ ] Mind. 1 GET-Endpunkt implementiert
- [ ] Logging und Fehlerbehandlung integriert
- [ ] Unit-Tests vorhanden

**Deliverables:**
| Nr. | Deliverable | Story | Beschreibung | Erfolgskriterium |
|-----|-------------|-------|--------------|-----------------|
| D1.1 | FastAPI-Backend | US-1.1 | Grundstruktur Backend | Projekt läuft lokal |
| D1.2 | Monitoring-API | US-1.2 | Erste Endpunkte | Testdaten abrufbar |
| D1.3 | Logging & Fehler | US-1.3 | Logging integriert | Fehler werden geloggt |
| D1.4 | API-Tests | US-1.4 | Unit-Tests | Tests laufen fehlerfrei |

**Story Points Total:** 6

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
