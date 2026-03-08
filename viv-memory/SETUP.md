# VIV-MIND Setup Guide

## Prerequisites

- Docker & Docker Compose installed on your VPS
- ~4GB RAM available
- Ports 7474, 7687, 8001, 3000, 6333 free

## Quick Start

### 1. Navigate to the project

```bash
cd /data/.openclaw/workspace/viv-memory
```

### 2. Set environment variables (optional but recommended)

```bash
export MEM0_API_KEY=m0-mTG6s7FdqBkztj9vwZArzjVQeCyZqH4yel4wJdd4
```

The `.env` file already contains this - Docker Compose will load it automatically.

### 3. Start all services

```bash
docker-compose up -d
```

This will start:
- **Neo4j** (Knowledge Graph) - http://localhost:7474
- **Mem0** (Semantic Memory) - http://localhost:8001
- **Qdrant** (Vector Store) - http://localhost:6333
- **Postgres** (Relational DB)
- **Langfuse** (Observability) - http://localhost:3000

### 4. Wait for services to be healthy (~2-3 minutes)

```bash
docker-compose ps
```

All services should show "healthy" status.

### 5. Access the UIs

- **Neo4j Browser**: http://localhost:7474 (login: neo4j/viv-memory-2025)
- **Langfuse**: http://localhost:3000
- **Mem0 API**: http://localhost:8001

## Testing the Connection

### Test Mem0 API

```bash
curl -X POST http://localhost:8001/v1/memories/ \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Oli prefers direct communication"}],
    "user_id": "oli",
    "agent_id": "viveka"
  }'
```

### Test Neo4j

```bash
# Via Neo4j Browser at http://localhost:7474
# Run: MATCH (n) RETURN count(n)
```

## Integration with OpenClaw

### Option A: HTTP API (Recommended)

VIV-Brain exposes an HTTP API that OpenClaw can call. Add to OpenClaw config:

```yaml
# In ~/.openclaw/config.yaml or similar
plugins:
  viv_memory:
    enabled: true
    mem0_url: http://localhost:8001
    neo4j_uri: bolt://localhost:7687
    neo4j_user: neo4j
    neo4j_password: viv-memory-2025
```

### Option B: Direct File Integration

VIV-Brain can read OpenClaw's memory files directly (mounted in docker-compose).

## Troubleshooting

### Port already in use

```bash
# Check what's using port 7474
sudo lsof -i :7474

# Stop existing Neo4j if running
sudo systemctl stop neo4j

# Or change ports in docker-compose.yml
```

### Neo4j won't start

```bash
# Check logs
docker-compose logs neo4j

# Common fix: remove old data
sudo rm -rf volumes/neo4j-data/*
docker-compose up -d neo4j
```

### Mem0 connection refused

```bash
# Check if service is running
docker-compose ps mem0

# Check logs
docker-compose logs mem0

# API key might be needed - check .env file is loaded
```

## Stopping Everything

```bash
docker-compose down
```

To remove all data (WARNING: deletes all memories):

```bash
docker-compose down -v
```

## Next Steps

Once running, VIV will:
1. ✅ Store every conversation in Mem0
2. ✅ Build a knowledge graph in Neo4j
3. ✅ Track patterns and beliefs
4. ✅ Generate morning briefings

The system is designed to be resilient - if services are down, VIV falls back to file-based memory.
