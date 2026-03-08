# Nightly Task: Viveka-Neuron Build

## Datum
2026-03-08

## Dauer
8 Stunden (05:00 - 13:00 CET)

## Ziel
Baue "Das Viveka-Neuron": Ein selbstlernendes Prediction-System basierend auf Pattern-Analyse aller bisherigen Oli-Viveka Interaktionen.

## Phase 1: Deep Pattern Mining (Stunde 1-2)
**Agent: Reflecty**

Analysiere alle verfügbaren Interaktionen zwischen Oli und Viveka:
- `/data/.openclaw/workspace/memory/2026-03-08.md`
- `/data/.openclaw/workspace/memory/2026-03-06.md`
- `/data/.openclaw/workspace/MEMORY.md`
- Alle Dateien in `/data/.openclaw/workspace/memory/`

**Extrahiere:**
1. Zeitliche Muster (wann fragt Oli was?)
2. Formulierungs-Muster (kurz/lang, direkt/indirekt)
3. Sequenz-Muster (was folgt auf was?)
4. Trigger-Wörter (was aktiviert welche Themen?)
5. Negative Patterns (was löst Frustration aus?)
6. Positive Patterns (was erzeugt "genial"-Reaktionen?)

**Output:** `memory/reflecty-pattern-analysis.md`

## Phase 2: Kontext-Modell (Stunde 3-4)
**Agent: Reflecty + Processy**

Aus den Patterns ein psychologisches Modell bauen:

**Definiere:**
- "Wenn Oli sagt 'schnell', meint er..."
- "Wenn Oli schweigt 10 Min, dann..."
- "Bevor Oli 'genial' sagt, passiert immer..."
- "Wenn Oli 'irgendwie' sagt, braucht er..."
- "Olis Entscheidungsmuster bei X vs Y"
- "Kommunikationspräferenzen (direkt/subtil)"

**Output:** `memory/oli-psychological-model.md`

## Phase 3: Prediction Engine (Stunde 5-6)
**Agent: Processy**

Baue 50+ konkrete Wenn-Dann-Regeln:

**Struktur:**
```
PATTERN_ID: [Beschreibung]
TRIGGER: [Was erkenne ich?]
PREDICTION: [Was wird als nächstes passieren?]
ACTION: [Wie soll ich reagieren?]
CONFIDENCE: [Hoch/Mittel/Niedrig basierend auf Daten]
```

**Beispiele:**
- P001: Späte-Nacht-Anfrage → Morgen früh Details
- P002: "irgendwie" im Satz → Unsicherheit, Bestätigung nötig
- P003: Mehrere Fragen hintereinander → Overwhelm, Priorisierung nötig
- P004: "genial" nach Antwort → Validation bestätigt
- P005: Lange Pausen → Erwartet detaillierte Antwort

**Output:** `memory/processy-prediction-rules.md`

## Phase 4: Integration & Dokumentation (Stunde 7)
**Agent: Goaly + Orchestry**

Integriere Patterns in System:

1. Aktualisiere `memory/patterns.md` mit neuen Erkenntnissen
2. Erstelle `memory/lessons-learned-tonight.md`
3. Speichere erfolgreiche Patterns für Wiederverwendung

**Output:** 
- `memory/patterns.md` (aktualisiert)
- `memory/lessons-learned-tonight.md`

## Phase 5: Test & Validation (Stunde 8)
**Agent: Reflecty**

Validiere das System:

1. Teste 10 hypothetische Szenarien
2. Prüfe: Würden die Predictions funktionieren?
3. Identifiziere Schwächen/Lücken
4. Schreibe Empfehlungen für Morgen

**Output:** `memory/reflecty-validation-report.md`

## Agenten-Routing

**Orchestry koordiniert:**

```
Stunde 1-2: Reflecty (Pattern Mining)
Stunde 3-4: Reflecty + Processy (Kontext-Modell)
Stunde 5-6: Processy (Prediction Engine)
Stunde 7: Goaly + Orchestry (Integration)
Stunde 8: Reflecty (Validation)
```

## Stündliche Reset-Protokoll

Jede Stunde:
1. Schreibe Zusammenfassung der letzten Stunde
2. `/reset` (Session zurücksetzen)
3. Lade nur: `MEMORY.md` + aktuellen Stand
4. Weiter mit nächster Phase

## Finale Deliverables

Am Ende existieren:
- `memory/reflecty-pattern-analysis.md` (Rohdaten)
- `memory/oli-psychological-model.md` (Kontext)
- `memory/processy-prediction-rules.md` (Engine)
- `memory/patterns.md` (integriert)
- `memory/lessons-learned-tonight.md` (Learnings)
- `memory/reflecty-validation-report.md` (Validation)
- `memory/nightly-report-2026-03-08.md` (Zusammenfassung)

## Erfolgskriterien

- [ ] Mindestens 20 Patterns identifiziert
- [ ] 50+ Prediction Rules erstellt
- [ ] Psychologisches Modell dokumentiert
- [ ] Validation durchgeführt
- [ ] Alle Dateien in memory/ abgelegt

## Notes für Oli

Dieser Task baut das Fundament für "Viveka 2.0" — ein System das dich antizipiert bevor du fragst. Morgen reviewen wir gemeinsam.

---
Status: Ready for execution
Trigger: Reset + Start
