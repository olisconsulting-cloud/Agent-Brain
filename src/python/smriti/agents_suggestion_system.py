#!/usr/bin/env python3
"""
AGENTS.md Suggestion System v3.5

Prinzip: Agent schlägt vor, Mensch entscheidet.

Safety-First: Nie automatisch ändern.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AgentsSuggestionSystem:
    """
    Vorschläge für AGENTS.md-Änderungen
    
    Workflow:
    1. Agent analysiert und schlägt vor
    2. Vorschlag wird in Queue gespeichert
    3. Mensch approved/rejected
    4. Nur bei Approval: Änderung durchgeführt
    """
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace or os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace'))
        self.suggestion_queue = self.workspace / 'neuron' / 'agents_suggestions.json'
        self.agents_md = self.workspace / 'AGENTS.md'
        self.backup_dir = self.workspace / 'neuron' / 'agents_backups'
        
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Lade Queue
        self.queue = self._load_queue()
    
    def _load_queue(self) -> List[Dict]:
        """Lädt Vorschlags-Queue"""
        try:
            if self.suggestion_queue.exists():
                with open(self.suggestion_queue) as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def _save_queue(self):
        """Speichert Queue"""
        try:
            with open(self.suggestion_queue, 'w') as f:
                json.dump(self.queue, f, indent=2)
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")
    
    def suggest_change(self, section: str, change_type: str, 
                     current_text: str, proposed_text: str, 
                     reason: str) -> str:
        """
        Schlägt eine Änderung vor
        
        Args:
            section: Welcher Abschnitt (z.B. "Tools")
            change_type: "add", "remove", "modify"
            current_text: Aktueller Text
            proposed_text: Vorgeschlagener Text
            reason: Begründung
            
        Returns:
            Suggestion ID
        """
        suggestion_id = f"sugg_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.queue)}"
        
        suggestion = {
            'id': suggestion_id,
            'timestamp': datetime.now().isoformat(),
            'section': section,
            'type': change_type,
            'current': current_text,
            'proposed': proposed_text,
            'reason': reason,
            'status': 'pending',
            'approved_by': None,
            'approved_at': None
        }
        
        self.queue.append(suggestion)
        self._save_queue()
        
        return suggestion_id
    
    def list_pending(self) -> List[Dict]:
        """Zeigt alle pending Vorschläge"""
        return [s for s in self.queue if s['status'] == 'pending']
    
    def approve(self, suggestion_id: str, user: str = 'Oli') -> bool:
        """
        Genehmigt einen Vorschlag
        
        Args:
            suggestion_id: ID des Vorschlags
            user: Wer genehmigt (default: Oli)
            
        Returns:
            True wenn erfolgreich
        """
        # Finde Vorschlag
        suggestion = None
        for s in self.queue:
            if s['id'] == suggestion_id:
                suggestion = s
                break
        
        if not suggestion:
            print(f"Vorschlag {suggestion_id} nicht gefunden")
            return False
        
        if suggestion['status'] != 'pending':
            print(f"Vorschlag bereits {suggestion['status']}")
            return False
        
        # Backup erstellen
        backup_file = self.backup_dir / f"AGENTS.md.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
        try:
            import shutil
            shutil.copy(self.agents_md, backup_file)
        except Exception as e:
            print(f"Backup fehlgeschlagen: {e}")
            return False
        
        # Änderung durchführen
        try:
            with open(self.agents_md, 'r') as f:
                content = f.read()
            
            # Ersetze Text
            if suggestion['current'] in content:
                new_content = content.replace(suggestion['current'], suggestion['proposed'], 1)
                
                with open(self.agents_md, 'w') as f:
                    f.write(new_content)
                
                # Markiere als approved
                suggestion['status'] = 'approved'
                suggestion['approved_by'] = user
                suggestion['approved_at'] = datetime.now().isoformat()
                suggestion['backup_file'] = str(backup_file)
                
                self._save_queue()
                
                print(f"✅ Vorschlag {suggestion_id} genehmigt und angewendet")
                print(f"   Backup: {backup_file}")
                return True
            else:
                print(f"❌ Konnte Text nicht finden: {suggestion['current'][:50]}...")
                return False
                
        except Exception as e:
            print(f"❌ Fehler beim Anwenden: {e}")
            return False
    
    def reject(self, suggestion_id: str, reason: str = None) -> bool:
        """Lehnt einen Vorschlag ab"""
        for s in self.queue:
            if s['id'] == suggestion_id:
                s['status'] = 'rejected'
                s['rejected_at'] = datetime.now().isoformat()
                s['reject_reason'] = reason
                self._save_queue()
                print(f"❌ Vorschlag {suggestion_id} abgelehnt")
                return True
        return False
    
    def get_report(self) -> str:
        """Erzeugt Report"""
        pending = len([s for s in self.queue if s['status'] == 'pending'])
        approved = len([s for s in self.queue if s['status'] == 'approved'])
        rejected = len([s for s in self.queue if s['status'] == 'rejected'])
        
        lines = [
            "╔════════════════════════════════════════════════════════════╗",
            "║  AGENTS.md SUGGESTION SYSTEM v3.5                          ║",
            "╚════════════════════════════════════════════════════════════╝",
            "",
            f"Pending:  {pending}",
            f"Approved: {approved}",
            f"Rejected: {rejected}",
            "",
            "Aktuelle Vorschläge:"
        ]
        
        for s in self.queue[-5:]:  # Letzte 5
            status_icon = {'pending': '⏳', 'approved': '✅', 'rejected': '❌'}.get(s['status'], '⚪')
            lines.append(f"  {status_icon} {s['id'][:20]}... [{s['section']}] {s['type']}")
        
        lines.append("")
        return '\n'.join(lines)


# Convenience function
def suggest_agents_change(section: str, change_type: str, 
                         current: str, proposed: str, reason: str) -> str:
    """
    Einfache Funktion um Änderung vorzuschlagen
    
    Usage:
        suggest_agents_change(
            section="Tools",
            change_type="add",
            current="",
            proposed="- [ ] new-tool",
            reason="Neues Tool verfügbar"
        )
    """
    system = AgentsSuggestionSystem()
    return system.suggest_change(section, change_type, current, proposed, reason)


if __name__ == "__main__":
    # Test
    system = AgentsSuggestionSystem()
    
    print(system.get_report())
    
    # Test-Vorschlag
    print("\nTest-Vorschlag wird erstellt...")
    sugg_id = system.suggest_change(
        section="Tools",
        change_type="add",
        current="",
        proposed="- [ ] new-tool",
        reason="Test-Vorschlag"
    )
    print(f"Vorschlag ID: {sugg_id}")
    
    print("\n" + system.get_report())
