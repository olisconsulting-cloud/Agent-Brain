# VIV-MEMORY Architektur
## Die Ultimative Memory-Lösung

**Status:** ✅ Installiert & Laufend  
**Stand:** 2026-03-08  
**Ort:** `/opt/viv-memory/` auf dem VPS

---

## Überblick

VIV-MEMORY ist ein **hybrides, mehrschichtiges Memory-System** — nicht nur Dateien, sondern eine komplette Datenbank-Infrastruktur für maximale Intelligenz.

**Philosophie:** Nicht "eine Lösung", sondern **mehrere spezialisierte Systeme**, die zusammenarbeiten.

---

## Die 5 Memory-Schichten

### Schicht 1: Relational (PostgreSQL)
**Was:** Strukturierte Daten, Metadaten, Zeitstempel  
**Port:** Intern im Docker-Netzwerk  
**Nutzen:** Schnelle Queries, ACID-Transaktionen

### Schicht 2: Vector (Qdrant)
**Was:** Embeddings, semantische Ähnlichkeit  
**Port:** 6333 (extern erreichbar)  
**Container:** `viv-qdrant`  
**Nutzen:** "Was hat Oli zu Ähnlichem gesagt?"

### Schicht 3: Graph (Neo4j)
**Was:** Beziehungen, Entitäten, Wissensnetzwerk  
**Port:** 7474 (Browser), 7687 (Bolt)  
**Container:** `viv-neo4j`  
**Login:** neo4j/viv-memory-2025  
**Nutzen:** "Oli → priorisiert → Qualität", kausale Zusammenhänge

### Schicht 4: Semantic (Mem0)
**Was:** Natürlichsprachliche Erinnerungen, Kontext  
**Port:** 8001 (API)  
**Nutzen:** "Erinnere dich an..."

### Schicht 5: Observability (Langfuse)
**Was:** Tracking, Metriken, Tracing  
**Port:** 3000  
**Nutzen:** "Wo lag ich falsch?"

---

## Das viv_brain Package

**Ort:** `/opt/viv-memory/viv-brain/viv_brain/`

### Module

| Modul | Zweck | Integration ins Neuron |
|-------|-------|------------------------|
| `identity_manager.py` | Identitäts-Persistenz | Wer bin ich über Sessions hinweg? |
| `knowledge_graph.py` | Neo4j-Interface | Wissensnetzwerk aufbauen |
| `memory_client.py` | Mem0-Client | Semantic Memory API |
| `night_mode.py` | Nachtverarbeitung | Background-Learning |
| `orchestrator.py` | Gesamtorchestrierung | Alles zusammenführen |

### Dependencies
- neo4j>=5.15.0
- requests>=2.31.0
- pydantic>=2.0.0
- python-dotenv>=1.0.0

---

## API-Endpunkte

### Mem0 API (localhost:8001)

**Erinnerung speichern:**
```bash
curl -X POST http://localhost:8001/v1/memories/ \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Oli prefers direct communication"}],
    "user_id": "oli",
    "agent_id": "viveka"
  }'
```

**Erinnerung suchen:**
```bash
curl -X POST http://localhost:8001/v1/memories/search/ \
  -H "Authorization: Token $MEM0_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "memory system Neo4j",
    "user_id": "oli"
  }'
```

### Neo4j (localhost:7687)

**Bolt-Verbindung:**
```
bolt://localhost:7687
User: neo4j
Password: viv-memory-2025
```

**Browser-UI:** http://localhost:7474

---

## Integration mit Viveka-Neuron

### Aktueller Status

| System | Status | Neuron-Integration |
|--------|--------|---------------------|
| File-basiertes Memory | ✅ | Basis |
| VIV-Memory Stack | ✅ Läuft | Noch nicht im Neuron aktiv |

### Geplante Integration

**Schritt 1: Hybrid-Modus**
- Dateien als Cache/Fallback
- VIV-Memory als primäre Quelle

**Schritt 2: Auto-Sync**
- Jede Interaktion → Mem0 + Neo4j
- Nachts: Background-Processing (night_mode.py)

**Schritt 3: Semantic Retrieval**
- Statt "grep in MEMORY.md" → "Query in VIV-Memory"
- Antworten basieren auf Knowledge Graph

---

## Environment

**API-Key Mem0:** `m0-mTG6s7FdqBkztj9vwZArzjVQeCyZqH4yel4wJdd4`

**Neo4j:**
- URI: bolt://localhost:7687
- User: neo4j
- Pass: viv-memory-2025

---

## Wichtig für Neustart

**Bei jedem `/new`:**
1. VIV-Memory Container prüfen (`docker ps`)
2. Falls down: `docker-compose up -d` in `/opt/viv-memory/`
3. Mem0 API testen
4. Neo4j Verbindung prüfen

**Fallback:** Wenn VIV-Memory nicht erreichbar → File-basiertes System

---

## Nächste Schritte

1. ✅ Integration in `viveka_neuron_v2.json`
2. ⏳ Python-Client für Mem0 in Sub-Agents
3. ⏳ Knowledge Graph befüllen mit historischen Daten
4. ⏳ Night Mode aktivieren für Background-Learning

---

*"Das ist nicht mehr 'ein bisschen Memory'. Das ist ein kognitives Ökosystem."*

— Dokumentation erstellt von Viveka, 2026-03-08
