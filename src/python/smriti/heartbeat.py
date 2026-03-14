#!/usr/bin/env python3
"""
Heartbeat v3.5 — Professional System Health Monitor

Based on OpenClaw Gateway Heartbeat specification:
- Lightweight (<200 lines)
- Non-intrusive
- Self-contained
- Production-ready

Features:
- M1-M5 metrics tracking
- Simple trend detection
- Health status reporting
- Automatic log rotation
- Configurable thresholds
"""

import json
import os
import time
import fcntl
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

@dataclass
class HealthMetrics:
    """Core health metrics for Smriti"""
    timestamp: str
    m1_predictive_surprise: float  # 0-5
    m2_denkraum_expansion: float  # 0-5
    m3_paradigm_shift: float       # 0-5
    m4_session_velocity: float    # 0-5
    m5_anti_fragile_resonanz: float  # 0-5
    overall_score: float          # Average
    status: str                   # healthy|warning|critical
    
    def to_dict(self) -> Dict:
        return asdict(self)

class Heartbeat:
    """
    Professional Heartbeat Monitor
    
    Design Principles:
    1. Single Responsibility: Only monitoring, no healing
    2. Fail-Safe: Never crashes, always returns status
    3. Efficient: Minimal resource usage
    4. Clear: Simple, understandable output
    """
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace or os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace'))
        self.metrics_file = self.workspace / 'neuron' / 'heartbeat_metrics.jsonl'
        self.status_file = self.workspace / 'neuron' / '.heartbeat_status'
        
        # Ensure directory exists
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Thresholds (configurable)
        self.thresholds = {
            'healthy': 3.5,
            'warning': 2.5,
            'critical': 2.0
        }
    
    def record(self, m1: float, m2: float, m3: float, m4: float, m5: float) -> HealthMetrics:
        """
        Record a new health measurement
        
        Args:
            m1-m5: Metric scores (0.0 - 5.0)
            
        Returns:
            HealthMetrics object with calculated status
        """
        # Calculate overall score
        overall = round((m1 + m2 + m3 + m4 + m5) / 5, 2)
        
        # Determine status
        if overall >= self.thresholds['healthy']:
            status = 'healthy'
        elif overall >= self.thresholds['warning']:
            status = 'warning'
        else:
            status = 'critical'
        
        # Create metrics object
        metrics = HealthMetrics(
            timestamp=datetime.now().isoformat(),
            m1_predictive_surprise=round(m1, 2),
            m2_denkraum_expansion=round(m2, 2),
            m3_paradigm_shift=round(m3, 2),
            m4_session_velocity=round(m4, 2),
            m5_anti_fragile_resonanz=round(m5, 2),
            overall_score=overall,
            status=status
        )
        
        # Save to file
        self._save_metrics(metrics)
        
        # Update status file
        self._update_status_file(metrics)
        
        return metrics
    
    def get_status(self) -> Dict:
        """
        Get current system health status
        
        Returns:
            Dict with current status and last metrics
        """
        try:
            # Read last metrics
            last_metrics = self._get_last_metrics()
            
            if not last_metrics:
                return {
                    'status': 'unknown',
                    'message': 'No metrics recorded yet',
                    'last_update': None
                }
            
            # Calculate trend (last 3 entries)
            trend = self._calculate_trend()
            
            return {
                'status': last_metrics.status,
                'overall_score': last_metrics.overall_score,
                'last_update': last_metrics.timestamp,
                'trend': trend,
                'metrics': last_metrics.to_dict()
            }
            
        except Exception as e:
            # Fail-safe: return error status
            return {
                'status': 'error',
                'message': str(e),
                'last_update': None
            }
    
    def get_dashboard(self) -> str:
        """
        Generate a simple text dashboard
        
        Returns:
            Formatted dashboard string
        """
        status = self.get_status()
        
        if status['status'] == 'unknown':
            return "Heartbeat: No data yet"
        
        if status['status'] == 'error':
            return f"Heartbeat: Error - {status['message']}"
        
        metrics = status['metrics']
        trend = status.get('trend', '→')
        
        # Status emoji
        emoji = {'healthy': '🟢', 'warning': '🟡', 'critical': '🔴'}.get(status['status'], '⚪')
        
        lines = [
            f"{emoji} Heartbeat v3.5 — {status['status'].upper()}",
            f"Overall: {metrics['overall_score']}/5.0 {trend}",
            f"M1: {metrics['m1_predictive_surprise']} | M2: {metrics['m2_denkraum_expansion']} | M3: {metrics['m3_paradigm_shift']}",
            f"M4: {metrics['m4_session_velocity']} | M5: {metrics['m5_anti_fragile_resonanz']}",
            f"Last update: {status['last_update'][:19] if status['last_update'] else 'N/A'}"
        ]
        
        return '\n'.join(lines)
    
    def get_recommendations(self) -> List[str]:
        """
        Get simple recommendations based on metrics
        
        Returns:
            List of recommendation strings
        """
        status = self.get_status()
        recommendations = []
        
        if status['status'] == 'unknown':
            return ["No data yet. Record some sessions first."]
        
        if status['status'] == 'error':
            return [f"Error: {status['message']}"]
        
        metrics = status['metrics']
        
        # Check individual metrics
        if metrics['m1_predictive_surprise'] < 3.0:
            recommendations.append("M1: Try to introduce more novel concepts")
        
        if metrics['m2_denkraum_expansion'] < 3.0:
            recommendations.append("M2: Use more frameworks and models")
        
        if metrics['m3_paradigm_shift'] < 2.5:
            recommendations.append("M3: Watch for shifts in understanding")
        
        if metrics['m4_session_velocity'] < 3.0:
            recommendations.append("M4: Sessions could be more productive")
        
        if metrics['m5_anti_fragile_resonanz'] < 3.0:
            recommendations.append("M5: Use criticism more productively")
        
        if not recommendations:
            recommendations.append("All metrics look good! Keep it up.")
        
        return recommendations
    
    def rotate_logs(self, max_age_days: int = 7) -> int:
        """
        Rotate old log files
        
        Args:
            max_age_days: Delete logs older than this
            
        Returns:
            Number of files deleted
        """
        deleted = 0
        cutoff = time.time() - (max_age_days * 24 * 3600)
        
        try:
            if self.metrics_file.exists():
                # Check file age
                if self.metrics_file.stat().st_mtime < cutoff:
                    # Archive instead of delete
                    archive = self.metrics_file.with_suffix('.jsonl.old')
                    self.metrics_file.rename(archive)
                    deleted += 1
        except Exception:
            pass
        
        return deleted
    
    def _save_metrics(self, metrics: HealthMetrics):
        """Save metrics to file with locking"""
        try:
            with open(self.metrics_file, 'a') as f:
                # Lock file for exclusive access
                fcntl.flock(f, fcntl.LOCK_EX)
                try:
                    f.write(json.dumps(metrics.to_dict()) + '\n')
                finally:
                    fcntl.flock(f, fcntl.LOCK_UN)
        except Exception as e:
            # Log error but don't crash
            print(f"[Heartbeat] Warning: Could not save metrics: {e}")
    
    def _update_status_file(self, metrics: HealthMetrics):
        """Update quick status file"""
        try:
            with open(self.status_file, 'w') as f:
                f.write(f"{metrics.status}\n{metrics.overall_score}\n{metrics.timestamp}")
        except Exception:
            pass
    
    def _get_last_metrics(self) -> Optional[HealthMetrics]:
        """Get last recorded metrics"""
        try:
            if not self.metrics_file.exists():
                return None
            
            with open(self.metrics_file, 'r') as f:
                lines = f.readlines()
                if not lines:
                    return None
                
                last_line = lines[-1].strip()
                data = json.loads(last_line)
                
                return HealthMetrics(**data)
        except Exception:
            return None
    
    def _calculate_trend(self) -> str:
        """Calculate simple trend from last 3 entries"""
        try:
            if not self.metrics_file.exists():
                return '→'
            
            with open(self.metrics_file, 'r') as f:
                lines = f.readlines()
                if len(lines) < 3:
                    return '→'
                
                # Get last 3 scores
                scores = []
                for line in lines[-3:]:
                    data = json.loads(line.strip())
                    scores.append(data['overall_score'])
                
                # Simple trend
                if scores[-1] > scores[0] + 0.3:
                    return '↗'
                elif scores[-1] < scores[0] - 0.3:
                    return '↘'
                else:
                    return '→'
        except Exception:
            return '→'


# Convenience function
def get_heartbeat(workspace: str = None) -> Heartbeat:
    """Get Heartbeat instance"""
    return Heartbeat(workspace)


if __name__ == "__main__":
    # Test
    hb = get_heartbeat()
    
    # Record test metrics
    metrics = hb.record(
        m1=4.2,
        m2=3.8,
        m3=3.5,
        m4=4.0,
        m5=3.2
    )
    
    print(hb.get_dashboard())
    print("\nRecommendations:")
    for rec in hb.get_recommendations():
        print(f"  • {rec}")
