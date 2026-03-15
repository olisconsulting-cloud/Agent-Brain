#!/usr/bin/env python3
"""
Sutra Manual Entry v1.0
SICHERES Tool für manuelle Session-Ende-Einträge

Kritische Unterschiede zum Extractor:
- Verwendet APPEND Modus (nie überschreiben)
- Prüft Duplikate vor dem Schreiben
- Backup vor Änderungen
- Atomare Operationen
"""

import json
import sys
import shutil
from datetime import datetime
from pathlib import Path

SUTRA_PATH = Path('/data/.openclaw/workspace/neuron/sutra_session_memory.jsonl')
BACKUP_DIR = Path('/data/.openclaw/workspace/neuron/backup')

def ensure_backup():
    """Erstelle Backup vor Änderungen"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    
    if SUTRA_PATH.exists():
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = BACKUP_DIR / f'sutra_backup_{timestamp}.jsonl'
        shutil.copy2(SUTRA_PATH, backup_path)
        return backup_path
    return None

def session_exists(session_id):
    """Prüfe ob Session bereits existiert"""
    if not SUTRA_PATH.exists():
        return False
    
    with open(SUTRA_PATH, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get('session_id') == session_id:
                    return True
            except json.JSONDecodeError:
                continue
    return False

def append_entry(entry):
    """Füge Eintrag sicher an (APPEND, nie überschreiben)"""
    
    # Sicherer Append-Modus
    with open(SUTRA_PATH, 'a') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    # Rotation nach dem Append
    rotate_if_needed()

def rotate_if_needed(max_entries=20):
    """FIFO-Rotation: Behalte nur letzte N Einträge"""
    
    if not SUTRA_PATH.exists():
        return
    
    # Lese alle Einträge
    entries = []
    with open(SUTRA_PATH, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(line)
    
    # Rotation nur wenn nötig
    if len(entries) > max_entries:
        entries = entries[-max_entries:]
        
        # Atomares Überschreiben (nur bei Rotation)
        temp_path = SUTRA_PATH.with_suffix('.tmp')
        with open(temp_path, 'w') as f:
            for entry in entries:
                f.write(entry + '\n')
        temp_path.replace(SUTRA_PATH)

def create_entry(session_id, summary, insights, decisions, patterns, anti_patterns):
    """Erstelle vollständigen Sutra-Eintrag"""
    
    # Berechne Quality-Score
    score = 0.0
    score += min(len(insights) * 0.2, 1.0)
    score += min(len(decisions) * 0.15, 0.6)
    score += min(len(patterns) * 0.1, 0.2)
    score += min(len(anti_patterns) * 0.1, 0.2)
    score = min(round(score, 2), 1.0)
    
    return {
        'version': 'sutra-v1.0',
        'session_id': session_id,
        'timestamp': datetime.now().isoformat(),
        'summary': summary,
        'insights': insights[:5],
        'decisions': decisions[:5],
        'patterns': patterns[:3],
        'anti_patterns': anti_patterns[:3],
        'hebel': len(insights) > 0,
        'quality_score': score
    }

def main():
    """Hauptfunktion für manuelle Einträge"""
    
    # Beispiel-Usage
    if len(sys.argv) == 1 or sys.argv[1] in ['--help', '-h']:
        print("""
Sutra Manual Entry — SICHERES Session-Ende Tool

Usage:
  python3 sutra_manual_entry.py \
    --session-id "sess_2026_03_15_1234" \
    --summary "Kurze Zusammenfassung" \
    --insights "Insight 1" "Insight 2" \
    --decisions "Decision 1" \
    --patterns "Pattern 1" \
    --anti-patterns "Anti-Pattern 1"

Oder importiere in Python:
  from sutra_manual_entry import create_entry, append_entry
  entry = create_entry(...)
  append_entry(entry)
        """)
        return
    
    # Parse Argumente
    args = sys.argv[1:]
    session_id = None
    summary = "Session abgeschlossen"
    insights = []
    decisions = []
    patterns = []
    anti_patterns = []
    
    i = 0
    while i < len(args):
        if args[i] == '--session-id' and i + 1 < len(args):
            session_id = args[i + 1]
            i += 2
        elif args[i] == '--summary' and i + 1 < len(args):
            summary = args[i + 1]
            i += 2
        elif args[i] == '--insights':
            i += 1
            while i < len(args) and not args[i].startswith('--'):
                insights.append(args[i])
                i += 1
        elif args[i] == '--decisions':
            i += 1
            while i < len(args) and not args[i].startswith('--'):
                decisions.append(args[i])
                i += 1
        elif args[i] == '--patterns':
            i += 1
            while i < len(args) and not args[i].startswith('--'):
                patterns.append(args[i])
                i += 1
        elif args[i] == '--anti-patterns':
            i += 1
            while i < len(args) and not args[i].startswith('--'):
                anti_patterns.append(args[i])
                i += 1
        else:
            i += 1
    
    if not session_id:
        print("❌ ERROR: --session-id erforderlich")
        sys.exit(1)
    
    # Prüfe Duplikat
    if session_exists(session_id):
        print(f"⚠️  Session {session_id[:8]}... bereits in Sutra")
        print("   Überspringe (keine Änderung)")
        return
    
    # Backup erstellen
    backup_path = ensure_backup()
    if backup_path:
        print(f"💾 Backup erstellt: {backup_path.name}")
    
    # Erstelle Eintrag
    entry = create_entry(session_id, summary, insights, decisions, patterns, anti_patterns)
    
    # Füge hinzu (sicherer Append)
    append_entry(entry)
    
    print(f"✅ Sutra: Session {session_id[:8]}... hinzugefügt")
    print(f"   Summary: {summary[:50]}...")
    print(f"   Insights: {len(insights)}")
    print(f"   Decisions: {len(decisions)}")
    print(f"   Quality: {entry['quality_score']}")

if __name__ == '__main__':
    main()
