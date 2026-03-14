#!/bin/bash
# Setup Autonome Cron-Jobs für Smriti v3.5

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  SMRITI v3.5 — Autonome Cron-Jobs Setup                    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

WORKSPACE="${OPENCLAW_WORKSPACE:-/data/.openclaw/workspace}"
CRON_SCRIPT="$WORKSPACE/smriti/cron/smriti_cron.sh"

# Check if cron script exists
if [ ! -f "$CRON_SCRIPT" ]; then
    echo "❌ Cron script not found: $CRON_SCRIPT"
    exit 1
fi

echo "✅ Cron script found: $CRON_SCRIPT"
echo ""

# Add to crontab
echo "📝 Adding to crontab..."

# Create temporary crontab
crontab -l > /tmp/current_crontab 2>/dev/null || echo "# New crontab" > /tmp/current_crontab

# Check if already exists
if grep -q "smriti_cron.sh" /tmp/current_crontab; then
    echo "ℹ️  Smriti cron jobs already installed"
else
    # Add new entries
    echo "" >> /tmp/current_crontab
    echo "# Smriti v3.5 — Autonome Systeme" >> /tmp/current_crontab
    echo "*/5 * * * * $CRON_SCRIPT >> $WORKSPACE/logs/cron.log 2>&1" >> /tmp/current_crontab
    
    # Install new crontab
    crontab /tmp/current_crontab
    echo "✅ Cron jobs installed"
fi

# Clean up
rm -f /tmp/current_crontab

echo ""
echo "📋 Cron Jobs:"
echo "  • Alle 5 Minuten: Smriti System-Check"
echo "  • 08:00 täglich: Morning Init"
echo "  • :30 jede Stunde: Auto-Optimizer"
echo "  • 22:00 täglich: Evening Feedback"
echo ""
echo "✅ Setup complete!"
echo ""
echo "To verify: crontab -l"
