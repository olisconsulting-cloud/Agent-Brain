#!/bin/bash
# Setup Autonome Cron-Jobs für Smriti v3.5
# Version 2.0 — Enhanced with user confirmation

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  SMRITI v3.5 — Autonome Cron-Jobs Setup v2.0              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

WORKSPACE="${OPENCLAW_WORKSPACE:-/data/.openclaw/workspace}"
CRON_SCRIPT="$WORKSPACE/smriti/cron/smriti_cron.sh"
LOG_FILE="$WORKSPACE/logs/cron.log"

# Check if cron script exists
if [ ! -f "$CRON_SCRIPT" ]; then
    echo "❌ Cron script not found: $CRON_SCRIPT"
    echo "   Bitte zuerst: cd /data/.openclaw/workspace/smriti-core/v3.5-enhanced"
    exit 1
fi

echo "✅ Cron script found: $CRON_SCRIPT"
echo ""

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Show what will be added
echo "📋 Folgende Cron-Jobs werden hinzugefügt:"
echo ""
echo "  # Smriti v3.5 — Autonome Systeme"
echo "  */5 * * * * $CRON_SCRIPT >> $LOG_FILE 2>&1"
echo ""
echo "  Was das macht:"
echo "    • Alle 5 Minuten: System-Check"
echo "    • 08:00 täglich: Morning Init (Trend-Analyse)"
echo "    • :30 jede Stunde: Auto-Optimizer (M1-M5 Tuning)"
echo "    • 22:00 täglich: Evening Feedback (Tagesreview)"
echo "    • :00 jede Stunde: Mutation Check"
echo ""

# Check if already installed
if crontab -l 2>/dev/null | grep -q "smriti_cron.sh"; then
    echo "⚠️  HINWEIS: Smriti Cron-Jobs sind bereits installiert!"
    echo ""
    echo "Aktuelle Einträge:"
    crontab -l | grep -A 1 "Smriti v3.5"
    echo ""
    read -p "Trotzdem neu installieren? (j/N): " REINSTALL
    if [[ ! "$REINSTALL" =~ ^[Jj]$ ]]; then
        echo "❌ Abgebrochen."
        exit 0
    fi
    echo ""
fi

# User confirmation
read -p "Cron-Jobs installieren? (j/N): " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Jj]$ ]]; then
    echo "❌ Installation abgebrochen."
    echo ""
    echo "Manuelle Installation:"
    echo "  crontab -e"
    echo "  Dann folgende Zeile hinzufügen:"
    echo "  */5 * * * * $CRON_SCRIPT >> $LOG_FILE 2>&1"
    exit 0
fi

echo ""
echo "📝 Installiere Cron-Jobs..."

# Create new crontab
(
    # Keep existing crontab (except old smriti entries)
    crontab -l 2>/dev/null | grep -v "smriti_cron.sh" || true
    
    # Add new entry
    echo ""
    echo "# Smriti v3.5 — Autonome Systeme (installiert: $(date '+%Y-%m-%d %H:%M'))"
    echo "*/5 * * * * $CRON_SCRIPT >> $LOG_FILE 2>&1"
) | crontab -

echo ""
echo "✅ Cron-Jobs erfolgreich installiert!"
echo ""
echo "📋 Verifizierung:"
crontab -l | grep -A 1 "Smriti v3.5"
echo ""
echo "🎯 Nächste Schritte:"
echo "  1. Warte auf nächsten 5-Minuten-Takt (z.B. 22:15, 22:20, ...)"
echo "  2. Prüfe Logs: tail -f $LOG_FILE"
echo "  3. Bei Problemen: crontab -l (zeigt aktuelle Jobs)"
echo ""
echo "✅ Setup complete!"
