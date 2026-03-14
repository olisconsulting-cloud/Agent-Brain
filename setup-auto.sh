#!/bin/bash
# Smriti v3.5 — Auto-Setup für vollständige Integration
# Fügt sich automatisch in AGENTS.md ein

WORKSPACE="/data/.openclaw/workspace"
AGENTS_FILE="$WORKSPACE/AGENTS.md"

echo "🔧 Smriti v3.5 Auto-Setup..."

# Prüfe ob AGENTS.md existiert
if [ ! -f "$AGENTS_FILE" ]; then
    echo "❌ AGENTS.md nicht gefunden: $AGENTS_FILE"
    exit 1
fi

# Prüfe ob Smriti bereits eingetragen
if grep -q "SMRITI v3.5" "$AGENTS_FILE"; then
    echo "✅ Smriti bereits in AGENTS.md eingetragen"
else
    echo "📝 Füge Smriti zu AGENTS.md hinzu..."
    
    cat >> "$AGENTS_FILE" << 'EOF'

---

## 🧠 SMRITI v3.5 — Automatisch Aktiv

### Session-Start (Immer laden):
```
exec bash /data/.openclaw/workspace/smriti/smriti-session-hook.sh
```

### Deliberate Disagreement (3 Perspektiven bei "wichtig"):
```
exec python3 /data/.openclaw/workspace/smriti/activate_dd.py "{{input}}"
```

**Was passiert:**
- ✅ Alle 5 Systeme starten automatisch
- ✅ Bei "wichtig": Optimist + Skeptiker + Devil's Advocate
- ✅ Qualitäts-Tracking läuft im Hintergrund
- ✅ Pattern-Mining aktiv

**Test:** Schreibe "wichtig Soll ich X machen?"
EOF

    echo "✅ Smriti zu AGENTS.md hinzugefügt"
fi

echo ""
echo "🎉 Setup complete!"
echo "Nach nächstem Restart: Smriti automatisch aktiv"
