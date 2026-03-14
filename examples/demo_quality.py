#!/usr/bin/env python3
"""
Smriti v3.5 — Quality Metrics Demo

This script demonstrates the Genius Quality Tracker.
Run it to see M1-M5 metrics in action.
"""

import sys
import os

# Add workspace to path
workspace = os.environ.get('SMRITI_WORKSPACE', os.path.expanduser('~/.openclaw/workspace'))
sys.path.insert(0, workspace)

try:
    from smriti.quality_tracker import GeniusQualityTracker
except ImportError:
    print("❌ Smriti not found. Please run:")
    print("   node install.mjs")
    print("   source .smriti_env")
    sys.exit(1)

def main():
    print("=" * 60)
    print("🧠 SMRITI v3.5 — Quality Metrics Demo")
    print("=" * 60)
    print()
    
    # Create tracker
    tracker = GeniusQualityTracker()
    
    # Demo session
    print("📊 Analyzing demo session...")
    print()
    
    test_messages = [
        {"role": "user", "content": "Kannst du das erklären?"},
        {"role": "assistant", "content": "Natürlich. Das ist ein System mit first principles und meta-ebene Betrachtung..."},
        {"role": "user", "content": "Ah, jetzt verstehe ich! Das ist eine meta-ebene Betrachtung."},
        {"role": "assistant", "content": "Genau! Du hast den Paradigmen-Shift erkannt. Das ist antifragile Resonanz."},
        {"role": "user", "content": "Aber warte, ist das nicht zu abstrakt?"},
        {"role": "assistant", "content": "Guter Punkt. Lass mich konkreter werden mit einem Beispiel..."},
        {"role": "user", "content": "Stimmt, das macht Sinn!"},
        {"role": "assistant", "content": "Präzise! Du verstehst das System-Denken."},
    ]
    
    # Analyze
    result = tracker.analyze_session(test_messages)
    
    # Print report
    tracker.print_report(result)
    
    print()
    print("=" * 60)
    print("✅ Demo complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  • Run with real data: python3 smriti/quality_tracker.py --session-file session.json")
    print("  • Check logs: tail -f logs/quality_tracker.log")
    print("  • See M1-M4 history: tail -f neuron/m1m4_log.jsonl")

if __name__ == "__main__":
    main()
