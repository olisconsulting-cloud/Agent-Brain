#!/usr/bin/env python3
"""
Self-Healing Engine v3.5 — Automatische Reparatur

Erkennt Probleme und repariert sie ohne menschliches Zutun.
"""

import json
import os
import time
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class SelfHealingEngine:
    """Automatische Reparatur von Smriti-Problemen"""
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace or os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace'))
        self.healing_log = self.workspace / 'logs' / 'self_healing.log'
        self.healing_log.parent.mkdir(parents=True, exist_ok=True)
        
        # Reparatur-Strategien
        self.healing_strategies = {
            'corrupt_json': self._fix_corrupt_json,
            'missing_config': self._restore_default_config,
            'service_down': self._restart_service,
            'disk_full': self._cleanup_disk,
            'memory_leak': self._clear_cache,
            'permission_error': self._fix_permissions,
            'broken_symlink': self._fix_symlinks,
            'log_rotation': self._rotate_logs
        }
    
    def health_check(self) -> Dict:
        """Führt vollständigen Health-Check durch"""
        
        issues = []
        
        # Check 1: JSON-Dateien
        json_issues = self._check_json_files()
        issues.extend(json_issues)
        
        # Check 2: Config-Dateien
        config_issues = self._check_configs()
        issues.extend(config_issues)
        
        # Check 3: Services
        service_issues = self._check_services()
        issues.extend(service_issues)
        
        # Check 4: Disk-Space
        disk_issues = self._check_disk_space()
        issues.extend(disk_issues)
        
        # Check 5: Permissions
        permission_issues = self._check_permissions()
        issues.extend(permission_issues)
        
        # Check 6: Symlinks
        symlink_issues = self._check_symlinks()
        issues.extend(symlink_issues)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_issues': len(issues),
            'issues': issues,
            'status': 'healthy' if len(issues) == 0 else 'needs_healing'
        }
    
    def heal(self, auto: bool = True) -> List[str]:
        """Führt automatische Reparatur durch"""
        
        results = []
        health = self.health_check()
        
        if health['status'] == 'healthy':
            results.append("✅ System gesund — keine Reparatur nötig")
            return results
        
        results.append(f"🔍 {health['total_issues']} Probleme gefunden")
        results.append("")
        
        # Repariere jedes Problem
        for issue in health['issues']:
            issue_type = issue['type']
            
            if issue_type in self.healing_strategies:
                if auto:
                    # Automatisch reparieren
                    try:
                        fix_result = self.healing_strategies[issue_type](issue)
                        results.append(f"🔧 {issue['description']}: {fix_result}")
                        self._log_healing(issue, fix_result, 'success')
                    except Exception as e:
                        error_msg = f"Fehlgeschlagen: {e}"
                        results.append(f"❌ {issue['description']}: {error_msg}")
                        self._log_healing(issue, error_msg, 'failed')
                else:
                    # Nur vorschlagen
                    results.append(f"💡 {issue['description']}: Auto-Reparatur möglich")
            else:
                results.append(f"⚠️ {issue['description']}: Manuelle Reparatur nötig")
        
        return results
    
    def _check_json_files(self) -> List[Dict]:
        """Prüft auf korrupte JSON-Dateien"""
        issues = []
        
        json_files = list(self.workspace.rglob('*.json'))
        for json_file in json_files:
            try:
                with open(json_file) as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                issues.append({
                    'type': 'corrupt_json',
                    'file': str(json_file),
                    'description': f'Korrupte JSON: {json_file.name}',
                    'error': str(e)
                })
        
        return issues
    
    def _check_configs(self) -> List[Dict]:
        """Prüft auf fehlende Config-Dateien"""
        issues = []
        
        required_configs = [
            self.workspace / 'neuron' / 'smriti.json',
            self.workspace / 'neuron' / 'bridge.json'
        ]
        
        for config_file in required_configs:
            if not config_file.exists():
                issues.append({
                    'type': 'missing_config',
                    'file': str(config_file),
                    'description': f'Fehlende Config: {config_file.name}'
                })
        
        return issues
    
    def _check_services(self) -> List[Dict]:
        """Prüft ob Services laufen"""
        issues = []
        
        # Prüfe mem0 (optional)
        try:
            result = subprocess.run(['curl', '-s', 'http://localhost:8000/health'],
                                  capture_output=True, timeout=2)
            if result.returncode != 0:
                issues.append({
                    'type': 'service_down',
                    'service': 'mem0',
                    'description': 'mem0 nicht erreichbar (Layer 2 Fallback aktiv)'
                })
        except Exception:
            pass  # Kein Fehler, Layer 2 funktioniert
        
        return issues
    
    def _check_disk_space(self) -> List[Dict]:
        """Prüft Speicherplatz"""
        issues = []
        
        total, used, free = shutil.disk_usage(self.workspace)
        free_gb = free / (1024**3)
        
        if free_gb < 1:  # Weniger als 1GB
            issues.append({
                'type': 'disk_full',
                'free_gb': free_gb,
                'description': f'Kritischer Speicherplatz: {free_gb:.1f} GB frei'
            })
        elif free_gb < 5:  # Weniger als 5GB
            issues.append({
                'type': 'disk_full',
                'free_gb': free_gb,
                'description': f'Wenig Speicherplatz: {free_gb:.1f} GB frei'
            })
        
        return issues
    
    def _check_permissions(self) -> List[Dict]:
        """Prüft Datei-Berechtigungen"""
        issues = []
        
        critical_files = [
            self.workspace / 'smriti' / 'activate_dd.py',
            self.workspace / 'smriti' / 'heartbeat_master.py'
        ]
        
        for file in critical_files:
            if file.exists():
                stat = file.stat()
                if not (stat.st_mode & 0o111):  # Nicht ausführbar
                    issues.append({
                        'type': 'permission_error',
                        'file': str(file),
                        'description': f'Nicht ausführbar: {file.name}'
                    })
        
        return issues
    
    def _check_symlinks(self) -> List[Dict]:
        """Prüft auf defekte Symlinks"""
        issues = []
        
        smriti_link = self.workspace / 'smriti'
        if smriti_link.is_symlink():
            if not smriti_link.exists():
                issues.append({
                    'type': 'broken_symlink',
                    'link': str(smriti_link),
                    'description': 'Defekter Symlink: smriti'
                })
        
        return issues
    
    # ===== REPARATUR-METHODEN =====
    
    def _fix_corrupt_json(self, issue: Dict) -> str:
        """Repariert korrupte JSON-Datei"""
        file_path = Path(issue['file'])
        
        # Backup erstellen
        backup = file_path.with_suffix('.json.bak')
        shutil.copy(file_path, backup)
        
        # Versuche zu reparieren
        try:
            with open(file_path) as f:
                content = f.read()
            
            # Häufige JSON-Fehler beheben
            content = content.replace("'", '"')  # Einfache zu doppelten Anführungszeichen
            content = content.rstrip(',')       # Trailing commas entfernen
            
            # Teste ob jetzt valide
            json.loads(content)
            
            # Speichere reparierte Version
            with open(file_path, 'w') as f:
                f.write(content)
            
            return f"Repariert (Backup: {backup.name})"
        except Exception as e:
            # Stelle Backup wieder her
            shutil.copy(backup, file_path)
            return f"Reparatur fehlgeschlagen, Backup wiederhergestellt"
    
    def _restore_default_config(self, issue: Dict) -> str:
        """Stellt Default-Config wieder her"""
        file_path = Path(issue['file'])
        
        # Default-Configs
        defaults = {
            'smriti.json': {
                'version': '3.5',
                'system_1_quality': {'threshold': 0.8, 'reflection_depth': 3},
                'system_2_pattern': {'enabled': True},
                'system_3_improvement': {'auto_mutations': True}
            },
            'bridge.json': {
                'version': '3.5',
                'enabled': True,
                'auto_cleanup': True
            }
        }
        
        default_content = defaults.get(file_path.name, {})
        
        with open(file_path, 'w') as f:
            json.dump(default_content, f, indent=2)
        
        return f"Default-Config wiederhergestellt"
    
    def _restart_service(self, issue: Dict) -> str:
        """Versucht Service neu zu starten"""
        service = issue.get('service', 'unknown')
        
        # Für mem0: Hinweis auf Fallback
        if service == 'mem0':
            return "mem0 nicht neu gestartet (Layer 2 Fallback funktioniert)"
        
        return f"Service {service} Neustart nicht möglich"
    
    def _cleanup_disk(self, issue: Dict) -> str:
        """Räumt Speicherplatz auf"""
        freed = 0
        
        # Alte Logs löschen
        log_dir = self.workspace / 'logs'
        if log_dir.exists():
            for log_file in log_dir.glob('*.log'):
                if log_file.stat().st_mtime < (time.time() - 7*24*3600):  # Älter als 7 Tage
                    size = log_file.stat().st_size
                    log_file.unlink()
                    freed += size
        
        # Alte Backups löschen
        backup_dir = self.workspace / 'neuron' / 'config_backups'
        if backup_dir.exists():
            backups = sorted(backup_dir.glob('*.json'))[:-5]  # Behalte letzte 5
            for backup in backups:
                size = backup.stat().st_size
                backup.unlink()
                freed += size
        
        freed_mb = freed / (1024*1024)
        return f"{freed_mb:.1f} MB freigegeben"
    
    def _clear_cache(self, issue: Dict) -> str:
        """Leert Cache"""
        cache_dir = self.workspace / 'data' / 'memory' / 'cache'
        
        if cache_dir.exists():
            count = 0
            for cache_file in cache_dir.glob('*.json'):
                cache_file.unlink()
                count += 1
            return f"{count} Cache-Dateien gelöscht"
        
        return "Kein Cache zum Löschen"
    
    def _fix_permissions(self, issue: Dict) -> str:
        """Repariert Berechtigungen"""
        file_path = Path(issue['file'])
        
        # Mache ausführbar
        current_mode = file_path.stat().st_mode
        new_mode = current_mode | 0o755
        file_path.chmod(new_mode)
        
        return f"Berechtigungen korrigiert (755)"
    
    def _fix_symlinks(self, issue: Dict) -> str:
        """Repariert defekte Symlinks"""
        link_path = Path(issue['link'])
        
        # Lösche defekten Link
        link_path.unlink()
        
        # Erstelle neu
        target = self.workspace / 'smriti-core' / 'v3.5-enhanced'
        link_path.symlink_to(target, target_is_directory=True)
        
        return f"Symlink neu erstellt -> {target}"
    
    def _rotate_logs(self, issue: Dict) -> str:
        """Rotiert Logs"""
        log_dir = self.workspace / 'logs'
        
        if log_dir.exists():
            for log_file in log_dir.glob('*.log'):
                if log_file.stat().st_size > 10*1024*1024:  # Größer als 10MB
                    # Rotiere
                    rotated = log_file.with_suffix('.log.1')
                    shutil.move(log_file, rotated)
        
        return "Logs rotiert"
    
    def _log_healing(self, issue: Dict, result: str, status: str):
        """Loggt Heilungs-Aktion"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'issue': issue,
            'result': result,
            'status': status
        }
        
        try:
            with open(self.healing_log, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception:
            pass
    
    def get_report(self) -> str:
        """Erzeugt Self-Healing-Report"""
        
        lines = [
            "╔════════════════════════════════════════════════════════════╗",
            "║  SELF-HEALING ENGINE v3.5 — Report                           ║",
            "╚════════════════════════════════════════════════════════════╝",
            "",
            "Reparatur-Strategien:",
        ]
        
        for strategy_name in self.healing_strategies.keys():
            lines.append(f"  • {strategy_name}")
        
        lines.extend([
            "",
            "Letzte Heilungs-Aktionen:",
        ])
        
        try:
            if self.healing_log.exists():
                with open(self.healing_log) as f:
                    entries = f.readlines()[-5:]
                    for entry in entries:
                        data = json.loads(entry)
                        status = '✅' if data.get('status') == 'success' else '❌'
                        lines.append(f"  {status} {data['timestamp'][:10]}: {data['issue']['type']}")
            else:
                lines.append("  Keine Aktionen durchgeführt")
        except Exception:
            lines.append("  Keine Aktionen durchgeführt")
        
        lines.append("")
        
        return '\n'.join(lines)


if __name__ == "__main__":
    # Test
    engine = SelfHealingEngine()
    
    print("🔍 Führe Health-Check durch...")
    health = engine.health_check()
    
    print(f"\nStatus: {health['status']}")
    print(f"Probleme: {health['total_issues']}")
    
    if health['issues']:
        print("\nGefundene Probleme:")
        for issue in health['issues']:
            print(f"  • {issue['description']}")
        
        print("\n🔧 Starte Heilung...")
        results = engine.heal(auto=True)
        for result in results:
            print(f"  {result}")
    else:
        print("\n✅ System gesund!")
    
    print("\n" + engine.get_report())
