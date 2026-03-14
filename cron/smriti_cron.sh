#!/bin/bash
# Smriti v3.5 — Autonome Cron-Jobs
# 
# Dieses Skript wird automatisch ausgeführt:
# - Morning Init: 08:00 täglich
# - Auto-Optimize: Jede Stunde
# - Evening Feedback: 22:00 täglich

WORKSPACE="${OPENCLAW_WORKSPACE:-/data/.openclaw/workspace}"
SMRITI_DIR="$WORKSPACE/smriti"
LOG_FILE="$WORKSPACE/logs/smriti_cron.log"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

log "=== Smriti Cron Job Started ==="

# Determine which task to run based on time
HOUR=$(date +%H)
MINUTE=$(date +%M)

# Morning Init (08:00)
if [ "$HOUR" -eq 08 ] && [ "$MINUTE" -eq 00 ]; then
    log "Running: Morning Init"
    cd "$SMRITI_DIR" && node src/js/ouroboros/morning_init.mjs 2>&1 | tee -a "$LOG_FILE"
    log "Morning Init completed"
fi

# Evening Feedback (22:00)
if [ "$HOUR" -eq 22 ] && [ "$MINUTE" -eq 00 ]; then
    log "Running: Evening Feedback"
    cd "$SMRITI_DIR" && node src/js/ouroboros/evening_feedback.mjs 2>&1 | tee -a "$LOG_FILE"
    log "Evening Feedback completed"
fi

# Auto-Optimize (jede Stunde zur Minute 30)
if [ "$MINUTE" -eq 30 ]; then
    log "Running: Auto-Optimizer"
    cd "$SMRITI_DIR" && node src/js/ouroboros/auto_optimizer.mjs 2>&1 | tee -a "$LOG_FILE"
    log "Auto-Optimizer completed"
fi

# Mutation Check (jede Stunde zur Minute 00)
if [ "$MINUTE" -eq 00 ] && [ "$HOUR" -ne 08 ] && [ "$HOUR" -ne 22 ]; then
    log "Running: Mutation Check"
    cd "$SMRITI_DIR" && node src/js/ouroboros/mutation_engine.mjs --check-queue 2>&1 | tee -a "$LOG_FILE"
    log "Mutation Check completed"
fi

log "=== Smriti Cron Job Finished ==="
