# SMRITI v3.5 — PACKAGE OVERVIEW

> The sweet spot: Power of v2.1, simplicity of v3.0

---

## 📦 CONTENTS (17 Files)

### Documentation (4)
- `README.md` — Overview, quick start, examples
- `AGENTS.md` — The five systems (load instructions)
- `HEARTBEAT.md` — Three gates + troubleshooting
- `OVERVIEW.md` — This file

### Configuration (8)
- `neuron/smriti.json` — Main config (references all others)
- `neuron/ouroboros.json` — Self-improvement settings
- `neuron/bridge.json` — System integration
- `neuron/memory/layer2.json` — File system memory
- `neuron/memory/layer3.json` — Semantic memory (mem0)
- `neuron/memory/layer4.json` — Graph memory (Neo4j, recommended)
- `docker-compose.yml` — Infrastructure setup

### Data & State (5) — Auto-created
- `neuron/patterns.jsonl` — Pattern storage
- `neuron/anti_patterns.jsonl` — Error database
- `neuron/.bridge_state.json` — Bridge status
- `neuron/ouroboros_mutations.jsonl` — Mutation log
- `neuron/ouroboros_validations.jsonl` — Validation log
- `neuron/ouroboros_state.json` — OUROBOROS state

**Note:** Only `neuron/smriti.json` needs to be loaded manually. All other configs are referenced automatically. Data files are created on first use.

---

## 🎯 THE FIVE SYSTEMS

See `AGENTS.md` for detailed system documentation.

**Quick Overview:**
1. **Quality Engine** — Think before speaking (triggers, 3 perspectives, uncertainty)
2. **Pattern Engine** — Learn across sessions (L1 observe, L2 blend, L3 predict)
3. **Improvement Engine** — Grow through mistakes (anti-patterns, OUROBOROS)
4. **BRIDGE** — Connect Pattern ↔ Improvement (real-time integration)
5. **Memory Infrastructure** — Technical foundation (L2 files, L3 semantic, L4 graph)

**System Flow:**
```
User Input → Quality (reflect) → Pattern (learn) 
    → BRIDGE (connect) → Improvement (grow)
    → Memory (store) → Validated by Pattern L3
```

---

## 🆚 COMPARISON

| Aspect | v3.0 | v3.5 | v2.1 |
|--------|------|------|------|
| Systems | 3 | 5 | 10 |
| Config Files | 4 | 8 | 16 |
| **Total Files** | **4** | **17** | **30+** |
| OUROBOROS | ❌ | ✅ | ✅ |
| BRIDGE | ❌ | ✅ | ✅ |
| Memory L3 | ❌ | ✅ | ✅ |
| **Memory L4** | ❌ | **✅ Recommended** | ✅ |
| Temporal | ❌ | ❌ | ✅ |
| M1-M4 | ❌ | ❌ | ✅ |
| Setup | 10 min | 15 min | 30 min |
| Cost/mo | ~$12 | ~$17 | ~$24 |

**v3.5 = 80% power, 50% complexity, 100% clarity**

---

## 🚀 QUICK START

```bash
# 1. Copy files
cp -r smriti-v3.5/* /your/agent/workspace/

# 2. Start infrastructure
cd /your/agent/workspace
docker-compose up -d mem0 qdrant postgres

# 3. Verify
curl http://localhost:8000/health

# 4. Done
```

---

## 💡 WHY v3.5?

**Not v3.0 (too simple):**
- No self-improvement
- No pattern validation
- No semantic memory

**Not v2.1 (too complex):**
- 10 systems overwhelming
- Temporal versioning overhead
- M1-M4 tracking burden

**v3.5 (just right):**
- Core intelligence ✅
- Self-improvement ✅
- Semantic memory ✅
- Bridge integration ✅
- Simple enough ✅

---

## 🎯 PERFECT FOR

- Teams sharing the system
- Production deployments
- Users wanting power + simplicity
- Long-term learning projects

---

*Smriti v3.5. The best of both worlds.*
