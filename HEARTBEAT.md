# HEARTBEAT.md — Smriti v3.5

> Three gates. Essential maintenance only.

---

## 🚪 THREE GATES

### Gate 1: Session Start

```
□ Load 5 system files
□ Check memory health (Layer 2-3)
□ Initialize BRIDGE listeners
□ Set session baseline
```

### Gate 2: Mid-Session (Optional)

```
□ Check drift (if intensive mode)
□ Resource status
□ Only if 30min+ active
```

### Gate 3: Session End

```
□ Log session to draft file
□ Persist patterns to storage
□ Update OUROBOROS cycles
□ Sync BRIDGE state
```

---

## 📅 CYCLES

### Weekly
- Condense day logs → MEMORY.md
- Review anti-patterns
- OUROBOROS auto-tune
- BRIDGE sync check

### Monthly
- Clean MEMORY.md (>2 weeks)
- Archive old logs
- Review pattern accuracy
- Optional: Neo4j optimization

---

## 🛡️ TROUBLESHOOTING

### Problem: mem0 not responding
**Symptom:** `curl http://localhost:8000/health` fails  
**Cause:** Container not started or crashed  
**Fix:**
```bash
docker-compose ps                    # Check status
docker-compose restart mem0          # Restart
docker-compose logs mem0 | tail -20  # Check logs
```

### Problem: Qdrant connection refused
**Symptom:** Port 6333 not accessible  
**Cause:** Qdrant still starting or port conflict  
**Fix:**
```bash
docker-compose restart qdrant
# Wait 10 seconds, then test:
curl http://localhost:6333/healthz
```

### Problem: Neo4j browser not loading
**Symptom:** http://localhost:7474 shows error  
**Cause:** Neo4j still initializing (takes 30-60s)  
**Fix:**
```bash
docker-compose logs neo4j | grep "Started"
# Wait for "Started" message, then refresh browser
```

### Problem: BRIDGE events not routing
**Symptom:** Patterns detected but OUROBOROS not triggered  
**Cause:** Confidence threshold not met or Bridge down  
**Fix:**
```bash
# Check .bridge_state.json
cat neuron/.bridge_state.json | jq .status
# Should show: "operational"

# If "degraded", restart:
touch neuron/.bridge_state.json  # Reset trigger
```

### Problem: Pattern storage growing too large
**Symptom:** patterns.jsonl > 100MB  
**Cause:** No archival configured  
**Fix:**
```bash
# Archive old patterns
mv neuron/patterns.jsonl neuron/patterns-$(date +%Y%m).jsonl
touch neuron/patterns.jsonl
# Update smriti.json to add archival frequency
```

---

*Essential maintenance. No overhead.*
