#!/usr/bin/env python3
"""
Heartbeat Master v3.5 — Komplettes Self-Monitoring System

Integriert:
- Echtzeit-Monitoring (M1-M5)
- Trend-Analyse
- Prädiktive Alerts
- Auto-Tuning
- Chaos-Monkey Tests

Usage:
    python3 heartbeat_master.py
    python3 heartbeat_master.py --dashboard
    python3 heartbeat_master.py --tune
    python3 heartbeat_master.py --chaos
"""

import sys
import os
import argparse
from pathlib import Path

WORKSPACE = Path(os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace'))
sys.path.insert(0, str(WORKSPACE / 'smriti' / 'src' / 'python'))

from smriti.heartbeat_monitor import HeartbeatMonitor, get_monitor
from smriti.auto_tuner import AutoTuner
from smriti.chaos_monkey import ChaosMonkey
from smriti.self_healing_engine import SelfHealingEngine

def main():
    parser = argparse.ArgumentParser(description='Heartbeat Master v3.5')
    parser.add_argument('--dashboard', action='store_true', help='Zeigt Dashboard')
    parser.add_argument('--tune', action='store_true', help='Führt Auto-Tuning durch')
    parser.add_argument('--chaos', action='store_true', help='Führt Chaos-Monkey-Test durch')
    parser.add_argument('--full', action='store_true', help='Führt kompletten Check durch')
    parser.add_argument('--heal', action='store_true', help='Führt Self-Healing durch')
    
    args = parser.parse_args()
    
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  HEARTBEAT MASTER v3.5 — Self-Monitoring System            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    if args.dashboard:
        # Zeige Dashboard
        monitor = get_monitor()
        print(monitor.get_dashboard())
        print("\nEmpfehlungen:")
        for rec in monitor.get_recommendations():
            print(f"  {rec}")
    
    elif args.tune:
        # Auto-Tuning
        print("🔧 Führe Auto-Tuning durch...")
        tuner = AutoTuner()
        
        # Lade aktuelle Trends
        monitor = get_monitor()
        trends = monitor._analyze_trends()
        
        if trends:
            actions = tuner.apply_tuning(trends)
            print("\nErgebnisse:")
            for action in actions:
                print(f"  {action}")
        else:
            print("  ℹ️ Keine Trends verfügbar (mindestens 3 Sessions nötig)")
    
    elif args.chaos:
        # Chaos Monkey
        print("🐒 Starte Chaos-Monkey...")
        monkey = ChaosMonkey()
        result = monkey.run_test()
        
        print(f"\nTest: {result.get('scenario', 'N/A')}")
        print(f"Erfolg: {'✅' if result.get('success') else '❌'}")
        print(f"Ergebnis: {result.get('result', 'N/A')}")
    
    elif args.full:
        # Kompletter Check
        print("🔍 Kompletter System-Check...\n")
        
        # 1. Dashboard
        monitor = get_monitor()
        print("1. Dashboard:")
        print(monitor.get_dashboard())
        
        # 2. Empfehlungen
        print("\n2. Empfehlungen:")
        recommendations = monitor.get_recommendations()
        for rec in recommendations:
            print(f"   {rec}")
        
        # 3. Auto-Tuning (wenn nötig)
        if any('fällt' in rec for rec in recommendations):
            print("\n3. Auto-Tuning wird empfohlen:")
            tuner = AutoTuner()
            trends = monitor._analyze_trends()
            if trends:
                actions = tuner.apply_tuning(trends)
                for action in actions:
                    print(f"   {action}")
        
        # 4. Chaos-Monkey (optional)
        print("\n4. Chaos-Monkey Test:")
        print("   Führe aus mit: python3 heartbeat_master.py --chaos")
        
        # 5. Self-Healing (optional)
        print("\n5. Self-Healing:")
        print("   Führe aus mit: python3 heartbeat_master.py --heal")
    
    elif args.heal:
        # Self-Healing
        print("🔧 Starte Self-Healing...")
        engine = SelfHealingEngine()
        
        print("\n1. Health-Check:")
        health = engine.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Probleme: {health['total_issues']}")
        
        if health['issues']:
            print("\n2. Gefundene Probleme:")
            for issue in health['issues']:
                print(f"   • {issue['description']}")
            
            print("\n3. Heilung wird durchgeführt...")
            results = engine.heal(auto=True)
            for result in results:
                print(f"   {result}")
        else:
            print("\n✅ System gesund — keine Heilung nötig!")
    
    else:
        # Standard: Zeige Hilfe
        print("Verwendung:")
        print("  python3 heartbeat_master.py --dashboard  # Zeigt Dashboard")
        print("  python3 heartbeat_master.py --tune      # Auto-Tuning")
        print("  python3 heartbeat_master.py --chaos       # Chaos-Monkey")
        print("  python3 heartbeat_master.py --heal         # Self-Healing")
        print("  python3 heartbeat_master.py --full        # Kompletter Check")
        print()
        print("Status: 🟢 Operational → 🟡 Self-Monitoring → 🔴 Self-Healing")

if __name__ == "__main__":
    main()
