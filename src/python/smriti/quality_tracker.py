#!/usr/bin/env python3
"""
Genius Quality Tracker v2.0 — Misst die 5 Meta-Metriken

Integriert mit Session-Logger und OpenClaw.

Usage:
    python quality_tracker.py --session-file <path>
    python quality_tracker.py --analyze-last-session
    python quality_tracker.py --mode continuous

Environment Variables:
    SMRITI_WORKSPACE — Workspace path
    SMRITI_LOG_LEVEL — debug|info|warn|error
"""

import json
import re
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
import hashlib

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

WORKSPACE = Path(os.environ.get('SMRITI_WORKSPACE', Path.home() / '.openclaw/workspace'))
LOG_LEVEL = os.environ.get('SMRITI_LOG_LEVEL', 'info')

LOG_LEVELS = {'debug': 0, 'info': 1, 'warn': 2, 'error': 3}

def log(level: str, message: str, data: Dict = None):
    """Structured logging"""
    if LOG_LEVELS.get(level, 1) >= LOG_LEVELS.get(LOG_LEVEL, 1):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            **(data or {})
        }
        print(f"[{level.upper()}] {message}")
        
        # Persist to log file
        try:
            log_dir = WORKSPACE / 'logs'
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / 'quality_tracker.log'
            with open(log_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception:
            pass

# ═══════════════════════════════════════════════════════════════════
# QUALITY TRACKER
# ═══════════════════════════════════════════════════════════════════

class GeniusQualityTracker:
    """Misst Qualität über traditionelle Metriken hinaus"""
    
    def __init__(self, workspace: Path = WORKSPACE):
        self.workspace = workspace
        self.smriti_dir = workspace / 'smriti'
        self.quality_dir = self.smriti_dir / 'quality_metrics'
        self.quality_dir.mkdir(parents=True, exist_ok=True)
        
        # Load konzeptuelle Frameworks (erweitert)
        self.conceptual_frameworks = [
            "first principles", "meta-ebene", "system-denken", "antifragilität",
            "temporal versioning", "anti-pattern", "5-whys", "second-order effects",
            "deliberate disagreement", "uncertainty quantification", "predictive",
            "paradigm", "framework", "modell", "abstraktion", "synthese",
            "emergence", "feedback loops", "leverage points", "bottleneck",
            "invariant", "heuristic", "epistemology", "ontology"
        ]
        
        # Keywords für Paradigmen-Shift (erweitert)
        self.shift_keywords = [
            "ah", "stimmt", "habe ich", "anders gesehen", "warte", 
            "doch nicht", "korrektur", "revidiere", "neu gedacht",
            "verstehe jetzt", "jetzt sehe ich", "das macht sinn",
            "guter punkt", "da hast du recht", "überzeugt"
        ]
        
        # Anti-fragile Resonanz
        self.positive_feedback_patterns = [
            "guter punkt", "korrekt", "besser so", "stimmt", 
            "das ist es", "genau", "präzise", "tiefgreifend",
            "exzellent", "brilliant", "perfekt", "genau richtig"
        ]
    
    def calculate_predictive_surprise(self, user_input: str, viveka_output: str) -> Dict:
        """
        Metrik 1: Predictive Surprise
        Neue Begriffe in Output, die nicht in Input waren
        """
        user_words = set(user_input.lower().split())
        output_words = set(viveka_output.lower().split())
        
        new_concepts = output_words - user_words
        
        # Filtere nach konzeptuellen Begriffen
        conceptual_new = [w for w in new_concepts if len(w) > 4]
        
        total_output = len(output_words) or 1
        surprise_ratio = len(conceptual_new) / total_output
        
        # Bonus für Framework-Nutzung
        framework_bonus = sum(1 for fw in self.conceptual_frameworks if fw in viveka_output.lower()) * 0.05
        surprise_ratio = min(surprise_ratio + framework_bonus, 1.0)
        
        return {
            "score": round(surprise_ratio, 3),
            "new_concepts": list(conceptual_new)[:10],
            "frameworks_used": [fw for fw in self.conceptual_frameworks if fw in viveka_output.lower()],
            "genius_threshold": surprise_ratio > 0.30,
            "explanation": f"{len(conceptual_new)} neue konzeptionelle Begriffe ({surprise_ratio:.1%} des Outputs)"
        }
    
    def calculate_denkraum_expansion(self, viveka_output: str) -> Dict:
        """
        Metrik 2: Denkraum-Erweiterung
        Frameworks/Modelle über die Frage hinaus
        """
        output_lower = viveka_output.lower()
        
        found_frameworks = [
            fw for fw in self.conceptual_frameworks 
            if fw in output_lower
        ]
        
        # Extra-Punkte für Tabellen/Strukturen
        has_structure = bool(re.search(r'\|.*\|', viveka_output))
        has_numbered_list = bool(re.search(r'^\d+\.', viveka_output, re.MULTILINE))
        has_bullets = bool(re.search(r'^[\-\*] ', viveka_output, re.MULTILINE))
        has_framework = len(found_frameworks) >= 1
        has_sections = bool(re.search(r'^#{1,3} ', viveka_output, re.MULTILINE))
        
        score = 0.0
        if has_framework:
            score += min(len(found_frameworks) * 0.15, 0.5)
        if has_structure:
            score += 0.2
        if has_numbered_list:
            score += 0.15
        if has_bullets:
            score += 0.1
        if has_sections:
            score += 0.05
        
        return {
            "score": round(min(score, 1.0), 3),
            "frameworks_used": found_frameworks[:5],
            "has_structure": has_structure,
            "has_numbered_list": has_numbered_list,
            "has_bullets": has_bullets,
            "has_sections": has_sections,
            "genius_threshold": score >= 0.7,
            "explanation": f"Frameworks: {len(found_frameworks)}, Struktur: {has_structure}, Listen: {has_numbered_list}"
        }
    
    def detect_paradigm_shift(self, session_messages: List[Dict]) -> Dict:
        """
        Metrik 4: Paradigmen-Shift-Induktion
        Erkennung wenn User's Sicht sich ändert
        """
        shifts_detected = []
        
        for i, msg in enumerate(session_messages):
            content = msg.get("content", "").lower()
            user_id = msg.get("role", "")
            
            if user_id == "user":
                for keyword in self.shift_keywords:
                    if keyword in content:
                        # Kontext extrahieren
                        context_start = max(0, i - 1)
                        context = session_messages[context_start:i+1]
                        
                        shifts_detected.append({
                            "keyword": keyword,
                            "message_index": i,
                            "context": " → ".join([
                                f"{m.get('role', '?')}: {m.get('content', '')[:50]}..." 
                                for m in context
                            ])
                        })
                        break  # Nur ein Shift pro Nachricht
        
        score = min(len(shifts_detected) * 0.25, 1.0)
        
        return {
            "score": round(score, 3),
            "shifts_detected": shifts_detected,
            "shift_count": len(shifts_detected),
            "genius_threshold": len(shifts_detected) >= 1,
            "explanation": f"{len(shifts_detected)} Paradigmen-Shift-Indikatoren gefunden"
        }
    
    def detect_antifragile_resonance(self, session_messages: List[Dict]) -> Dict:
        """
        Metrik 5: Anti-Fragile Resonanz
        Kritik produktiv nutzen
        """
        positive_responses = 0
        critical_messages = 0
        productive_turns = []
        
        for i, msg in enumerate(session_messages):
            content = msg.get("content", "").lower()
            role = msg.get("role", "")
            
            # Kritik erkennen
            if role == "user" and any(w in content for w in ["falsch", "nein", "aber", "nicht", "problem", "issue", "error"]):
                critical_messages += 1
                
                # Nachfolgende Antwort prüfen
                if i + 1 < len(session_messages):
                    next_msg = session_messages[i + 1]
                    next_content = next_msg.get("content", "").lower()
                    
                    # Produktive Resonanz?
                    if any(pattern in next_content for pattern in self.positive_feedback_patterns):
                        positive_responses += 1
                        productive_turns.append({
                            "criticism_index": i,
                            "response_index": i + 1,
                            "criticism": content[:100],
                            "response": next_msg.get("content", "")[:100]
                        })
        
        # Score: Verhältnis von produktiven Antworten zu Kritik
        if critical_messages > 0:
            score = positive_responses / critical_messages
        else:
            score = 0.5  # Neutral wenn keine Kritik
        
        return {
            "score": round(score, 3),
            "critical_messages": critical_messages,
            "positive_responses": positive_responses,
            "productive_turns": productive_turns,
            "genius_threshold": score >= 0.7,
            "explanation": f"{positive_responses}/{critical_messages} Kritiken produktiv genutzt"
        }
    
    def calculate_session_velocity(self, session_messages: List[Dict]) -> Dict:
        """
        Metrik 3: Session Velocity
        Tempo der Iteration
        """
        if len(session_messages) < 2:
            return {
                "score": 0.5,
                "message_count": len(session_messages),
                "turns": 0,
                "genius_threshold": False,
                "explanation": "Zu wenige Nachrichten für Velocity-Berechnung"
            }
        
        # Zähle User-Assistant Paare
        turns = 0
        last_role = None
        for msg in session_messages:
            role = msg.get("role", "")
            if role != last_role and role in ["user", "assistant"]:
                turns += 1
                last_role = role
        
        turns = turns // 2  # Volle Iterationen
        
        # Score basierend auf Turns
        if turns >= 10:
            score = 1.0
        elif turns >= 5:
            score = 0.8
        elif turns >= 3:
            score = 0.6
        else:
            score = 0.4
        
        return {
            "score": round(score, 3),
            "message_count": len(session_messages),
            "turns": turns,
            "genius_threshold": turns >= 5,
            "explanation": f"{turns} vollständige Iterationen"
        }
    
    def analyze_session(self, session_messages: List[Dict]) -> Dict[str, Any]:
        """Vollständige Session-Analyse"""
        log('info', f"Analyzing session with {len(session_messages)} messages")
        
        if len(session_messages) < 2:
            log('warn', 'Session too short for meaningful analysis')
            return {
                "error": "Session too short",
                "m1": {"score": 0, "explanation": "N/A"},
                "m2": {"score": 0, "explanation": "N/A"},
                "m3": {"score": 0, "explanation": "N/A"},
                "m4": {"score": 0, "explanation": "N/A"},
                "m5": {"score": 0, "explanation": "N/A"},
            }
        
        # Extrahiere User-Input und Assistant-Output
        user_inputs = [m.get("content", "") for m in session_messages if m.get("role") == "user"]
        assistant_outputs = [m.get("content", "") for m in session_messages if m.get("role") == "assistant"]
        
        combined_user_input = " ".join(user_inputs)
        combined_assistant_output = " ".join(assistant_outputs)
        
        # Berechne alle Metriken
        m1 = self.calculate_predictive_surprise(combined_user_input, combined_assistant_output)
        m2 = self.calculate_denkraum_expansion(combined_assistant_output)
        m3 = self.detect_paradigm_shift(session_messages)
        m4 = self.calculate_session_velocity(session_messages)
        m5 = self.detect_antifragile_resonance(session_messages)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "m1": m1,
            "m2": m2,
            "m3": m3,
            "m4": m4,
            "m5": m5,
            "overall_score": round((m1['score'] + m2['score'] + m3['score'] + m4['score'] + m5['score']) / 5, 3),
            "genius_moments": sum([
                1 for m in [m1, m2, m3, m4, m5] if m.get('genius_threshold')
            ])
        }
        
        # Speichere Ergebnis
        self._save_result(result)
        
        return result
    
    def _save_result(self, result: Dict):
        """Speichere Analyse-Ergebnis"""
        try:
            result_file = self.quality_dir / f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(result_file, 'w') as f:
                json.dump(result, f, indent=2)
            
            # Auch zu M1M4 Log hinzufügen
            m1m4_file = self.workspace / 'neuron' / 'm1m4_log.jsonl'
            m1m4_file.parent.mkdir(parents=True, exist_ok=True)
            with open(m1m4_file, 'a') as f:
                f.write(json.dumps(result) + '\n')
            
            log('info', f'Result saved to {result_file}')
        except Exception as e:
            log('error', 'Failed to save result', {'error': str(e)})
    
    def print_report(self, result: Dict):
        """Drucke formatierten Report"""
        print("\n" + "=" * 60)
        print("📊 GENIUS QUALITY REPORT")
        print("=" * 60)
        print(f"Timestamp: {result['timestamp']}")
        print(f"Overall Score: {result['overall_score']:.2f}/1.0")
        print(f"Genius Moments: {result['genius_moments']}/5")
        print()
        print("M1 — Predictive Surprise:")
        print(f"   Score: {result['m1']['score']:.2f} {'🌟' if result['m1']['genius_threshold'] else ''}")
        print(f"   {result['m1']['explanation']}")
        print()
        print("M2 — Denkraum-Erweiterung:")
        print(f"   Score: {result['m2']['score']:.2f} {'🌟' if result['m2']['genius_threshold'] else ''}")
        print(f"   {result['m2']['explanation']}")
        print()
        print("M3 — Paradigmen-Shift:")
        print(f"   Score: {result['m3']['score']:.2f} {'🌟' if result['m3']['genius_threshold'] else ''}")
        print(f"   {result['m3']['explanation']}")
        print()
        print("M4 — Session Velocity:")
        print(f"   Score: {result['m4']['score']:.2f} {'🌟' if result['m4']['genius_threshold'] else ''}")
        print(f"   {result['m4']['explanation']}")
        print()
        print("M5 — Anti-Fragile Resonanz:")
        print(f"   Score: {result['m5']['score']:.2f} {'🌟' if result['m5']['genius_threshold'] else ''}")
        print(f"   {result['m5']['explanation']}")
        print("=" * 60)

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Genius Quality Tracker v2.0")
    parser.add_argument("--session-file", type=str, help="Path to session JSON file")
    parser.add_argument("--test", action="store_true", help="Run with test data")
    parser.add_argument("--continuous", action="store_true", help="Continuous mode (for integration)")
    
    args = parser.parse_args()
    
    tracker = GeniusQualityTracker()
    
    if args.test:
        # Test mit Beispiel-Daten
        test_messages = [
            {"role": "user", "content": "Kannst du das erklären?"},
            {"role": "assistant", "content": "Natürlich. Das ist ein System mit first principles..."},
            {"role": "user", "content": "Ah, jetzt verstehe ich! Das ist eine meta-ebene Betrachtung."},
            {"role": "assistant", "content": "Genau! Du hast den Paradigmen-Shift erkannt."},
            {"role": "user", "content": "Aber warte, ist das nicht zu abstrakt?"},
            {"role": "assistant", "content": "Guter Punkt. Lass mich konkreter werden..."},
        ]
        
        result = tracker.analyze_session(test_messages)
        tracker.print_report(result)
    
    elif args.session_file:
        # Lade echte Session
        try:
            with open(args.session_file) as f:
                session = json.load(f)
            
            messages = session.get('messages', [])
            result = tracker.analyze_session(messages)
            tracker.print_report(result)
        except Exception as e:
            log('error', f'Failed to load session: {e}')
            sys.exit(1)
    
    elif args.continuous:
        log('info', 'Continuous mode started — waiting for input')
        # Für Integration mit OpenClaw
        # Liest von stdin
        import sys
        for line in sys.stdin:
            try:
                data = json.loads(line)
                messages = data.get('messages', [])
                result = tracker.analyze_session(messages)
                print(json.dumps(result))
            except Exception as e:
                log('error', 'Failed to process input', {'error': str(e)})
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
