# Risikotabelle

| Risiko | Beschreibung | Wahrscheinlichkeit (H/M/N) | Impact (H/M/N) | Risikoscore | Prävention | Fallback |
|--------|-------------|--------------------------|----------------|-------------|-----------|---------|
| Hohe technische Komplexität | Viele Komponenten, viele Schnittstellen, neue Technologien | H | H | 9 | Architektur früh planen, Doku, kleine Iterationen | Expertenrat, Scope reduzieren |
| API-Änderungen/Rate Limits | Hersteller ändern APIs oder setzen Limits | M | H | 6 | API-Änderungen monitoren, Mock-APIs, Caching | Fallback-API, manueller Import |
| Zeitmanagement (Einzelperson) | Alle Rollen durch eine Person, Überlastung möglich | H | H | 9 | Realistische Planung, Puffer, Priorisierung | Aufgaben streichen, Scope anpassen |
| Deployment-Probleme (IaC/CI-CD) | Fehler in IaC, CI/CD Pipeline schlägt fehl | M | H | 6 | Automatisierte Tests, Staging-Umgebung | Manuelles Deployment, Rollback |
| Datenbankprobleme | Schema-Fehler, Performance, Neo4J-Ausfall | M | M | 4 | DB-Tests, Monitoring, Backups | Restore, Wechsel auf Ersatz-DB |
| Sicherheitslücken | API Keys, Secrets versehentlich im Git | M | H | 6 | Secrets-Management, .gitignore, Reviews | Revoke Keys, History Cleanup |
| Hersteller-APIs ohne Zugang | API nicht öffentlich, Zugang verweigert | M | M | 4 | Vorab prüfen, Alternativen recherchieren | Manuelle Datenbeschaffung |
