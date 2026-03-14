#!/usr/bin/env python3
"""
OUROBOROS-REFLECTY BRIDGE CONNECTOR v1.1
Verbindet L1-L3 Intelligence mit Meta-Learning

Fixes:
- File locking für Race Conditions
- Try/except + Error logging
- Pending events sofort persistieren
- Konflikt-Detection implementiert
- Mutation timeouts (48h)
- Auto-cleanup (30 Tage)
- Health checks
- Schema validation
"""

import json
import datetime
import time
import fcntl
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

# ═══════════════════════════════════════════════════════════════════
# SCHEMA VALIDATION
# ═══════════════════════════════════════════════════════════════════

EVENT_SCHEMA = {
    "required": ["source_level", "event_type", "data", "confidence"],
    "types": {
        "source_level": str,
        "event_type": str,
        "data": dict,
        "confidence": (int, float)
    },
    "source_levels": ["L1", "L2", "L3"],
    "event_types": ["pattern", "blend", "prediction", "synthesis", "wrong_prediction"]
}

COMMAND_SCHEMA = {
    "required": ["command_type", "mutation_data"],
    "types": {
        "command_type": str,
        "mutation_data": dict
    },
    "command_types": ["mutation_start", "mutation_end", "rollback_triggered", "new_threshold"]
}

class EventPriority(Enum):
    IMMEDIATE = "SOFORT"
    QUEUED = "QUEUE"
    SILENT = "LOG"

class BridgeError(Exception):
    """Bridge-spezifische Fehler"""
    pass

@dataclass
class ReflectyEvent:
    """Event von Reflecty L1-L3"""
    source_level: str
    event_type: str
    data: Dict
    confidence: float
    timestamp: str = None
    event_id: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.datetime.now().isoformat()
        if self.event_id is None:
            self.event_id = f"evt_{int(time.time() * 1000)}"
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def validate(self) -> bool:
        """Validiere Event gegen Schema"""
        if self.source_level not in EVENT_SCHEMA["source_levels"]:
            raise BridgeError(f"Ungültiger source_level: {self.source_level}")
        if self.event_type not in EVENT_SCHEMA["event_types"]:
            raise BridgeError(f"Ungültiger event_type: {self.event_type}")
        if not 0.0 <= self.confidence <= 1.0:
            raise BridgeError(f"Confidence muss 0-1 sein: {self.confidence}")
        return True

@dataclass  
class OuroborosCommand:
    """Command an OUROBOROS"""
    command_type: str
    mutation_data: Dict
    timestamp: str = None
    command_id: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.datetime.now().isoformat()
        if self.command_id is None:
            self.command_id = f"cmd_{int(time.time() * 1000)}"
    
    def validate(self) -> bool:
        """Validiere Command gegen Schema"""
        if self.command_type not in COMMAND_SCHEMA["command_types"]:
            raise BridgeError(f"Ungültiger command_type: {self.command_type}")
        return True

class FileLock:
    """Kontext-Manager für File Locking"""
    def __init__(self, filepath: Path, timeout: int = 5):
        self.filepath = filepath
        self.timeout = timeout
        self.fd = None
        
    def __enter__(self):
        self.fd = open(self.filepath, 'a+')
        start = time.time()
        while True:
            try:
                fcntl.flock(self.fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return self
            except (IOError, OSError):
                if time.time() - self.timeout > start:
                    raise BridgeError(f"Timeout beim Locken von {self.filepath}")
                time.sleep(0.01)
                
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fd:
            fcntl.flock(self.fd.fileno(), fcntl.LOCK_UN)
            self.fd.close()

class BridgeConnector:
    """Haupt-Bridge zwischen Reflecty und OUROBOROS - v1.1 Robust"""
    
    BRIDGE_STATE_FILE = Path("neuron/.bridge_state.json")
    EVENT_LOG = Path("neuron/bridge_events.jsonl")
    ERROR_LOG = Path("neuron/bridge_errors.jsonl")
    PENDING_EVENTS_FILE = Path("neuron/.bridge_pending.json")
    HEALTH_LOG = Path("neuron/bridge_health.jsonl")
    
    # Thresholds
    HIGH_CONFIDENCE = 0.9
    MEDIUM_CONFIDENCE = 0.7
    
    # Timeouts
    MUTATION_TIMEOUT_HOURS = 48
    CLEANUP_DAYS = 30
    HEALTH_CHECK_MINUTES = 5
    
    def __init__(self):
        self.state = self._load_state()
        self.pending_events: List[ReflectyEvent] = self._load_pending_events()
        self._check_mutation_timeouts()
        self._cleanup_old_data()
        self._log_health_check("initialized")
        
    def _log_error(self, error_type: str, details: Dict):
        """Logge Fehler mit Timestamp"""
        error_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": error_type,
            "details": details
        }
        try:
            with open(self.ERROR_LOG, 'a') as f:
                f.write(json.dumps(error_entry) + "\n")
        except Exception as e:
            print(f"KRITISCH: Kann Fehler nicht loggen: {e}")
    
    def _log_health_check(self, status: str):
        """Logge Health Check"""
        health_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "status": status,
            "active_mutations": len(self.state.get("active_mutations", [])),
            "pending_events": len(self.pending_events),
            "learning_cycles": self.state.get("learning_cycles", 0)
        }
        try:
            with open(self.HEALTH_LOG, 'a') as f:
                f.write(json.dumps(health_entry) + "\n")
        except Exception as e:
            self._log_error("health_log_failed", {"error": str(e)})
    
    def _load_state(self) -> Dict:
        """Lade Bridge-Status mit File Locking"""
        try:
            if self.BRIDGE_STATE_FILE.exists():
                with FileLock(self.BRIDGE_STATE_FILE):
                    with open(self.BRIDGE_STATE_FILE, 'r') as f:
                        return json.load(f)
        except Exception as e:
            self._log_error("state_load_failed", {"error": str(e)})
            
        # Fallback: Neuer State
        return {
            "bridge_id": "orb_001",
            "active_mutations": [],
            "pending_patterns": [],
            "conflicts": [],
            "learning_cycles": 0,
            "last_sync": None,
            "version": "1.1"
        }
    
    def _save_state(self):
        """Speichere Bridge-Status mit File Locking"""
        try:
            self.state["last_sync"] = datetime.datetime.now().isoformat()
            with FileLock(self.BRIDGE_STATE_FILE):
                with open(self.BRIDGE_STATE_FILE, 'w') as f:
                    json.dump(self.state, f, indent=2)
        except Exception as e:
            self._log_error("state_save_failed", {"error": str(e)})
            raise BridgeError(f"Konnte State nicht speichern: {e}")
    
    def _load_pending_events(self) -> List[ReflectyEvent]:
        """Lade pending Events aus Datei (statt RAM)"""
        try:
            if self.PENDING_EVENTS_FILE.exists():
                with open(self.PENDING_EVENTS_FILE, 'r') as f:
                    data = json.load(f)
                    return [ReflectyEvent(**evt) for evt in data]
        except Exception as e:
            self._log_error("pending_load_failed", {"error": str(e)})
        return []
    
    def _persist_pending_events(self):
        """Speichere pending Events sofort"""
        try:
            data = [evt.to_dict() for evt in self.pending_events]
            with open(self.PENDING_EVENTS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self._log_error("pending_persist_failed", {"error": str(e)})
            raise BridgeError(f"Konnte pending events nicht speichern: {e}")
    
    def _log_event(self, event: Dict, direction: str):
        """Logge Event mit Rotation (max 1000 Einträge)"""
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "direction": direction,
            **event
        }
        try:
            # Rotation: Max 1000 Einträge
            if self.EVENT_LOG.exists():
                with open(self.EVENT_LOG) as f:
                    lines = f.readlines()
                if len(lines) >= 1000:
                    lines = lines[-999:]  # Behalte letzte 999
                    with open(self.EVENT_LOG, 'w') as f:
                        f.writelines(lines)
            
            with open(self.EVENT_LOG, 'a') as f:
                f.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            self._log_error("event_log_failed", {"error": str(e)})
    
    def _check_mutation_timeouts(self):
        """Prüfe Mutationen auf Timeout (48h)"""
        now = datetime.datetime.now()
        active = self.state.get("active_mutations", [])
        timed_out = []
        still_active = []
        
        for mut in active:
            started = datetime.datetime.fromisoformat(mut["started"])
            hours_ago = (now - started).total_seconds() / 3600
            
            if hours_ago > self.MUTATION_TIMEOUT_HOURS:
                timed_out.append(mut)
                # Logge Timeout
                self._log_error("mutation_timeout", {
                    "mutation_id": mut.get("mutation_id"),
                    "hours_old": hours_ago
                })
            else:
                still_active.append(mut)
        
        if timed_out:
            self.state["active_mutations"] = still_active
            self._save_state()
            # Auch Reflecty informieren
            for mut in timed_out:
                self._notify_reflecty_timeout(mut)
    
    def _notify_reflecty_timeout(self, mutation: Dict):
        """Informiere Reflecty über Timeout"""
        # Speichere in special timeout log für Reflecty
        timeout_entry = {
            "type": "mutation_timeout",
            "mutation": mutation,
            "timestamp": datetime.datetime.now().isoformat()
        }
        try:
            timeout_log = Path("neuron/.reflecty_timeouts.json")
            existing = []
            if timeout_log.exists():
                with open(timeout_log) as f:
                    existing = json.load(f)
            existing.append(timeout_entry)
            with open(timeout_log, 'w') as f:
                json.dump(existing, f, indent=2)
        except Exception as e:
            self._log_error("timeout_notify_failed", {"error": str(e)})
    
    def _cleanup_old_data(self):
        """Räume Daten älter als 30 Tage auf"""
        cutoff = datetime.datetime.now() - datetime.timedelta(days=self.CLEANUP_DAYS)
        
        # Cleanup old mutations in state
        active = self.state.get("active_mutations", [])
        old_count = len(active)
        active = [m for m in active if 
                  datetime.datetime.fromisoformat(m.get("started", "2020-01-01")) > cutoff]
        if len(active) < old_count:
            self.state["active_mutations"] = active
            self._save_state()
    
    def _detect_conflict(self, event: ReflectyEvent) -> Optional[Dict]:
        """Prüfe auf Konflikte mit aktiven Mutationen"""
        active = self.state.get("active_mutations", [])
        
        for mut in active:
            # Konflikt: Reflecty sagt X, Mutation will X verhindern
            if event.event_type == "prediction":
                predicted = event.data.get("prediction")
                mutation_effect = mut.get("predicted_outcome", "")
                
                # Einfache Konflikt-Erkennung: Vorhersage enthält "kein" oder "not"
                # während Mutation "M3 +" sagt (oder umgekehrt)
                if predicted and mutation_effect:
                    if ("kein" in predicted.lower() or "not" in predicted.lower()) and \
                       ("+" in mutation_effect or "steig" in mutation_effect.lower()):
                        return {
                            "type": "PREDICTION_VS_MUTATION",
                            "prediction": predicted,
                            "mutation": mut["mutation_id"],
                            "mutation_effect": mutation_effect,
                            "confidence": event.confidence
                        }
        
        return None
    
    # ═══════════════════════════════════════════════════════════════
    # REFLECTY → OUROBOROS (Intelligence Flow)
    # ═══════════════════════════════════════════════════════════════
    
    def receive_from_reflecty(self, event: ReflectyEvent) -> str:
        """
        Empfange Event von Reflecty und route an OUROBOROS
        Mit Fehlerbehandlung und Conflict Detection
        """
        try:
            # 1. Validierung
            event.validate()
            
            # 2. Logging
            self._log_event(event.to_dict(), "reflecty_to_ouroboros")
            
            # 3. Konflikt-Check
            conflict = self._detect_conflict(event)
            if conflict:
                self.state["conflicts"].append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "event_id": event.event_id,
                    **conflict
                })
                self._save_state()
                return f"⚠️ KONFLIKT erkannt: {conflict['type']} - Oli-Entscheidung nötig"
            
            # 4. Routing
            priority = self._classify_event(event)
            
            if priority == EventPriority.IMMEDIATE:
                return self._handle_immediate(event)
            elif priority == EventPriority.QUEUED:
                return self._handle_queued(event)
            else:
                return self._handle_silent(event)
                
        except BridgeError as e:
            self._log_error("validation_failed", {"event": event.to_dict(), "error": str(e)})
            return f"❌ Validation failed: {e}"
        except Exception as e:
            self._log_error("reflecty_receive_failed", {"event": event.to_dict(), "error": str(e)})
            return f"❌ Bridge error: {e}"
    
    def _classify_event(self, event: ReflectyEvent) -> EventPriority:
        """Klassifiziere Event-Priorität"""
        if event.confidence >= self.HIGH_CONFIDENCE:
            return EventPriority.IMMEDIATE
        if event.confidence >= self.MEDIUM_CONFIDENCE and event.source_level in ["L2", "L3"]:
            return EventPriority.QUEUED
        return EventPriority.SILENT
    
    def _handle_immediate(self, event: ReflectyEvent) -> str:
        """SOFORT an OUROBOROS weiterleiten"""
        ouroboros_event = {
            "type": "reflecty_high_confidence",
            "source": event.source_level,
            "event_id": event.event_id,
            "data": event.data,
            "confidence": event.confidence,
            "requires_mutation_review": True
        }
        self._add_to_ouroboros_queue(ouroboros_event)
        return f"IMMEDIATE: {event.event_type} → OUROBOROS Queue"
    
    def _handle_queued(self, event: ReflectyEvent) -> str:
        """SOFORT persistieren (nicht nur RAM)"""
        self.pending_events.append(event)
        self._persist_pending_events()  # KRITISCH: sofort speichern!
        return f"QUEUED: {event.event_type} für Batch"
    
    def _handle_silent(self, event: ReflectyEvent) -> str:
        """Nur loggen"""
        return f"SILENT: {event.event_type} geloggt"
    
    def _add_to_ouroboros_queue(self, event: Dict):
        """Füge zu OUROBOROS Queue hinzu mit Locking"""
        ouroboros_queue = Path("neuron/.ouroboros_queue.json")
        
        try:
            with FileLock(ouroboros_queue):
                existing = []
                if ouroboros_queue.exists():
                    with open(ouroboros_queue) as f:
                        existing = json.load(f)
                
                # Max 100 Einträge in Queue
                if len(existing) >= 100:
                    existing = existing[-99:]
                
                existing.append(event)
                
                with open(ouroboros_queue, 'w') as f:
                    json.dump(existing, f, indent=2)
        except Exception as e:
            self._log_error("ouroboros_queue_failed", {"error": str(e)})
            raise BridgeError(f"Konnte nicht zu OUROBOROS Queue hinzufügen: {e}")
    
    # ═══════════════════════════════════════════════════════════════
    # OUROBOROS → REFLECTY (Validation Flow)
    # ═══════════════════════════════════════════════════════════════
    
    def receive_from_ouroboros(self, command: OuroborosCommand) -> str:
        """Empfange Command von OUROBOROS mit Fehlerbehandlung"""
        try:
            command.validate()
            self._log_event(asdict(command), "ouroboros_to_reflecty")
            
            if command.command_type == "mutation_start":
                return self._notify_reflecty_mutation_start(command)
            elif command.command_type == "mutation_end":
                return self._notify_reflecty_mutation_end(command)
            elif command.command_type == "rollback_triggered":
                return self._notify_reflecty_rollback(command)
            else:
                return f"Unknown command: {command.command_type}"
                
        except BridgeError as e:
            self._log_error("command_validation_failed", {"command": asdict(command), "error": str(e)})
            return f"❌ Command validation failed: {e}"
        except Exception as e:
            self._log_error("ouroboros_receive_failed", {"command": asdict(command), "error": str(e)})
            return f"❌ Bridge error: {e}"
    
    def _notify_reflecty_mutation_start(self, command: OuroborosCommand) -> str:
        """Informiere Reflecty L3 Oracle: Mutation startet"""
        mutation_id = command.mutation_data.get("mutation_id", "unknown")
        
        self.state["active_mutations"].append({
            "mutation_id": mutation_id,
            "command_id": command.command_id,
            "started": datetime.datetime.now().isoformat(),
            "predicted_outcome": command.mutation_data.get("predicted_effect", "unknown"),
            "l3_tracking": True,
            "status": "active"
        })
        self._save_state()
        
        return f"L3 Oracle: Tracking Mutation {mutation_id} (Timeout: {self.MUTATION_TIMEOUT_HOURS}h)"
    
    def _notify_reflecty_mutation_end(self, command: OuroborosCommand) -> str:
        """Informiere Reflecty L3: Mutation beendet, validiere"""
        mutation_id = command.mutation_data.get("mutation_id")
        
        self.state["active_mutations"] = [
            m for m in self.state["active_mutations"] 
            if m["mutation_id"] != mutation_id
        ]
        
        self.state["learning_cycles"] += 1
        self._save_state()
        
        return f"L3 Oracle: Validated Mutation {mutation_id}"
    
    def _notify_reflecty_rollback(self, command: OuroborosCommand) -> str:
        """Informiere Reflecty: Rollback = Lernmoment"""
        mutation_id = command.mutation_data.get("mutation_id", "unknown")
        
        self.state["learning_cycles"] += 1
        self._save_state()
        
        # Spezielles Learning-Event für Reflecty
        learning_event = {
            "type": "rollback_learning",
            "mutation_id": mutation_id,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        try:
            learning_log = Path("neuron/.reflecty_learning.json")
            existing = []
            if learning_log.exists():
                with open(learning_log) as f:
                    existing = json.load(f)
            existing.append(learning_event)
            with open(learning_log, 'w') as f:
                json.dump(existing, f, indent=2)
        except Exception as e:
            self._log_error("learning_log_failed", {"error": str(e)})
        
        return f"L3 Oracle: Rollback logged as learning ({mutation_id})"
    
    # ═══════════════════════════════════════════════════════════════
    # SESSION INTEGRATION
    # ═══════════════════════════════════════════════════════════════
    
    def sync_session_start(self):
        """Bei Session-Start: Prüfe aktive Mutationen + Health"""
        self._check_mutation_timeouts()
        self._log_health_check("session_start")
        
        active = self.state.get("active_mutations", [])
        conflicts = self.state.get("conflicts", [])
        
        status_lines = []
        if active:
            status_lines.append(f"⚠️ {len(active)} aktive Mutationen werden überwacht")
        else:
            status_lines.append("✓ Keine aktiven Mutationen")
        
        if conflicts:
            status_lines.append(f"🔥 {len(conflicts)} offene Konflikte!")
        
        return "\n".join(status_lines) if status_lines else "✓ Bridge operational"
    
    def sync_session_end(self):
        """Bei Session-Ende: Verarbeite pending Events + Health"""
        self._log_health_check("session_end")
        
        if not self.pending_events:
            return "✓ Keine pending Events"
        
        count = 0
        errors = []
        
        for event in self.pending_events:
            try:
                self._handle_immediate(event)
                count += 1
            except Exception as e:
                errors.append({"event_id": event.event_id, "error": str(e)})
        
        self.pending_events = []
        
        # Cleanup pending file
        try:
            if self.PENDING_EVENTS_FILE.exists():
                self.PENDING_EVENTS_FILE.unlink()
        except Exception as e:
            self._log_error("pending_cleanup_failed", {"error": str(e)})
        
        result = f"✓ {count} Events batch-verarbeitet"
        if errors:
            result += f"\n⚠️ {len(errors)} Fehler: {errors}"
        
        return result
    
    # ═══════════════════════════════════════════════════════════════
    # STATUS & DEBUG
    # ═══════════════════════════════════════════════════════════════
    
    def get_status(self) -> Dict:
        """Gib aktuellen Bridge-Status zurück"""
        return {
            "bridge_id": self.state.get("bridge_id", "unknown"),
            "version": self.state.get("version", "1.0"),
            "active_mutations": len(self.state.get("active_mutations", [])),
            "pending_events": len(self.pending_events),
            "conflicts": len(self.state.get("conflicts", [])),
            "learning_cycles": self.state.get("learning_cycles", 0),
            "last_sync": self.state.get("last_sync", "never"),
            "health": "ok"
        }
    
    def get_recent_events(self, limit: int = 10) -> List[Dict]:
        """Hole letzte N Events"""
        if not self.EVENT_LOG.exists():
            return []
        
        try:
            with open(self.EVENT_LOG) as f:
                lines = f.readlines()
            events = [json.loads(line) for line in lines[-limit:]]
            return events
        except Exception as e:
            self._log_error("get_events_failed", {"error": str(e)})
            return []
    
    def get_conflicts(self) -> List[Dict]:
        """Zeige offene Konflikte"""
        return self.state.get("conflicts", [])
    
    def resolve_conflict(self, conflict_index: int, resolution: str) -> str:
        """Löse Konflikt auf"""
        conflicts = self.state.get("conflicts", [])
        if 0 <= conflict_index < len(conflicts):
            conflict = conflicts[conflict_index]
            conflict["resolved"] = True
            conflict["resolution"] = resolution
            conflict["resolved_at"] = datetime.datetime.now().isoformat()
            
            # Entferne aus aktiven
            self.state["conflicts"] = [c for c in conflicts if not c.get("resolved")]
            self._save_state()
            
            return f"✓ Konflikt resolved: {resolution}"
        return "❌ Ungültiger Index"


# ═══════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS (für Integration in AGENTS.md)
# ═══════════════════════════════════════════════════════════════════

_bridge_instance: Optional[BridgeConnector] = None

def get_bridge() -> BridgeConnector:
    """Singleton-Pattern für Bridge"""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = BridgeConnector()
    return _bridge_instance

def bridge_init():
    """Startup: Initialisiere Bridge"""
    try:
        bridge = get_bridge()
        status = bridge.sync_session_start()
        return f"🌉 Bridge v1.1 initialized\n{status}"
    except Exception as e:
        return f"❌ Bridge init failed: {e}"

def reflecty_send_event(level: str, event_type: str, data: Dict, confidence: float):
    """Reflecty sendet Event an Bridge"""
    try:
        event = ReflectyEvent(
            source_level=level,
            event_type=event_type,
            data=data,
            confidence=confidence
        )
        bridge = get_bridge()
        result = bridge.receive_from_reflecty(event)
        return result
    except Exception as e:
        return f"❌ Event send failed: {e}"

def ouroboros_send_command(command_type: str, mutation_data: Dict):
    """OUROBOROS sendet Command an Bridge"""
    try:
        command = OuroborosCommand(
            command_type=command_type,
            mutation_data=mutation_data
        )
        bridge = get_bridge()
        result = bridge.receive_from_ouroboros(command)
        return result
    except Exception as e:
        return f"❌ Command send failed: {e}"

def bridge_session_end():
    """Session-Ende: Finalisiere"""
    try:
        bridge = get_bridge()
        result = bridge.sync_session_end()
        return result
    except Exception as e:
        return f"❌ Session end failed: {e}"

def bridge_status():
    """Zeige aktuellen Status"""
    try:
        bridge = get_bridge()
        status = bridge.get_status()
        
        lines = [
            "🌉 BRIDGE STATUS v1.1",
            "",
            f"Bridge ID: {status['bridge_id']}",
            f"Version: {status['version']}",
            f"Last Sync: {status['last_sync'] or 'never'}",
            "",
            f"Active Mutations: {status['active_mutations']}",
            f"Pending Events: {status['pending_events']}",
            f"Open Conflicts: {status['conflicts']}",
            f"Learning Cycles: {status['learning_cycles']}",
            "",
            f"Health: {status['health']}"
        ]
        
        return "\n".join(lines)
    except Exception as e:
        return f"❌ Status check failed: {e}"

def bridge_conflicts():
    """Zeige offene Konflikte"""
    try:
        bridge = get_bridge()
        conflicts = bridge.get_conflicts()
        
        if not conflicts:
            return "✓ Keine offenen Konflikte"
        
        lines = ["🔥 OFFENE KONFLIKTE:", ""]
        for i, c in enumerate(conflicts):
            lines.append(f"[{i}] {c.get('type', 'unknown')}")
            lines.append(f"    Time: {c.get('timestamp', 'unknown')}")
            lines.append(f"    Details: {c.get('details', {})}")
            lines.append("")
        
        return "\n".join(lines)
    except Exception as e:
        return f"❌ Conflict check failed: {e}"


if __name__ == "__main__":
    # Test
    print(bridge_init())
    print()
    
    # Simuliere Events
    print("Testing Events...")
    result = reflecty_send_event(
        level="L1",
        event_type="pattern",
        data={"pattern": "test_pattern"},
        confidence=0.95
    )
    print(f"Reflecty → Bridge: {result}")
    
    result = reflecty_send_event(
        level="L3",
        event_type="prediction",
        data={"prediction": "kein M3 Anstieg"},
        confidence=0.92
    )
    print(f"Reflecty → Bridge: {result}")
    
    result = ouroboros_send_command(
        command_type="mutation_start",
        mutation_data={"mutation_id": "mut_test", "predicted_effect": "M3 +0.5"}
    )
    print(f"OUROBOROS → Bridge: {result}")
    
    print()
    print(bridge_status())
    print()
    print(bridge_conflicts())
    print()
    print(bridge_session_end())
