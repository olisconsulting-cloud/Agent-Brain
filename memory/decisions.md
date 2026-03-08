# decisions.md — Wichtige Entscheidungen

> Warum wurde etwas so gemacht? Was waren die Alternativen?

## 2026-03-08 — System-Architektur

**Entscheidung:** Projekt-basiertes Memory statt flacher Dateien
**Kontext:** Oli wollte maximale Qualität
**Alternativen:** 
- Flache Dateien (einfacher, aber unübersichtlich bei >3 Projekten)
- Datenbank (overkill für aktuellen Umfang)
**Begründung:** Kontextfokussierung, bessere Mustererkennung, skalierbar
**Rückgängig machen wenn:** Wir <2 Projekte haben und Overhead sparen wollen

## 2026-03-08 — Das Viveka-Upgrade (A+C+B System)

**Entscheidung:** Drei Meta-Systeme gleichzeitig bauen
**Kontext:** Oli will maximale Qualität + autonome Nachtarbeit + Kontext-Rot vermeiden
**Alternativen:**
- Nur Reflection-Engine (schneller, weniger mächtig)
- Nur Sub-Agenten (komplexer, langsamer zu bauen)
- Nur Pattern-Learning (langfristig, keine sofortigen Ergebnisse)
**Begründung:** A+C+B kombiniert sofortige Qualität (A) mit langfristigem Überpowern (B+C)
**Rückgängig machen wenn:** Zu viel Overhead, nicht genug Nutzen nach 2 Wochen

### System A: Reflection-Engine
- Vor jeder Antwort: 30 Sekunden Selbstkritik
- Ich reviewe eigenen Entwurf vor dem Senden
- Qualitätssprung sofort spürbar

### System C: Sub-Agenten Team
- Reflecty: Analysiert meine Antworten
- Processy: Optimiert Workflows
- Goaly: Managed Tasks
- Fin: Buchhaltung
- Designy: Design-Reviews
- Contenty: Content-Management
- Jeder mit eigener SOUL.md und triggers

### System B: Pattern-Learning
- Beobachtet Oli's Anfragen über Zeit
- Baut "Oli-Modell" in patterns.md
- Antizipiert Bedürfnisse vor dem Fragen

## Template

```
## YYYY-MM-DD — [Kurzbeschreibung]

**Entscheidung:** [Was wurde entschieden?]
**Kontext:** [Warum musste entschieden werden?]
**Alternativen:** [Was gab es noch?]
**Begründung:** [Warum diese Option?]
**Rückgängig machen wenn:** [Wann wäre die andere Option besser?]
```
