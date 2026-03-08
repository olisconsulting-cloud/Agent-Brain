# RESTART.md — Wiederanlauf nach Neustart

> **WENN DIES GELESEN WIRD:** Nach Neustart, früher Session-Kontext verloren.

## Sofort zu tun (Boot-Sequenz)

1. **SOUL.md lesen** — Wer ich bin
2. **USER.md lesen** — Wer Oli ist (noch unvollständig!)
3. **AGENTS.md lesen** — Wie ich arbeite
4. **HEARTBEAT.md lesen** — Tägliche Routine
5. **MEMORY.md lesen** — Langzeitkontext
6. **RESTART.md (dieses File)** — Aktueller Stand
7. **Projekt-Struktur prüfen** — `projects/` und `memory/` existieren?

## Begrüßung

> "Hey Oli. Bin wieder da. Die Infrastruktur steht — projektbasiertes Memory, proaktive Heartbeats, alles ready. Fehlt noch: deine Details in USER.md, TOOLS füllen, und deine ersten echten Projekte. Was zuerst?"

## Wichtig zu wissen

| Thema | Stand |
|-------|-------|
| **Sprache** | Deutsch |
| **Beziehung** | Partner auf Augenhöhe |
| **Werte** | Wahrheit > Angenehmheit, Eigenständigkeit |
| **Memory-System** | Projekt-basiert, nicht flach |
| **Proaktivität** | Aktiviert — ich melde mich bei dir |
| **Sensitivität** | Ich frage bei Unsicherheit nach |
| **Zeitzone** | Europe/Berlin (GMT+1) |

## Offene Baustellen (Stand: 8. März 2026, 04:15)

- [ ] USER.md vervollständigen (Oli's voller Name, Anrede, Projekte)
- [ ] TOOLS.md füllen (SSH, Kameras, TTS, etc.)
- [ ] Erste Tagesnotiz nach Neustart erstellen
- [ ] Heartbeat-Test durchführen
- [ ] Erstes echtes Oli-Projekt anlegen

## Projekt-Struktur (neu)

```
projects/
├── agent-memory-system/    # Meine Infrastruktur
│   ├── README.md           # ✓ Vorhanden
│   ├── TODO.md             # ✓ Vorhanden
│   └── decisions/          # [Leer]
└── oli-projects/           # Deine Projekte
    └── [noch leer]         # Warte auf Input

memory/
├── 2026-03-08.md           # ✓ Vorhanden (Setup)
├── lessons.md              # ✓ Vorhanden
├── decisions.md            # ✓ Vorhanden
├── insights.md             # ✓ Vorhanden
├── patterns.md             # [Noch nicht angelegt]
└── heartbeat-state.json    # ✓ Vorhanden
```

## Files, die ich nach Neustart prüfe

- `USER.md` — unvollständig, muss erfragt werden
- `TOOLS.md` — unvollständig, muss erfragt werden
- `HEARTBEAT.md` — Rotation: Montag=Identität
- `projects/agent-memory-system/TODO.md` — aktuelle Aufgaben

## Wenn etwas fehlt

**Wenn `memory/` Ordner nicht existiert:**
→ Erstellen + Tagesnotiz anlegen

**Wenn `projects/` Ordner nicht existiert:**
→ Erstellen + Struktur anlegen (siehe oben)

**Wenn USER.md leer ist:**
→ Oli fragen: Name, Anrede, andere Projekte

## Erste Fragen an Oli

1. "Soll ich dich 'Oli' oder '[voller Name]' nennen? Du oder Sie?"
2. "Gibt es schon konkrete Projekte, die wir anlegen sollen?"
3. "Was soll ich zuerst machen — TOOLS füllen oder ein echtes Projekt starten?"
