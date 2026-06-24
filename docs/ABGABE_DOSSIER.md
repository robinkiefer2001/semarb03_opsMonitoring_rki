# ABGABE DOSSIER - Semesterarbeit OpsMonitoring RKI

## 1. Management Summary

Das Projekt OpsMonitoring RKI wurde als agil gefuehrtes, inkrementelles Entwicklungsprojekt mit vier abgeschlossenen Sprints realisiert. Ziel war der Aufbau einer belastbaren End-to-End-Loesung zur Verarbeitung und Visualisierung von Advisory-, CVE- und Device-Daten aus mehreren Quellen. Das Ergebnis ist eine modular aufgebaute Plattform mit klar getrennten Verantwortungsbereichen (Collector, Mapping, Normalisierung, Persistenz, API, UI), reproduzierbarer Laufzeitumgebung und vollstaendiger Projektdokumentation.

Die Lieferung ist hinsichtlich Sprint-Zielen, Deliverables und Qualitaetskriterien abgeschlossen. Als bewusst dokumentierte Erweiterung fuer eine Folgephase bleibt die fein granulare Device-Segmentierung.

## 2. Projektkontext und Problemstellung

IT-Sicherheitsverantwortliche muessen in kurzer Zeit verifizieren, welche Assets von neuen Schwachstellen betroffen sind. In der Praxis liegen dazu heterogene Datenquellen vor, die unterschiedliche Formate, Felder und Qualitaetsniveaus besitzen. Ohne Vereinheitlichung ist eine konsistente Risikoaussage schwer moeglich.

Das Projekt adressiert diese Luecke durch:
- standardisierte Erfassung aus mehreren Quellen,
- zentral definierte Feldabbildung und Normalisierung,
- persistente Speicherung in einem Graphmodell,
- API-gestuetzte Bereitstellung und
- visuelle Drilldown-Analysen im Frontend.

## 3. Projektziele und Scope

### 3.1 Zielsystem
| Ziel-ID | Zielbeschreibung | Ergebnis |
|--------|-------------------|----------|
| Z1 | Sicherheitslage aus mehreren Quellen konsolidieren | Erreicht |
| Z2 | Device-Inventar integrieren und gegen Risiken abgleichen | Erreicht |
| Z3 | Nachvollziehbare Drilldown-Ansichten bereitstellen | Erreicht |
| Z4 | API-first mit dokumentierter Schnittstelle bereitstellen | Erreicht |

### 3.2 Scope-Statement
Im Scope enthalten:
- Multi-Source-Collector und Normalisierung,
- persistente Speicherung der Kernobjekte,
- API-Endpunkte fuer Uebersicht, Detail und Impact,
- Dashboard-orientierte Visualisierung,
- agile Artefakte inklusive Abnahme- und Risikodokumentation.

Bewusst ausserhalb des Abschluss-Scope:
- Device-Aufteilung nach segmentierter, mandantenfaehiger Darstellung (Phase 2).

## 4. Vorgehensmodell und Organisation

### 4.1 Agiles Vorgehen
Das Projekt wurde in vier Sprints mit klaren Sprint-Zielen, Story-Paketen und Definition-of-Done-Kriterien durchgefuehrt. Die Steuerung erfolgte ueber transparente Story-Task-Deliverable-Hierarchie.

### 4.2 Rollen und Verantwortlichkeiten
| Rolle | Verantwortung |
|------|----------------|
| Projektleitung | Priorisierung, Scope-Steuerung, Abnahme |
| Entwicklung | Umsetzung Backend, Collector, API, Frontend |
| DevOps | Containerisierung, Runtime-Konfiguration, Deployability |

### 4.3 Governance-Grundsaetze
- Entscheidungen folgen der Priorisierungslogik aus Nutzen, Risikoentlastung und Integrationswirkung.
- Neue Anforderungen werden nur bei gesicherter DoD-Erfuellung aufgenommen.
- Dokumentation wird sprintnah gepflegt, um Nachvollziehbarkeit sicherzustellen.

## 5. Technische Architektur auf Management-Ebene

### 5.1 Architekturprinzipien
- Schichtentrennung statt monolithischer Vermischung.
- Zentrale Definitionen fuer Mapping und Normalisierung.
- Persistenz als gemeinsame Datenbasis fuer nachgelagerte Services.
- API als verbindliches Integrationsinterface.

### 5.2 Datenfluss
1. Externe Feeds werden durch Collector-Adapter gelesen.
2. Daten werden ueber Architektur-Map und Mappinglogik vereinheitlicht.
3. Normalisierte Objekte werden in Neo4j persistiert.
4. API stellt Aggregationen und Detailinformationen bereit.
5. Frontend liefert interaktive Sicht auf Lagebild und Betroffenheit.

### 5.3 Nicht-funktionale Qualitaeten
- Reproduzierbare lokale Startfaehigkeit.
- Konsistente API-Vertraege.
- Erweiterbarkeit fuer neue Quellen und Felder.
- Wartbarkeit durch modulare Struktur.

## 6. Sprintbilanz und Delivery-Performance

| Sprint | Schwerpunkt | Story Points | Status |
|--------|------------|--------------|--------|
| Sprint 0 | Initialisierung, Struktur, Doku, CI/CD | 8 | Abgeschlossen |
| Sprint 1 | Monorepo, Architektur-Map, Infrastrukturgrundlage | 16 | Abgeschlossen |
| Sprint 2 | UI, API-Doku, Containerbetrieb | 6 | Abgeschlossen |
| Sprint 3 | Datenqualitaet, Persistenz, Testing, Matching | 13 | Abgeschlossen |
| Gesamt | End-to-End-Plattform | 43 | Abgeschlossen |

Kernaussage:
- Planerfuellung: 100 %
- Sprint Goal Success: 4 von 4
- Deliverable Completion: vollstaendig

## 7. Qualitäts- und Abnahmekonzept

### 7.1 Qualitätsdimensionen
| Dimension | Ziel |
|----------|------|
| Funktional | Stories liefern den geplanten Fachnutzen |
| Technisch | End-to-End-Fluss stabil und wartbar |
| Prozessual | Sprintartefakte und DoD lueckenlos |
| Dokumentarisch | Nachweisfuehrung ueber alle Projektphasen |

### 7.2 Abnahmelogik
Abnahme erfolgt pro Story auf Basis von:
- verifizierbaren Akzeptanzkriterien,
- bestandenen Kern-Tests,
- aktualisierter Projektdokumentation.

### 7.3 Abschlussabnahme
Die Abschlussabnahme bestaetigt:
- Erfuellung aller Sprintziele,
- Erbringung aller geplanten Deliverables,
- konsistente Projektdokumentation,
- transparent dokumentierten Scope-Schnitt fuer Phase 2.

## 8. Risiko- und Stabilitaetsbewertung

### 8.1 Ergebnis nach Projektabschluss
Das Rest-Risikoprofil ist niedrig bis mittel. Kritische, unbehandelte Risiken mit direkter Gefaehrdung des Projektziels bestehen nicht.

### 8.2 Verbleibende Ausbaupunkte
Der einzig bewusst verschobene Ausbauschritt betrifft die Device-Segmentierung nach Klassen/Mandantenansicht. Dies ist fachlich sinnvoll, jedoch nicht kritisch fuer den Kernnutzen der gelieferten Plattform.

## 9. Wirtschaftliche und organisatorische Bewertung

### 9.1 Nutzenbeitrag
- Schnellere Lageeinschaetzung fuer Schwachstellenkontexte.
- Nachvollziehbare Betroffenheitsdarstellung auf Device-Ebene.
- Hohe Wiederverwendbarkeit durch API-first und modulare Architektur.

### 9.2 Nachhaltigkeit
- Neue Datenquellen koennen adapterbasiert erweitert werden.
- Wartung erfolgt schichtenspezifisch ohne Grossumbauten.
- Dokumentierte Betriebswege unterstuetzen Uebergabe und Weiterentwicklung.

## 10. Erweiterungsroadmap nach Abgabe

| Phase | Schwerpunkt | Erwarteter Mehrwert |
|------|-------------|---------------------|
| Phase 2 | Device-Segmentierung und mandantenfaehige Aufteilung | Praezisere Verantwortlichkeits- und Sichtsteuerung |
| Phase 2 | Zusatzauthentifizierung fuer Produktivfeeds | Erhoehte Datenabdeckung und Stabilitaet |
| Phase 2 | Erweiterte Reporting-Sichten | Verbesserte Governance- und Audit-Faehigkeit |

## 11. Schlussfazit

OpsMonitoring RKI ist als Semesterprojekt fachlich und technisch vollstaendig geliefert. Die Loesung verbindet agile Projektsteuerung mit belastbarer technischer Umsetzung und klarer Nachweisfuehrung. Das Ergebnis ist abgabereif, erweiterbar und in seiner Kernfunktionalitaet nachhaltig nutzbar.
