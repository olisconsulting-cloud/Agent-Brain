#!/usr/bin/env python3
"""
Deliberate Disagreement — Quick Activation Script

Usage:
    python3 activate_dd.py "#wichtig Deine Frage hier"
    
Or in OpenClaw:
    exec python3 /data/.openclaw/workspace/smriti/activate_dd.py "#wichtig Soll ich X machen?"
"""

import sys
import os

# Auto-detect workspace
WORKSPACE = os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace')
sys.path.insert(0, f'{WORKSPACE}/smriti/src/python')

try:
    from smriti.deliberate_disagreement import deliberate_disagreement
    
    # Get input from command line or use default
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = "#wichtig Soll ich Docker für das neue Projekt verwenden?"
    
    print("🎭 Deliberate Disagreement — 3 Perspectives")
    print("=" * 60)
    print(f"Input: {user_input}")
    print()
    
    result = deliberate_disagreement(user_input)
    
    if result:
        print(result)
    else:
        print("❌ Nicht aktiviert (kein Trigger erkannt)")
        print("Tippe '#wichtig' am Anfang deiner Frage")
        
except Exception as e:
    print(f"❌ Fehler: {e}")
    import traceback
    traceback.print_exc()
