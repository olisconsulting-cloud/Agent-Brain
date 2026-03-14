#!/usr/bin/env python3
"""
Auto-Detector für "wichtig" — Integriert in OpenClaw Sessions

Dieses Skript prüft automatisch auf "wichtig" und aktiviert Deliberate Disagreement.
"""

import sys
import os

WORKSPACE = os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace')
sys.path.insert(0, f'{WORKSPACE}/smriti/src/python')

def check_and_activate(user_input):
    """Prüft auf 'wichtig' und aktiviert bei Bedarf"""
    try:
        from smriti.deliberate_disagreement_v2 import deliberate_disagreement_v2
        
        # Prüfe ob "wichtig" vorkommt
        if 'wichtig' in user_input.lower():
            result = deliberate_disagreement_v2(user_input)
            if result:
                return result
        
        return None
    except Exception as e:
        return f"[Smriti Error: {e}]"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        result = check_and_activate(user_input)
        if result:
            print(result)
