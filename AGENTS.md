# AGENTS.md — Smriti v3.5 Full Integration

## 🧠 Automatische Systeme (Immer Aktiv)

### System 1: Quality Engine
- Misst M1-M5 Metriken automatisch
- Speichert in `neuron/m1m4_log.jsonl`

### System 2: Pattern Engine (Reflecty)
- Beobachtet im Hintergrund
- Speichert Patterns in `neuron/patterns.jsonl`

### System 3: Improvement Engine (OUROBOROS)
- Prüft täglich auf Verbesserungen
- Log: `neuron/ouroboros_mutations.jsonl`

### System 4: BRIDGE
- Verbindet alle Systeme
- Status: `neuron/.bridge_state.json`

### System 5: Memory Infrastructure
- Layer 2: Immer aktiv (Dateien)
- Layer 3: Mit Fallback (mem0)

---

## 🎭 Manuelle Aktivierung (Bei Bedarf)

### Deliberate Disagreement (3 Perspektiven)
**Wann:** Bei wichtigen Entscheidungen
**Wie:** Schreibe "wichtig" in deine Frage

```
exec python3 /data/.openclaw/workspace/smriti/activate_dd.py "{{input}}"
```

**Beispiel:**
- "Das ist wichtig: Soll ich Docker verwenden?"
- "wichtig! Neue Marketing-Strategie"

---

## 🚀 Session Start (Einmalig)

```
exec bash /data/.openclaw/workspace/smriti/smriti-session-hook.sh
```

**Was passiert:**
- Alle 5 Systeme initialisieren
- Environment laden
- Health-Checks durchführen

---

## 📊 Monitoring

```
# Logs ansehen
exec tail -f /data/.openclaw/workspace/logs/quality_tracker.log

# BRIDGE Status
exec python3 -c "from neuron.bridge_connector import bridge_status; print(bridge_status())"

# M1-M4 Metriken
exec tail -f /data/.openclaw/workspace/neuron/m1m4_log.jsonl
```

---

## 🛠️ Tools

- web_search
- web_fetch
- file_read
- file_write
- exec (für Smriti-Integration)

---

## 💡 Hinweise

- **Automatisch:** Quality, Pattern, Improvement, BRIDGE, Memory
- **Manuell:** Deliberate Disagreement (bei "wichtig")
- **Session-Start:** Einmalig `smriti-session-hook.sh` ausführen

---

*Smriti v3.5 — Production Ready*
