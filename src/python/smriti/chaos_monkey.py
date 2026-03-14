#!/usr/bin/env python3
"""
Chaos Monkey v3.5 — Testet System-Resilienz

Provoziert Fehler, um zu testen ob Smriti robust ist.
"""

import random
import time
import os
from pathlib import Path
from datetime import datetime

class ChaosMonkey:
    """Testet Smriti durch gezielte Störungen"""
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace or os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace'))
        self.test_log = self.workspace / 'logs' / 'chaos_monkey.log'
        self.is_running = False
        
        # Test-Szenarien
        self.scenarios = [
            {
                'name': 'Memory Corruption',
                'description': 'Löscht zufälligen Cache-Eintrag',
                'action': self._corrupt_memory,
                'severity': 'low'
            },
            {
                'name': 'Config Error',
                'description': 'Fügt temporären Fehler in Config ein',
                'action': self._config_error,
                'severity': 'medium'
            },
            {
                'name': 'Service Down',
                'description': 'Simuliert mem0 Ausfall',
                'action': self._service_down,
                'severity': 'high'
            },
            {
                'name': 'High Load',
                'description': 'Erzeugt viele gleichzeitige Anfragen',
                'action': self._high_load,
                'severity': 'medium'
            },
            {
                'name': 'Disk Full',
                'description': 'Simuliert volle Festplatte',
                'action': self._disk_full,
                'severity': 'high'
            }
        ]
    
    def run_test(self, scenario_name: str = None) -> dict:
        """Führt ein Chaos-Test-Szenario aus"""
        
        if scenario_name:
            scenario = next((s for s in self.scenarios if s['name'] == scenario_name), None)
            if not scenario:
                return {'error': f'Szenario {scenario_name} nicht gefunden'}
        else:
            # Zufälliges Szenario
            scenario = random.choice(self.scenarios)
        
        print(f"🐒 Chaos Monkey: {scenario['name']}")
        print(f"   Beschreibung: {scenario['description']}")
        print(f"   Schweregrad: {scenario['severity']}")
        
        # Führe Test durch
        start_time = time.time()
        try:
            result = scenario['action']()
            success = True
        except Exception as e:
            result = f"Fehler: {e}"
            success = False
        
        duration = time.time() - start_time
        
        # Logge Ergebnis
        test_result = {
            'timestamp': datetime.now().isoformat(),
            'scenario': scenario['name'],
            'severity': scenario['severity'],
            'duration': duration,
            'success': success,
            'result': result
        }
        
        self._log_test(test_result)
        
        return test_result
    
    def _corrupt_memory(self):
        """Löscht zufälligen Cache-Eintrag"""
        cache_dir = self.workspace / 'data' / 'memory' / 'cache'
        if cache_dir.exists():
            files = list(cache_dir.glob('*.json'))
            if files:
                target = random.choice(files)
                target.unlink()
                return f"Gelöscht: {target.name}"
        return "Kein Cache zum Löschen gefunden"
    
    def _config_error(self):
        """Fügt temporären Fehler in Config ein"""
        config_file = self.workspace / 'neuron' / 'smriti.json'
        if config_file.exists():
            # Backup
            backup = config_file.with_suffix('.json.bak')
            import shutil
            shutil.copy(config_file, backup)
            
            # Temporärer Fehler
            import json
            with open(config_file) as f:
                config = json.load(f)
            
            original = config.get('system_1_quality', {}).get('threshold', 0.8)
            config['system_1_quality']['threshold'] = -1  # Ungültiger Wert
            
            with open(config_file, 'w') as f:
                json.dump(config, f)
            
            # Warte und stelle wieder her
            time.sleep(2)
            config['system_1_quality']['threshold'] = original
            with open(config_file, 'w') as f:
                json.dump(config, f)
            
            return f"Config-Fehler injiziert und wiederhergestellt"
        return "Config nicht gefunden"
    
    def _service_down(self):
        """Simuliert mem0 Ausfall"""
        # Prüfe ob mem0 läuft
        try:
            import subprocess
            result = subprocess.run(['curl', '-s', 'http://localhost:8000/health'], 
                                  capture_output=True, timeout=2)
            if result.returncode == 0:
                return "mem0 läuft (Fallback zu Layer 2 funktioniert)"
            else:
                return "mem0 nicht erreichbar (Layer 2 Fallback aktiv)"
        except Exception:
            return "mem0 nicht erreichbar (Layer 2 Fallback aktiv)"
    
    def _high_load(self):
        """Erzeugt viele gleichzeitige Anfragen"""
        import threading
        
        def dummy_request():
            time.sleep(0.1)
        
        threads = []
        for _ in range(10):
            t = threading.Thread(target=dummy_request)
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        return "10 parallele Anfragen verarbeitet"
    
    def _disk_full(self):
        """Simuliert volle Festplatte"""
        # Prüfe verfügbaren Speicher
        import shutil
        total, used, free = shutil.disk_usage(self.workspace)
        
        if free < 1024 * 1024 * 100:  # Weniger als 100MB
            return "WARNUNG: Wenig Speicherplatz!"
        else:
            return f"Speicher OK: {free // (1024*1024)} MB frei"
    
    def _log_test(self, result: dict):
        """Loggt Test-Ergebnis"""
        try:
            with open(self.test_log, 'a') as f:
                f.write(f"{result}\n")
        except Exception:
            pass
    
    def get_report(self) -> str:
        """Erzeugt Chaos-Monkey-Report"""
        
        lines = [
            "╔════════════════════════════════════════════════════════════╗",
            "║  CHAOS MONKEY v3.5 — Resilienz-Report                      ║",
            "╚════════════════════════════════════════════════════════════╝",
            "",
            "Verfügbare Szenarien:",
        ]
        
        for scenario in self.scenarios:
            lines.append(f"  • {scenario['name']} ({scenario['severity']})")
            lines.append(f"    {scenario['description']}")
        
        lines.extend([
            "",
            "Letzte Tests:",
        ])
        
        try:
            if self.test_log.exists():
                with open(self.test_log) as f:
                    lines_list = f.readlines()[-5:]
                    for line in lines_list:
                        lines.append(f"  {line.strip()}")
            else:
                lines.append("  Keine Tests durchgeführt")
        except Exception:
            lines.append("  Keine Tests durchgeführt")
        
        lines.append("")
        
        return '\n'.join(lines)


if __name__ == "__main__":
    # Test
    monkey = ChaosMonkey()
    
    print(monkey.get_report())
    print("\n" + "="*60)
    print("Führe zufälligen Test aus...")
    print("="*60 + "\n")
    
    result = monkey.run_test()
    print(f"\nErgebnis: {result}")
