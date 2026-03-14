#!/usr/bin/env python3
"""
Heartbeat Monitor v3.5 — Echtzeit-Monitoring + Trend-Analyse

Integriert mit Smriti v3.5 für automatische Health-Überwachung.
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import deque

class HeartbeatMonitor:
    """Überwacht M1-M5 in Echtzeit und erkennt Trends"""
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace or os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace'))
        self.log_file = self.workspace / 'neuron' / 'm1m4_log.jsonl'
        self.trend_file = self.workspace / 'neuron' / 'trends_weekly.json'
        self.alert_file = self.workspace / 'neuron' / 'heartbeat_alerts.jsonl'
        
        # Speicher für Echtzeit-Analyse
        self.session_buffer = deque(maxlen=10)  # Letzte 10 Sessions
        self.metrics_history = {
            'm1': deque(maxlen=100),
            'm2': deque(maxlen=100),
            'm3': deque(maxlen=100),
            'm4': deque(maxlen=100),
            'm5': deque(maxlen=100)
        }
        
        # Thresholds für Alerts
        self.thresholds = {
            'm1': {'warning': 3.0, 'critical': 2.0},
            'm2': {'warning': 2.5, 'critical': 1.5},
            'm3': {'warning': 2.0, 'critical': 1.0},
            'm4': {'warning': 2.5, 'critical': 1.5},
            'm5': {'warning': 2.5, 'critical': 1.5}
        }
    
    def record_session(self, metrics: Dict) -> Dict:
        """Speichert eine Session und analysiert Trends"""
        
        # Zu Buffer hinzufügen
        self.session_buffer.append(metrics)
        
        # Zu History hinzufügen
        for key in ['m1', 'm2', 'm3', 'm4', 'm5']:
            if key in metrics and isinstance(metrics[key], dict):
                score = metrics[key].get('score', 0)
                self.metrics_history[key].append(score)
        
        # Trend-Analyse durchführen
        trends = self._analyze_trends()
        
        # Prädiktive Alerts prüfen
        alerts = self._check_predictive_alerts()
        
        # Speichern
        self._save_metrics(metrics, trends, alerts)
        
        return {
            'metrics': metrics,
            'trends': trends,
            'alerts': alerts,
            'status': self._calculate_overall_status(trends)
        }
    
    def _analyze_trends(self) -> Dict:
        """Analysiert Trends über die letzten Sessions"""
        
        trends = {}
        
        for metric_name, history in self.metrics_history.items():
            if len(history) < 3:
                trends[metric_name] = {'trend': 'insufficient_data', 'direction': '→'}
                continue
            
            # Letzte 3 Werte
            recent = list(history)[-3:]
            
            # Trend berechnen
            if recent[-1] > recent[0] + 0.3:
                trend = 'improving'
                direction = '↗'
            elif recent[-1] < recent[0] - 0.3:
                trend = 'declining'
                direction = '↘'
            else:
                trend = 'stable'
                direction = '→'
            
            # Durchschnitt
            avg = sum(recent) / len(recent)
            
            trends[metric_name] = {
                'trend': trend,
                'direction': direction,
                'average': round(avg, 2),
                'current': recent[-1],
                'change': round(recent[-1] - recent[0], 2)
            }
        
        return trends
    
    def _check_predictive_alerts(self) -> List[Dict]:
        """Prüft auf prädiktive Alerts"""
        
        alerts = []
        
        for metric_name, history in self.metrics_history.items():
            if len(history) < 3:
                continue
            
            recent = list(history)[-3:]
            current = recent[-1]
            threshold = self.thresholds.get(metric_name, {})
            
            # Kritischer Alert
            if current < threshold.get('critical', 2.0):
                alerts.append({
                    'level': 'critical',
                    'metric': metric_name,
                    'message': f'{metric_name.upper()} kritisch niedrig ({current})',
                    'action': f'Auto-tuning für {metric_name} empfohlen',
                    'timestamp': datetime.now().isoformat()
                })
            # Warning
            elif current < threshold.get('warning', 3.0):
                alerts.append({
                    'level': 'warning',
                    'metric': metric_name,
                    'message': f'{metric_name.upper()} unter Warning-Threshold ({current})',
                    'action': f'Überwachung empfohlen',
                    'timestamp': datetime.now().isoformat()
                })
            
            # Trend-Alert (3x fallend)
            if len(recent) >= 3 and all(recent[i] > recent[i+1] for i in range(len(recent)-1)):
                if recent[-1] < 3.5:
                    alerts.append({
                        'level': 'trend',
                        'metric': metric_name,
                        'message': f'{metric_name.upper()} fällt seit 3 Sessions',
                        'action': 'Intervention prüfen',
                        'timestamp': datetime.now().isoformat()
                    })
        
        return alerts
    
    def _calculate_overall_status(self, trends: Dict) -> str:
        """Berechnet den Gesamt-Status"""
        
        critical_count = sum(1 for t in trends.values() if t.get('trend') == 'declining')
        
        if critical_count >= 3:
            return '🔴 critical'
        elif critical_count >= 1:
            return '🟡 warning'
        else:
            return '🟢 healthy'
    
    def _save_metrics(self, metrics: Dict, trends: Dict, alerts: List):
        """Speichert alle Daten"""
        
        # Zu Log-Datei hinzufügen
        entry = {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'trends': trends,
            'alert_count': len(alerts)
        }
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception:
            pass
        
        # Alerts speichern
        for alert in alerts:
            try:
                with open(self.alert_file, 'a') as f:
                    f.write(json.dumps(alert) + '\n')
            except Exception:
                pass
    
    def get_dashboard(self) -> str:
        """Erzeugt ein Text-Dashboard"""
        
        trends = self._analyze_trends()
        status = self._calculate_overall_status(trends)
        
        lines = [
            "╔════════════════════════════════════════════════════════════╗",
            "║  HEARTBEAT v3.5 — Dashboard                                ║",
            "╚════════════════════════════════════════════════════════════╝",
            "",
            f"Status: {status}",
            f"Letzte Update: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "Metriken:",
        ]
        
        for metric_name, trend in trends.items():
            if 'average' in trend:
                bar = '█' * int(trend['average']) + '░' * (5 - int(trend['average']))
                lines.append(f"  {metric_name.upper():2} {bar} {trend['average']:.1f}/5 {trend['direction']}")
        
        lines.extend([
            "",
            "Trends:",
        ])
        
        for metric_name, trend in trends.items():
            if 'trend' in trend:
                emoji = {'improving': '🟢', 'stable': '🟡', 'declining': '🔴'}.get(trend['trend'], '⚪')
                lines.append(f"  {emoji} {metric_name.upper()}: {trend['trend']}")
        
        lines.extend([
            "",
            "Nächste Wartung: 2026-03-21",
            "",
        ])
        
        return '\n'.join(lines)
    
    def get_recommendations(self) -> List[str]:
        """Gibt Empfehlungen basierend auf Trends"""
        
        recommendations = []
        trends = self._analyze_trends()
        
        for metric_name, trend in trends.items():
            if trend.get('trend') == 'declining':
                if metric_name == 'm1':
                    recommendations.append(f"🎯 M1 fällt: Überrasche mehr mit neuen Konzepten")
                elif metric_name == 'm2':
                    recommendations.append(f"🎯 M2 fällt: Nutze mehr Frameworks/Modelle")
                elif metric_name == 'm3':
                    recommendations.append(f"🎯 M3 fällt: Achte mehr auf Paradigmen-Shifts")
                elif metric_name == 'm4':
                    recommendations.append(f"🎯 M4 fällt: Beschleunige die Iteration")
                elif metric_name == 'm5':
                    recommendations.append(f"🎯 M5 fällt: Nutze Kritik produktiver")
        
        return recommendations if recommendations else ["✅ Alle Metriken stabil"]


# Singleton für einfachen Zugriff
_monitor = None

def get_monitor():
    """Singleton Pattern"""
    global _monitor
    if _monitor is None:
        _monitor = HeartbeatMonitor()
    return _monitor


if __name__ == "__main__":
    # Test
    monitor = get_monitor()
    
    # Simuliere einige Sessions
    for i in range(5):
        metrics = {
            'm1': {'score': 3.5 + i * 0.1},
            'm2': {'score': 3.0 + i * 0.05},
            'm3': {'score': 2.5},
            'm4': {'score': 4.0},
            'm5': {'score': 2.8 - i * 0.1}  # Fällt absichtlich
        }
        
        result = monitor.record_session(metrics)
        print(f"Session {i+1}: {result['status']}")
    
    print("\n" + monitor.get_dashboard())
    print("\nEmpfehlungen:")
    for rec in monitor.get_recommendations():
        print(f"  {rec}")
