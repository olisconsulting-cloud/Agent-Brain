#!/usr/bin/env python3
"""
Deliberate Disagreement v2.0 — DYNAMIC Three Perspectives

Usage:
    python3 activate_dd.py "wichtig Deine Frage hier"
    
Aktiviert bei 'wichtig' in JEDEM Kontext!
"""

import sys
import os

# Auto-detect workspace
WORKSPACE = os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace')
sys.path.insert(0, f'{WORKSPACE}/smriti/src/python')

try:
    from smriti.deliberate_disagreement_v2 import deliberate_disagreement_v2
    
    # Get input from command line or use default
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = "wichtig Soll ich Docker für das neue Projekt verwenden?"
    
    print("🎭 Deliberate Disagreement v2.0 — DYNAMIC 3 Perspectives")
    print("=" * 60)
    print(f"Input: {user_input}")
    print()
    
    result = deliberate_disagreement_v2(user_input)
    
    if result:
        print(result)
    else:
        print("❌ Nicht aktiviert")
        print("Tipp: Schreibe 'wichtig' irgendwo in deine Frage")
        print("Beispiel: 'Das ist wichtig: Soll ich X machen?'")
        
except Exception as e:
    print(f"❌ Fehler: {e}")
    import traceback
    traceback.print_exc()
