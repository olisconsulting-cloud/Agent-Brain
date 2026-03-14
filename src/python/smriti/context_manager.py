#!/usr/bin/env python3
"""
Context Manager v3.5 — Hierarchische Kontext-Verwaltung

Prinzip: P0 (Immer) + P1 (On-Demand) + P2 (Search)

Verhindert Context-Window-Überlastung.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class ContextPriority:
    """Prioritäts-Level für Kontext"""
    P0_ALWAYS = "p0_always"      # Immer laden (Core)
    P1_ON_DEMAND = "p1_on_demand"  # Bei Trigger laden
    P2_SEARCH = "p2_search"       # Semantisch suchen

class ContextManager:
    """
    Verwaltet hierarchischen Kontext
    
    Ziel: Max 150 Zeilen P0, Rest on-demand
    """
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace or os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace'))
        
        # P0: Immer laden (Core)
        self.p0_files = [
            self.workspace / 'SOUL.md',
            self.workspace / 'USER.md',
            self.workspace / 'AGENTS.md',
        ]
        
        # P1: On-Demand (bei Trigger)
        self.p1_files = {
            'strategisch': self.workspace / 'neuron' / 'core_mission.json',
            'fehler': self.workspace / 'neuron' / 'anti_patterns_v3.jsonl',
            'subagent': self.workspace / 'neuron' / 'subagent_factory.py',
            'heartbeat': self.workspace / 'neuron' / 'HEARTBEAT.md',
        }
        
        # P2: Search (semantisch)
        self.p2_index = self.workspace / 'neuron' / 'context_index.json'
        
        # Aktueller Kontext
        self.loaded_context = {}
        self.context_size = 0  # Zeilen
        self.max_p0_size = 150  # Max P0 Zeilen
    
    def get_core_context(self) -> str:
        """
        Lädt P0-Kontext (immer)
        
        Returns:
            Kombinierter P0-Text
        """
        parts = []
        total_lines = 0
        
        for file in self.p0_files:
            if file.exists():
                try:
                    with open(file) as f:
                        content = f.read()
                        lines = content.count('\n')
                        
                        # Prüfe ob wir über Limit gehen
                        if total_lines + lines > self.max_p0_size:
                            # Kürze
                            allowed = self.max_p0_size - total_lines
                            content = self._compress_content(content, allowed)
                            lines = allowed
                        
                        parts.append(f"\n\n=== {file.name} ===\n\n{content}")
                        total_lines += lines
                        
                except Exception as e:
                    parts.append(f"\n\n=== {file.name} ===\n\n[Error: {e}]")
        
        self.context_size = total_lines
        return '\n'.join(parts)
    
    def load_on_demand(self, trigger: str) -> Optional[str]:
        """
        Lädt P1-Kontext bei Trigger
        
        Args:
            trigger: Schlüsselwort (z.B. "strategisch")
            
        Returns:
            Inhalt oder None
        """
        if trigger in self.p1_files:
            file = self.p1_files[trigger]
            if file.exists():
                try:
                    with open(file) as f:
                        return f.read()
                except Exception:
                    pass
        return None
    
    def search_context(self, query: str, max_results: int = 3) -> List[Dict]:
        """
        Semantische Suche in P2
        
        Args:
            query: Suchbegriff
            max_results: Max Ergebnisse
            
        Returns:
            Liste von Treffern
        """
        # Einfache Keyword-Suche (könnte mit embeddings erweitert werden)
        results = []
        
        # Suche in MEMORY.md
        memory_file = self.workspace / 'MEMORY.md'
        if memory_file.exists():
            try:
                with open(memory_file) as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        # Extrahiere relevanten Abschnitt
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if query.lower() in line.lower():
                                # Kontext um das Keyword
                                start = max(0, i - 2)
                                end = min(len(lines), i + 3)
                                context = '\n'.join(lines[start:end])
                                results.append({
                                    'source': 'MEMORY.md',
                                    'context': context,
                                    'line': i
                                })
                                if len(results) >= max_results:
                                    break
            except Exception:
                pass
        
        return results
    
    def _compress_content(self, content: str, max_lines: int) -> str:
        """Komprimiert Inhalt auf max_lines"""
        lines = content.split('\n')
        
        if len(lines) <= max_lines:
            return content
        
        # Strategie: Header + Essenz + Footer
        header_lines = lines[:20]  # Erste 20 Zeilen
        footer_lines = lines[-10:]  # Letzte 10 Zeilen
        
        # Mitte: Nur wichtige Zeilen (keine Leerzeilen, keine Kommentare)
        middle = [l for l in lines[20:-10] if l.strip() and not l.strip().startswith('#')]
        
        # Berechne wie viel Platz für Mitte bleibt
        middle_budget = max_lines - len(header_lines) - len(footer_lines) - 5  # 5 für "..."
        
        if len(middle) > middle_budget:
            middle = middle[:middle_budget]
            middle.append("\n... [gekürzt] ...\n")
        
        return '\n'.join(header_lines + middle + footer_lines)
    
    def get_context_report(self) -> str:
        """Zeigt aktuellen Kontext-Status"""
        
        lines = [
            "╔════════════════════════════════════════════════════════════╗",
            "║  CONTEXT MANAGER v3.5 — Status                             ║",
            "╚════════════════════════════════════════════════════════════╝",
            "",
            f"P0 (Immer): {len(self.p0_files)} Dateien",
            f"P1 (On-Demand): {len(self.p1_files)} Trigger",
            f"Aktuelle Größe: {self.context_size} Zeilen",
            f"Limit: {self.max_p0_size} Zeilen",
            f"Status: {'✅ OK' if self.context_size <= self.max_p0_size else '⚠️ Überladen'}",
            "",
            "P1 Trigger:"
        ]
        
        for trigger, file in self.p1_files.items():
            exists = "✅" if file.exists() else "❌"
            lines.append(f"  {exists} {trigger} → {file.name}")
        
        lines.append("")
        return '\n'.join(lines)


# Convenience
def get_core_context() -> str:
    """Lädt P0-Kontext"""
    return ContextManager().get_core_context()


def load_for_trigger(trigger: str) -> Optional[str]:
    """Lädt Kontext für Trigger"""
    return ContextManager().load_on_demand(trigger)


def search_memory(query: str) -> List[Dict]:
    """Sucht in Memory"""
    return ContextManager().search_context(query)


if __name__ == "__main__":
    # Test
    cm = ContextManager()
    
    print(cm.get_context_report())
    
    # Test P0
    print("\n" + "="*60)
    print("P0 Kontext (erste 500 Zeichen):")
    print("="*60)
    core = cm.get_core_context()
    print(core[:500] + "...")
    
    # Test Search
    print("\n" + "="*60)
    print("Suche nach 'Smriti':")
    print("="*60)
    results = cm.search_context("Smriti")
    for r in results[:2]:
        print(f"\n{r['source']} (Zeile {r['line']}):")
        print(r['context'][:200])
