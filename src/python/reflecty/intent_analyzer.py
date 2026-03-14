#!/usr/bin/env python3
"""
Intent Analyzer v3.5 — Autonome Context-Ladung

Analysiert User-Input und lädt passenden Kontext automatisch.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class IntentAnalyzer:
    """
    Analysiert Intent und lädt passenden Kontext
    
    Keine Keywords nötig — alles automatisch!
    """
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace or os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace'))
        
        # Intent Patterns
        self.intent_patterns = {
            'strategic': {
                'keywords': ['strategisch', 'mission', 'hebel', 'ziel', 'plan', 'vision'],
                'p1_files': ['core_mission.json'],
                'weight': 1.0
            },
            'error_learning': {
                'keywords': ['fehler', 'bug', 'problem', 'issue', 'fix', 'reparieren'],
                'p1_files': ['anti_patterns_v3.jsonl'],
                'weight': 1.0
            },
            'subagent': {
                'keywords': ['recherchiere', 'baue', 'implementiere', 'coder', 'analysiere'],
                'p1_files': ['subagent_factory.py'],
                'weight': 1.0
            },
            'heartbeat': {
                'keywords': ['heartbeat', 'status', 'gesundheit', 'metriken', 'm1', 'm2'],
                'p1_files': ['HEARTBEAT.md'],
                'weight': 0.8
            },
            'bridge': {
                'keywords': ['bridge', 'verbindung', 'system', 'integration'],
                'p1_files': ['.bridge_state.json'],
                'weight': 0.8
            },
            'memory': {
                'keywords': ['erinnere', 'memory', 'früher', 'damals', 'history'],
                'p2_search': True,
                'weight': 0.9
            }
        }
    
    def analyze(self, user_input: str) -> Dict:
        """
        Analysiert Input und gibt Intent zurück
        
        Args:
            user_input: Der Text des Users
            
        Returns:
            Dict mit Intent, Confidence, zu ladenden Dateien
        """
        user_lower = user_input.lower()
        scores = {}
        
        # Berechne Score für jeden Intent
        for intent_name, pattern in self.intent_patterns.items():
            score = 0
            matches = []
            
            for keyword in pattern['keywords']:
                if keyword in user_lower:
                    score += 1
                    matches.append(keyword)
            
            # Normalisiere
            if pattern['keywords']:
                score = score / len(pattern['keywords']) * pattern['weight']
            
            scores[intent_name] = {
                'score': score,
                'matches': matches,
                'p1_files': pattern.get('p1_files', []),
                'p2_search': pattern.get('p2_search', False)
            }
        
        # Finde besten Intent
        best_intent = max(scores.items(), key=lambda x: x[1]['score'])
        
        return {
            'primary_intent': best_intent[0],
            'confidence': best_intent[1]['score'],
            'matches': best_intent[1]['matches'],
            'p1_files': best_intent[1]['p1_files'],
            'p2_search': best_intent[1]['p2_search'],
            'all_scores': {k: v['score'] for k, v in scores.items()}
        }
    
    def load_context(self, intent_result: Dict) -> str:
        """
        Lädt Kontext basierend auf Intent
        
        Args:
            intent_result: Ergebnis von analyze()
            
        Returns:
            Kombinierter Kontext-String
        """
        parts = []
        
        # P0 immer laden
        p0 = self._load_p0()
        parts.append(f"=== P0 Core ===\n{p0}")
        
        # P1 bei Bedarf
        if intent_result['confidence'] > 0.3:
            for filename in intent_result['p1_files']:
                content = self._load_p1_file(filename)
                if content:
                    parts.append(f"\n=== P1 {filename} ===\n{content}")
        
        # P2 bei Bedarf
        if intent_result.get('p2_search') and intent_result['confidence'] > 0.5:
            search_results = self._search_p2(intent_result['matches'])
            if search_results:
                parts.append(f"\n=== P2 Memory Search ===\n{search_results}")
        
        return '\n'.join(parts)
    
    def _load_p0(self, max_lines: int = 150) -> str:
        """Lädt P0 Core"""
        p0_files = [
            self.workspace / 'SOUL.md',
            self.workspace / 'USER.md',
            self.workspace / 'AGENTS.md'
        ]
        
        parts = []
        total_lines = 0
        
        for file in p0_files:
            if file.exists():
                try:
                    with open(file) as f:
                        content = f.read()
                        lines = content.count('\n')
                        
                        if total_lines + lines > max_lines:
                            # Kürze
                            all_lines = content.split('\n')
                            allowed = max_lines - total_lines
                            content = '\n'.join(all_lines[:allowed])
                            content += "\n... [gekürzt] ..."
                        
                        parts.append(content)
                        total_lines += lines
                except Exception:
                    pass
        
        return '\n\n'.join(parts)
    
    def _load_p1_file(self, filename: str) -> Optional[str]:
        """Lädt P1 Datei"""
        file = self.workspace / 'neuron' / filename
        if file.exists():
            try:
                with open(file) as f:
                    return f.read()
            except Exception:
                pass
        return None
    
    def _search_p2(self, keywords: List[str]) -> str:
        """Sucht in MEMORY.md"""
        memory_file = self.workspace / 'MEMORY.md'
        if not memory_file.exists():
            return ""
        
        try:
            with open(memory_file) as f:
                content = f.read()
            
            results = []
            for keyword in keywords:
                if keyword in content.lower():
                    # Finde Kontext
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if keyword in line.lower():
                            start = max(0, i - 2)
                            end = min(len(lines), i + 3)
                            context = '\n'.join(lines[start:end])
                            results.append(context)
                            break
            
            return '\n\n'.join(results[:3])  # Max 3 Ergebnisse
        except Exception:
            return ""
    
    def get_report(self) -> str:
        """Zeigt Analyzer-Status"""
        lines = [
            "╔════════════════════════════════════════════════════════════╗",
            "║  INTENT ANALYZER v3.5                                      ║",
            "╚════════════════════════════════════════════════════════════╝",
            "",
            f"Erkannte Intents: {len(self.intent_patterns)}",
            ""
        ]
        
        for intent, config in self.intent_patterns.items():
            lines.append(f"  • {intent}")
            lines.append(f"    Keywords: {', '.join(config['keywords'][:3])}...")
            if config.get('p1_files'):
                lines.append(f"    P1: {', '.join(config['p1_files'])}")
        
        lines.append("")
        return '\n'.join(lines)


# Convenience
def analyze_intent(user_input: str, workspace: str = None) -> Dict:
    """Einfache Funktion für Intent-Analyse"""
    analyzer = IntentAnalyzer(workspace)
    return analyzer.analyze(user_input)


def get_context_for_input(user_input: str, workspace: str = None) -> str:
    """Lädt Kontext für User-Input"""
    analyzer = IntentAnalyzer(workspace)
    intent = analyzer.analyze(user_input)
    return analyzer.load_context(intent)


if __name__ == "__main__":
    # Test
    analyzer = IntentAnalyzer()
    
    print(analyzer.get_report())
    
    # Test Inputs
    test_inputs = [
        "Wie ist unsere strategische Mission?",
        "Ich habe einen Fehler gefunden",
        "Recherchiere nach Best Practices",
        "Wie geht es dem Heartbeat?",
        "Erinnere dich an Smriti"
    ]
    
    for user_input in test_inputs:
        print(f"\n{'='*60}")
        print(f"Input: {user_input}")
        print('='*60)
        
        intent = analyzer.analyze(user_input)
        print(f"Intent: {intent['primary_intent']} (confidence: {intent['confidence']:.2f})")
        print(f"Matches: {intent['matches']}")
        print(f"P1 Files: {intent['p1_files']}")
        print(f"P2 Search: {intent['p2_search']}")
