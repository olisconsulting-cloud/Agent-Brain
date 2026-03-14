#!/usr/bin/env python3
"""
Auto-Tuner v3.5 — Selbst-Optimierung basierend auf Heartbeat-Daten

Passt Smriti-Einstellungen automatisch an, basierend auf M1-M5 Trends.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

class AutoTuner:
    """Optimiert Smriti automatisch basierend auf Performance"""
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace or os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace'))
        self.config_file = self.workspace / 'neuron' / 'smriti.json'
        self.backup_dir = self.workspace / 'neuron' / 'config_backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Lade aktuelle Config
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Lädt aktuelle Smriti-Config"""
        try:
            with open(self.config_file) as f:
                return json.load(f)
        except Exception:
            return {}
    
    def _backup_config(self):
        """Erstellt Backup vor Änderungen"""
        from datetime import datetime
        backup_file = self.backup_dir / f"smriti_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            with open(backup_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return str(backup_file)
        except Exception as e:
            print(f"Backup failed: {e}")
            return None
    
    def _save_config(self):
        """Speichert geänderte Config"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Save failed: {e}")
            return False
    
    def tune_for_metric(self, metric_name: str, trend: str, current_value: float) -> Optional[str]:
        """Passt Einstellungen für eine spezifische Metrik an"""
        
        action = None
        
        if metric_name == 'm1' and trend == 'declining':
            # M1 fällt: Überrasche mehr
            if 'system_1_quality' in self.config:
                old_threshold = self.config['system_1_quality'].get('threshold', 0.8)
                new_threshold = max(0.6, old_threshold - 0.05)
                self.config['system_1_quality']['threshold'] = new_threshold
                action = f"M1: Threshold {old_threshold} → {new_threshold} (mehr Überraschungen)"
        
        elif metric_name == 'm2' and trend == 'declining':
            # M2 fällt: Mehr Frameworks
            if 'system_1_quality' in self.config:
                if 'frameworks' not in self.config['system_1_quality']:
                    self.config['system_1_quality']['frameworks'] = []
                # Füge mehr Frameworks hinzu
                new_frameworks = ['first_principles', 'systems_thinking', 'mental_models']
                for fw in new_frameworks:
                    if fw not in self.config['system_1_quality']['frameworks']:
                        self.config['system_1_quality']['frameworks'].append(fw)
                action = f"M2: Frameworks erweitert um {new_frameworks}"
        
        elif metric_name == 'm3' and trend == 'declining':
            # M3 fällt: Achte mehr auf Shifts
            if 'system_1_quality' in self.config:
                self.config['system_1_quality']['shift_detection'] = True
                self.config['system_1_quality']['shift_sensitivity'] = 0.7
                action = "M3: Shift-Erkennung aktiviert (Sensitivität 0.7)"
        
        elif metric_name == 'm4' and trend == 'declining':
            # M4 fällt: Beschleunige
            if 'system_1_quality' in self.config:
                old_depth = self.config['system_1_quality'].get('reflection_depth', 3)
                new_depth = max(1, old_depth - 1)
                self.config['system_1_quality']['reflection_depth'] = new_depth
                action = f"M4: Reflection Depth {old_depth} → {new_depth} (schneller)"
        
        elif metric_name == 'm5' and trend == 'declining':
            # M5 fällt: Nutze Kritik besser
            if 'system_1_quality' in self.config:
                self.config['system_1_quality']['anti_fragile_mode'] = True
                self.config['system_1_quality']['criticism_bonus'] = 0.2
                action = "M5: Anti-fragile Mode aktiviert (Kritik-Bonus 0.2)"
        
        return action
    
    def apply_tuning(self, trends: Dict) -> List[str]:
        """Wendet Tuning auf alle Metriken an"""
        
        actions = []
        
        # Backup erstellen
        backup_path = self._backup_config()
        if backup_path:
            actions.append(f"✅ Backup erstellt: {backup_path}")
        
        # Für jede Metrik prüfen
        for metric_name, trend_data in trends.items():
            if isinstance(trend_data, dict) and trend_data.get('trend') == 'declining':
                current = trend_data.get('current', 3.0)
                action = self.tune_for_metric(metric_name, 'declining', current)
                if action:
                    actions.append(f"🔧 {action}")
        
        # Speichern wenn Änderungen
        if len(actions) > 1:  # Mehr als nur Backup
            if self._save_config():
                actions.append("✅ Config gespeichert")
            else:
                actions.append("❌ Config konnte nicht gespeichert werden")
        else:
            actions.append("ℹ️ Keine Änderungen nötig")
        
        return actions
    
    def get_tuning_report(self) -> str:
        """Erzeugt einen Tuning-Report"""
        
        lines = [
            "╔════════════════════════════════════════════════════════════╗",
            "║  AUTO-TUNER v3.5 — Report                                  ║",
            "╚════════════════════════════════════════════════════════════╝",
            "",
            f"Config: {self.config_file}",
            f"Backups: {self.backup_dir}",
            "",
            "Aktuelle Einstellungen:",
        ]
        
        if 'system_1_quality' in self.config:
            sq = self.config['system_1_quality']
            lines.append(f"  Threshold: {sq.get('threshold', 'N/A')}")
            lines.append(f"  Reflection Depth: {sq.get('reflection_depth', 'N/A')}")
            lines.append(f"  Frameworks: {len(sq.get('frameworks', []))}")
        
        lines.extend([
            "",
            "Letzte Backups:",
        ])
        
        try:
            backups = sorted(self.backup_dir.glob('smriti_backup_*.json'))[-3:]
            for backup in backups:
                lines.append(f"  • {backup.name}")
        except Exception:
            lines.append("  Keine Backups gefunden")
        
        lines.append("")
        
        return '\n'.join(lines)


if __name__ == "__main__":
    # Test
    tuner = AutoTuner()
    
    # Simuliere declining Trends
    trends = {
        'm1': {'trend': 'declining', 'current': 2.5},
        'm2': {'trend': 'stable', 'current': 3.5},
        'm3': {'trend': 'declining', 'current': 2.0},
    }
    
    print(tuner.get_tuning_report())
    print("\n" + "="*60)
    print("Tuning wird angewendet...")
    print("="*60 + "\n")
    
    actions = tuner.apply_tuning(trends)
    for action in actions:
        print(f"  {action}")
