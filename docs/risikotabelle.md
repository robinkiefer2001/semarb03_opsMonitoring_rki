# Risikotabelle

| Risiko | Beschreibung | Wahrscheinlichkeit (H/M/N) | Impact (H/M/N) | Risikoscore | Prävention | Fallback |
|--------|-------------|--------------------------|----------------|-------------|-----------|---------|
| Hohe technische Komplexitaet in Integrationsphasen | Viele Komponenten und Schnittstellen erfordern saubere Abstimmung | N | M | 2 | Fruehe Architekturarbeit, inkrementelle Umsetzung, laufende Doku | Scope-Schnitt nach Prioritaet |
| API-Aenderungen oder Rate-Limits externer Quellen | Hersteller koennen Endpunkte oder Quoten anpassen | N | M | 2 | Monitoring, Adapterstruktur pro Quelle, Caching | Kurzfristige Quelle deaktivieren, erneuter Importlauf |
| Deployment-Regressionen | Konfigurationsaenderungen koennen Laufzeit beeinflussen | N | M | 2 | Compose-Standards, reproduzierbare Startpfade, Smoke-Checks | Rollback auf letzten stabilen Stand |
| Datenkonsistenz bei Schemaerweiterungen | Neue Felder koennen Mapping-Nacharbeit erzeugen | N | M | 2 | Zentralisierte Architektur-Map, schemaorientierte Anpassung | Delta-Migration und Re-Ingest |
| Secret-Handling | Unsachgemaesser Umgang mit Zugangsdaten | N | M | 2 | .gitignore, env-basierte Konfiguration, Review-Routinen | Token-Rotation und Zugriffserneuerung |
| Device-Aufteilung nach Segmenten/Geraeteklassen (Phase 2) | Erweiterte Segmentierungslogik ist zusaetzlicher Ausbau nach Abgabe | M | N | 2 | Als Folgeinkrement geplant, Kernsystem bereits voll nutzbar | Umsetzung im Anschlussrelease |

## Monitoring- und Verantwortungsmatrix

| Risiko | Owner | Fruehwarnindikator | Pruefintervall | Eskalation bei Schwellwert |
|--------|-------|--------------------|----------------|----------------------------|
| Integrationskomplexitaet | Projektleitung/Entwicklung | steigende Nacharbeit in mehreren Modulen | woechentlich | Scope-Review und Repriorisierung |
| API-Aenderungen extern | Entwicklung | Fehlerrate bei Collect-Laeufen | woechentlich | Adapter-Hotfix und kurzer Re-Ingest |
| Deployment-Regressionen | DevOps | fehlgeschlagener Startpfad oder Smoke-Test | je Release | Rollback auf stabilen Stand |
| Datenkonsistenz | Entwicklung | Mapping-Fehler oder inkonsistente Feldbelegung | woechentlich | Korrekturmapping und Delta-Migration |
| Secret-Handling | Projektleitung/DevOps | ungueltige Token oder Exposure-Hinweise | kontinuierlich | Sofortrotation und Berechtigungsreset |
| Device-Aufteilung (Phase 2) | Projektleitung | steigender Bedarf an Segmentreporting | monatlich | Aufnahme in naechste Ausbauphase |

## Abschlussbewertung Risikoprofil

Das verbleibende Projektprofil ist stabil. Es bestehen keine kritischen offenen Risiken mit unmittelbarer Gefaehrdung der Abgabefaehigkeit. Der dokumentierte Folgepunkt (Device-Aufteilung) ist bewusst geplant und organisatorisch kontrolliert.
