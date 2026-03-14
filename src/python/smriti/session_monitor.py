#!/usr/bin/env python3
"""
Smriti Session Monitor — Automatisch bei jeder Session aktiv

Dieses Skript läuft im Hintergrund und überwacht alle OpenClaw Sessions.
Aktiviert automatisch Deliberate Disagreement bei "wichtig".
"""

import os
import sys
import time
import json
from pathlib import Path

WORKSPACE = Path(os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace'))
sys.path.insert(0, str(WORKSPACE / 'smriti' / 'src' / 'python'))

from smriti.deliberate_disagreement_v2 import deliberate_disagreement_v2

class SessionMonitor:
    """Überwacht Sessions und aktiviert Smriti automatisch"""
    
    def __init__(self):
        self.workspace = WORKSPACE
        self.session_log = self.workspace / 'logs' / 'smriti_sessions.jsonl'
        self.session_log.parent.mkdir(parents=True, exist_ok=True)
        
        print("🧠 Smriti Session Monitor gestartet")
        print("   Überwache auf 'wichtig'...")
    
    def process_input(self, user_input: str, session_id: str = "default"):
        """Verarbeite User Input"""
        
        # Prüfe auf "wichtig"
        if 'wichtig' in user_input.lower():
            print(f"🎭 'wichtig' erkannt in Session {session_id}")
            
            # Aktiviere Deliberate Disagreement
            result = deliberate_disagreement_v2(user_input)
            
            if result:
                # Speichere für spätere Abfrage
                self._save_result(session_id, user_input, result)
                return result
        
        return None
    
    def _save_result(self, session_id: str, input_text: str, result: str):
        """Speichere Ergebnis für spätere Abfrage"""
        entry = {
            "timestamp": time.time(),
            "session_id": session_id,
            "input": input_text,
            "dd_result": result
        }
        
        with open(self.session_log, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def get_last_result(self, session_id: str = "default"):
        """Hole letztes Ergebnis für Session"""
        try:
            if not self.session_log.exists():
                return None
            
            # Lese letzte Zeile
            with open(self.session_log, 'r') as f:
                lines = f.readlines()
                for line in reversed(lines):
                    entry = json.loads(line)
                    if entry.get('session_id') == session_id:
                        return entry.get('dd_result')
        except Exception:
            pass
        
        return None

# Singleton für einfachen Zugriff
_monitor = None

def get_monitor():
    """Singleton Pattern"""
    global _monitor
    if _monitor is None:
        _monitor = SessionMonitor()
    return _monitor

if __name__ == "__main__":
    # Test
    monitor = get_monitor()
    
    # Simuliere Input
    test_input = "Das ist wichtig: Soll ich Docker verwenden?"
    result = monitor.process_input(test_input, "test_session")
    
    if result:
        print("\n=== ERGEBNIS ===")
        print(result[:500])
    else:
        print("Nicht aktiviert")
