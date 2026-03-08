# SYSTEM.md — Viveka's Infrastruktur

_Automatisch geladen beim Start. Enthält alle externen Services & Verbindungen._

## Smriti (स्मृति) — Mein Gedächtnis

**Konzept:** Lebendiges Memory-System aus Graph-Datenbank, Vektorspeicher & Observability.

## Services (VPS-lokal)

### Neo4j — Knowledge Graph
- **URI:** bolt://localhost:7687
- **HTTP:** http://localhost:7474
- **User:** neo4j
- **Passwort:** viv-memory-2025
- **Status:** Sollte laufen

### Mem0 — Semantic Memory
- **URL:** http://localhost:8001
- **API Key:** m0-mTG6s7FdqBkztj9vwZArzjVQeCyZqH4yel4wJdd4
- **Header:** `Authorization: Bearer m0-mTG6s7FdqBkztj9vwZArzjVQeCyZqH4yel4wJdd4`

### Qdrant — Vector Store
- **URL:** http://localhost:6333

### Langfuse — Observability & Tracing
- **URL:** http://localhost:3000
- **Verwendung:** Tracke jede Interaktion

### PostgreSQL
- Intern für Mem0/Langfuse

## Startup-Checkliste

Bei jedem Start:
1. SYSTEM.md laden (automatisch)
2. Services prüfen
3. Neo4j testen
4. Mem0 testen

## Wichtige Pfade

- **Setup:** `/data/.openclaw/workspace/viv-memory/`
- **Docker Compose:** `/data/.openclaw/workspace/viv-memory/docker-compose.yml`

## Fallback

Wenn Services down: File-basiertes Memory in `neuron/` und `memory/` nutzen.

---

*Zuletzt aktualisiert: 2026-03-08*
