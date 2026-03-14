# Integration Plan: AGENTS.md + OUROBOROS + REFLECTY

## 🎯 Ziel: Ein System statt drei

### Aktueller Zustand (CHAOS):
```
agents_suggestion_system.py  ← NEU, redundant
context_manager.py           ← NEU, redundant
ouroboros/mutation_engine.mjs ← EXISTIERT
reflecty/reflecty.py         ← EXISTIERT
```

### Ziel-Zustand (CLEAN):
```
ouroboros/mutation_engine.mjs  ← Handhabt ALLE Mutationen (inkl. AGENTS.md)
reflecty/reflecty.py          ← Handhabt Context (P0/P1/P2)
```

---

## 🔧 Konkrete Umsetzung

### Schritt 1: OUROBOROS erweitern

**Datei:** `src/js/ouroboros/mutation_engine.mjs`

**Neu:** Mutation Type D — AGENTS.md Changes

```javascript
// In mutation_engine.mjs
const MUTATION_TYPES = {
  A: 'auto_execute',           // Bestehend
  B: 'approval_queue',         // Bestehend
  C: 'human_decision',         // Bestehend
  D: 'agents_md_change'        // NEU
};

// NEU: AGENTS.md Mutation Handler
async function handleAgentsMDMutation(mutation) {
  const { section, change_type, current, proposed, reason } = mutation.data;
  
  // Type D = Immer Approval Queue (nie auto)
  mutation.type = 'D';
  mutation.requires_approval = true;
  
  // Speichere in Approval Queue
  await addToApprovalQueue({
    ...mutation,
    display_text: `AGENTS.md [${section}]: ${change_type}\n${reason}`,
    preview_diff: generateDiff(current, proposed)
  });
}
```

### Schritt 2: REFLECTY erweitern

**Datei:** `src/python/reflecty/reflecty.py`

**Neu:** Context Management Methoden

```python
class Reflecty:
    def __init__(self):
        # Bestehend: L1, L2, L3
        
        # NEU: Context Management
        self.context_priorities = {
            'P0_ALWAYS': ['SOUL.md', 'USER.md', 'AGENTS.md'],
            'P1_ON_DEMAND': {
                'strategisch': 'core_mission.json',
                'fehler': 'anti_patterns_v3.jsonl',
                'subagent': 'subagent_factory.py'
            },
            'P2_SEARCH': 'MEMORY.md'
        }
    
    def get_context_for_session(self, intent_analysis):
        """
        NEU: Lädt kontext basierend auf Intent
        
        Args:
            intent_analysis: Ergebnis von L1 Observer
            
        Returns:
            Kontext-String (max 150 Zeilen P0)
        """
        # P0 immer laden
        p0 = self._load_p0()
        
        # P1 basierend auf Keywords
        p1 = self._load_p1_on_demand(intent_analysis.get('keywords', []))
        
        # P2 semantisch suchen
        if intent_analysis.get('requires_memory_search'):
            p2 = self._search_p2(intent_analysis['query'])
        
        return self._combine_context(p0, p1, p2)
    
    def _load_p0(self, max_lines=150):
        """Lädt P0 mit Kompression"""
        # Implementation...
        pass
```

### Schritt 3: Integration in AGENTS.md

**Aktuell (veraltet):**
```markdown
## 🧠 SMRITI v3.5 — Automatisch Aktiv
### Session-Start:
exec bash /data/.openclaw/workspace/smriti/smriti-session-hook.sh
```

**Neu (integriert):**
```markdown
## 🧠 SMRITI v3.5 + OUROBOROS + REFLECTY

### Session-Start:
# 1. Reflecty L1-L3 laden (Context + Intelligence)
exec python3 /data/.openclaw/workspace/smriti/src/python/reflecty/reflecty.py --mode=session_start

# 2. OUROBOROS prüft Pending Mutationen
exec node /data/.openclaw/workspace/smriti/src/js/ouroboros/mutation_engine.mjs --check-queue

### AGENTS.md Änderungen:
# Werden durch OUROBOROS Type D Mutationen gehandhabt
# Queue: neuron/ouroboros_approval_queue.json
# Status: python3 /data/.openclaw/workspace/smriti/check_mutations.py
```

---

## 🗑️ Was gelöscht wird

1. **agents_suggestion_system.py** — Redundant zu OUROBOROS
2. **context_manager.py** — Redundant zu REFLECTY
3. **docs/AGENTS_MD_BEST_PRACTICES.md** — Dokumentation bleibt, aber als Referenz

---

## ✅ Vorteile dieser Lösung

| Aspekt | Vorher (3 Systeme) | Nachher (1 System) |
|--------|-------------------|-------------------|
| Komplexität | 🔴 Hoch | 🟢 Niedrig |
| Verständlichkeit | 🔴 Schwer | 🟢 Einfach |
| Wartbarkeit | 🔴 Schwer | 🟢 Einfach |
| Duplikation | 🔴 Viel | 🟢 Keine |
| Integration | 🔴 Schlecht | 🟢 Perfekt |

---

## 🚀 Implementation Steps

1. **Backup** der neuen Dateien (nur für Referenz)
2. **Löschen** von agents_suggestion_system.py + context_manager.py
3. **Erweitern** von mutation_engine.mjs um Type D
4. **Erweitern** von reflecty.py um Context Management
5. **Update** von AGENTS.md mit neuen Einträgen
6. **Test** des integrierten Systems

---

*Ein System. Eine Verantwortung. Keine Duplikation.*
