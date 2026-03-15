#!/bin/bash
# Sutra Auto-Extractor Hook v1.1
# Wird bei Session-Ende aufgerufen

set -euo pipefail  # Strict mode

SESSION_FILE="${1:-}"
LOG_FILE="/data/.openclaw/workspace/smriti/logs/sutra.log"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Prüfe Argumente
if [ -z "$SESSION_FILE" ]; then
    log "❌ ERROR: Usage: sutra_session_end.sh <session_file.jsonl>"
    exit 1
fi

if [ ! -f "$SESSION_FILE" ]; then
    log "❌ ERROR: Session file not found: $SESSION_FILE"
    exit 1
fi

# Prüfe Python3
if ! command -v python3 &> /dev/null; then
    log "❌ ERROR: python3 not found"
    exit 1
fi

# Prüfe Extractor
EXTRACTOR="/data/.openclaw/workspace/smriti/sutra_extractor.py"
if [ ! -f "$EXTRACTOR" ]; then
    log "❌ ERROR: Extractor not found: $EXTRACTOR"
    exit 1
fi

# Erstelle Log-Verzeichnis
mkdir -p "$(dirname "$LOG_FILE")"

# Prüfe Session-Qualität (min 10 Nachrichten)
# Verwende Python für korrektes JSON-Parsing
MESSAGE_COUNT=$(python3 -c "
import json
import sys
try:
    with open('$SESSION_FILE') as f:
        data = json.load(f)
        messages = data.get('messages', [])
        print(len(messages))
except Exception as e:
    print(0)
    sys.exit(1)
" 2>/dev/null || echo "0")

if [ "$MESSAGE_COUNT" -lt 10 ]; then
    log "⏭️  Session zu kurz ($MESSAGE_COUNT Nachrichten), übersprungen"
    exit 0
fi

log "🧵 Extrahiere Session ($MESSAGE_COUNT Nachrichten)..."

# Führe Extraktion durch
if python3 "$EXTRACTOR" "$SESSION_FILE" >> "$LOG_FILE" 2>&1; then
    log "✅ Sutra-Extraktion erfolgreich"
    
    # REFLECTY ACTIVATOR Integration
    log "🧠 Starte Reflecty Activator..."
    
    REFLECTY_ACTIVATOR="/data/.openclaw/workspace/skills/reflecty-activator/reflecty_session_end.py"
    SESSION_ID=$(basename "$SESSION_FILE" .jsonl)
    
    if [ -f "$REFLECTY_ACTIVATOR" ]; then
        # Extrahiere Session-ID aus Dateiname oder Inhalt
        python3 "$REFLECTY_ACTIVATOR" --session-id "$SESSION_ID" --session-file "$SESSION_FILE" >> "$LOG_FILE" 2>&1 || true
        log "✅ Reflecty Activator abgeschlossen"
    else
        log "⚠️  Reflecty Activator nicht gefunden: $REFLECTY_ACTIVATOR"
    fi
    
    log "✅ Session-Ende-Protokoll vollständig"
    exit 0
else
    log "❌ Sutra-Extraktion fehlgeschlagen (Exit-Code: $?)"
    exit 1
fi
