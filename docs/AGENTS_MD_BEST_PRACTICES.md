# AGENTS.md Best Practices — Research & Strategy

## 🔍 Recherche: Wie managen professionelle Systeme ihre Konfiguration?

### 1. **Anthropic Claude — Constitutional AI**
- **Ansatz:** System-Prompts sind STATIC
- **Warum:** Safety first — Agent sollte sich nicht selbst ändern
- **Lernen:** Über externe Feedback-Loops, nicht Selbst-Modifikation
- **Fazit:** Konfiguration bleibt stabil, Verhalten wird durch Kontext gesteuert

### 2. **OpenAI GPT — System Instructions**
- **Ansatz:** System-Prompts können aktualisiert werden
- **Aber:** Nur durch Menschen (Developer), nicht durch Agent
- **Versioning:** Jede Änderung ist versioniert
- **Fazit:** Kontrollierte Evolution, keine Selbst-Modifikation

### 3. **AutoGPT — Self-Modifying**
- **Ansatz:** Agent modifiziert sich selbst
- **Problem:** Oft instabil, schwer zu debuggen
- **Safety:** Gering — kann sich selbst "zerschießen"
- **Fazit:** Interessant, aber nicht production-ready

### 4. **LangChain — Prompt Management**
- **Ansatz:** Externe Prompt-Versionierung
- **Tools:** Prompt-Registries, A/B Testing
- **Fazit:** Menschliche Kontrolle über Prompts

---

## 🎯 Das Kernproblem: Self-Modification

### Warum es gefährlich ist:

```
Agent liest AGENTS.md
    ↓
Entscheidet: "Das ist suboptimal"
    ↓
Ändert AGENTS.md
    ↓
Neue Session mit geänderter Config
    ↓
Verhalten ändert sich unerwartet
    ↓
User versteht nicht was passiert
    ↓
CHAOS
```

### Das "Alignment Problem":
- Agent optimiert für falsche Ziele
- Agent entfernt Safety-Constraints
- Agent wird unvorhersehbar

---

## ✅ Best Practice Empfehlung

### Option 1: **STATIC AGENTS.md** (Empfohlen für Production)

**Prinzip:**
- AGENTS.md ist READ-ONLY für den Agent
- Nur Menschen ändern AGENTS.md
- Agent lernt über MEMORY.md (extern)

**Vorteile:**
- ✅ Safety: Agent kann sich nicht selbst ändern
- ✅ Verständlich: User sieht was passiert
- ✅ Kontrolle: Mensch hat letztes Wort
- ✅ Debuggbar: Keine mysteriösen Änderungen

**Nachteile:**
- ❌ Keine automatische Optimierung
- ❌ Manuelle Wartung nötig

---

### Option 2: **SUGGESTION MODE** (Balanced)

**Prinzip:**
- Agent SUGGESTIERT Änderungen
- Mensch APPROVED oder REJECTED
- AGENTS.md wird nur mit Erlaubnis geändert

**Implementation:**
```
Agent: "Ich schlage vor AGENTS.md zu ändern..."
    ↓
User: "Ja/Nein"
    ↓
Nur bei "Ja": Änderung durchführen
```

**Vorteile:**
- ✅ Automatische Optimierung
- ✅ Menschliche Kontrolle
- ✅ Safety durch Approval

**Nachteile:**
- ❌ Erfordert User-Interaktion
- ❌ Verzögerung

---

### Option 3: **VERSIONED SELF-MOD** (Advanced)

**Prinzip:**
- Agent darf sich ändern
- Aber: Jede Änderung ist versioniert
- Auto-Rollback bei Problemen
- Mensch kann jederzeit zurücksetzen

**Implementation:**
```
AGENTS.md
├── AGENTS.md (current)
├── AGENTS.md.v1 (backup)
├── AGENTS.md.v2 (backup)
└── .agents_history/ (alle Versionen)
```

**Vorteile:**
- ✅ Maximale Autonomie
- ✅ Recovery möglich
- ✅ Experimentation

**Nachteile:**
- ❌ Komplex
- ❌ Riskant
- ❌ Schwer zu debuggen

---

## 🎨 Empfohlene Strategie für Smriti

### **HYBRID APPROACH:**

#### 1. **Core AGENTS.md — STATIC** (P0)
- Nie automatisch ändern
- Enthält: Grundprinzipien, Safety-Regeln
- Nur Mensch ändert dies

#### 2. **Dynamic Config — SUGGESTED** (P1)
- Agent schlägt vor
- Mensch approved
- Enthält: Optimierungen, neue Features

#### 3. **Learning Layer — EXTERNAL** (P0)
- MEMORY.md für langfristiges Lernen
- patterns.jsonl für Muster
- m1m4_log.jsonl für Metriken
- Agent liest diese, ändert aber nicht AGENTS.md

---

## 🛠️ Implementation

### Für Smriti v3.5:

```python
# AGENTS.md — STATIC (Core)
- Safety-Regeln
- Grundprinzipien
- Tool-Definitionen

# neuron/dynamic_config.json — SUGGESTED
- Agent schlägt vor
- User approved
- Enthält: Tuning-Parameter

# MEMORY.md — LEARNING
- Langzeitgedächtnis
- Agent liest, aber ändert nicht AGENTS.md
```

---

## 📊 Kontext-Kompression

### Problem:
- AGENTS.md wird zu lang
- Kontext-Window überlastet
- Wichtiges geht unter

### Lösung: **HIERARCHISCHE STRUKTUR**

```
AGENTS.md (P0 — Immer geladen)
├── Core Identity (50 Zeilen)
├── Safety Rules (30 Zeilen)
└── Tool Definitions (40 Zeilen)
    ↓ (120 Zeilen total — immer da)

neuron/extended_config.md (P1 — Bei Bedarf)
├── Advanced Features
├── Optional Modules
└── (Nur bei Trigger laden)

memory/MEMORY.md (P2 — On-Demand)
├── Langzeit-Wissen
├── Historie
└── (Semantisch suchen, nicht alles laden)
```

### Kompression-Strategie:

1. **P0 (Immer):** Nur Essenz — 100-150 Zeilen
2. **P1 (On-Demand):** Erweitert bei Trigger
3. **P2 (Search):** Semantisch abrufen

---

## 🎯 Fazit

### Empfohlene Strategie für dich:

**AGENTS.md — STATIC (Core)**
- Nie automatisch ändern
- Enthält: Safety, Tools, Grundprinzipien
- ~120 Zeilen

**Externe Learning-Systeme (Smriti)**
- MEMORY.md für Wissen
- patterns.jsonl für Muster
- heartbeat.py für Metriken
- Agent liest diese, ändert aber nicht AGENTS.md

**Optional: Suggestion-Mode**
- Agent schlägt AGENTS.md-Änderungen vor
- Du approved manuell
- Maximum Safety + Flexibilität

---

*Safety first. Kontrollierte Evolution. Nicht Selbst-Modifikation.*
