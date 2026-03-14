# SMRITI v3.5 — Production Ready Cognitive OS

> **One command. Full intelligence. Zero configuration.**

**Version:** 3.5 Production Ready  
**Status:** ✅ Fully Executable & Production Ready  
**Install Time:** 2 minutes  
**Systems:** 5 (Quality, Pattern, Improvement, Bridge, Memory)

---

## 🚀 Quick Start (2 Minutes)

```bash
# 1. Download Smriti v3.5
cd /your/openclaw/workspace
git clone https://github.com/olisconsulting-cloud/Agent-Brain.git smriti

# 2. Install (ONE COMMAND)
cd smriti
node install.mjs

# 3. Auto-Setup (Fügt sich in AGENTS.md ein)
bash setup-auto.sh

# 4. Done! Smriti ist jetzt automatisch aktiv.
```

**That's it.** Nach Restart: Alle 5 Systeme automatisch + Deliberate Disagreement bei "wichtig".

---

## 📦 What's Included

### Executable Components (Actually Running!)

| Component | File | What It Does |
|-----------|------|--------------|
| **BRIDGE** | `neuron/bridge_connector.py` | Real-time event routing with file locking |
| **Reflecty** | `agents/reflecty/reflecty.py` | Pattern mining with mem0 + fallback |
| **Quality Tracker** | `smriti/quality_tracker.py` | 5 Meta-metrics (M1-M5) with logging |
| **Mutation Engine** | `scripts/ouroboros/mutation_engine.mjs` | **Actually changes configs!** |
| **Auto-Rollback** | `scripts/ouroboros/auto_rollback.mjs` | Recovery on failed mutations |
| **Session Hook** | `scripts/smriti/session_hook.mjs` | Auto-initialization |
| **Installer** | `install.mjs` | One-click setup |
| **Test Suite** | `test.mjs` | Comprehensive verification |

### Key Features

✅ **Environment-based configuration** — No hardcoded paths  
✅ **Automatic fallback** — Works without mem0 (Layer 2)  
✅ **Real mutations** — OUROBOROS actually changes files  
✅ **Error handling** — No silent failures  
✅ **OpenClaw integration** — Session hooks ready  
✅ **Production logging** — Structured logs to `logs/`  

---

## 🎯 The 5 Systems — Actually Running

### 1. Quality Engine (Always On)

**Before every response:**
```python
from smriti.quality_tracker import GeniusQualityTracker

tracker = GeniusQualityTracker()
metrics = tracker.analyze_session(messages)
# Returns: M1-M5 scores with explanations
```

**Features:**
- ✅ 5 Meta-Metrics (Predictive Surprise, Denkraum, Velocity, Paradigm, Resonanz)
- ✅ Automatic logging to `neuron/m1m4_log.jsonl`
- ✅ Structured logging with levels
- ✅ File fallback when mem0 unavailable

### 2. Pattern Engine (Background)

**Continuously running:**
```bash
# Auto-runs via session hook
python3 agents/reflecty/reflecty.py --mode analyze
```

**Features:**
- ✅ L1-L3 Pattern detection
- ✅ mem0 integration with file fallback
- ✅ Environment-based configuration
- ✅ Error handling with graceful degradation

### 3. Improvement Engine (Automatic)

**Self-improvement that actually works:**
```bash
# Detects signals and CHANGES CONFIGS
node scripts/ouroboros/mutation_engine.mjs

# Dry-run to preview
node scripts/ouroboros/mutation_engine.mjs --dry-run
```

**Features:**
- ✅ **Actually modifies configuration files**
- ✅ Automatic backups before changes
- ✅ Approval system for Type C mutations
- ✅ Rollback capability

### 4. BRIDGE (Real-time)

**Event routing with robustness:**
```python
from neuron.bridge_connector import get_bridge

bridge = get_bridge()
bridge.receive_from_reflecty(event)
bridge.receive_from_ouroboros(command)
```

**Features:**
- ✅ File locking (race-condition safe)
- ✅ Schema validation
- ✅ Conflict detection
- ✅ Health monitoring
- ✅ Automatic cleanup

### 5. Memory Infrastructure (Active)

**4 Layers with fallback:**
- Layer 1: Context window (automatic)
- Layer 2: File system (always works)
- Layer 3: Semantic (mem0 + Qdrant, with fallback)
- Layer 4: Graph (Neo4j, optional)

---

## 🔧 Configuration

### Environment Variables

Create `.smriti_env` or set in your shell:

```bash
# Core
export SMRITI_WORKSPACE=/data/.openclaw/workspace
export SMRITI_USER_ID=your_name

# Services
export SMRITI_MEM0_URL=http://localhost:8000
export SMRITI_QDRANT_URL=http://localhost:6333

# Logging
export SMRITI_LOG_LEVEL=info  # debug|info|warn|error
```

### Feature Flags

```bash
export SMRITI_AUTO_MUTATION=true      # Enable auto-mutations
export SMRITI_QUALITY_TRACKING=true   # Enable M1-M5 tracking
export SMRITI_PATTERN_MINING=true      # Enable Reflecty
```

---

## 🚀 Usage

### Automatic (Recommended)

Add to `AGENTS.md`:
```markdown
## Session Start

```
exec bash smriti-session-hook.sh
```
```

### Manual

```bash
# Initialize
source .smriti_env

# Run components
python3 smriti/quality_tracker.py --test
python3 agents/reflecty/reflecty.py --mode test
node scripts/ouroboros/mutation_engine.mjs --dry-run

# Check bridge status
python3 -c "from neuron.bridge_connector import bridge_status; print(bridge_status())"
```

---

## 🧪 Testing

```bash
# Run full test suite
node test.mjs

# Test individual components
python3 smriti/quality_tracker.py --test
python3 agents/reflecty/reflecty.py --mode test
node scripts/ouroboros/mutation_engine.mjs --dry-run
```

---

## 📊 Monitoring

### Logs

```bash
# Quality tracker logs
tail -f logs/quality_tracker.log

# OUROBOROS mutations
tail -f neuron/ouroboros_mutations.jsonl

# Bridge events
tail -f neuron/bridge_events.jsonl

# M1-M4 scores
tail -f neuron/m1m4_log.jsonl
```

### Health Checks

```bash
# mem0
curl http://localhost:8000/health

# Qdrant
curl http://localhost:6333/healthz

# Bridge status
python3 -c "from neuron.bridge_connector import bridge_status; print(bridge_status())"
```

---

## 🛠️ Troubleshooting

### mem0 not responding

```bash
# Restart containers
docker-compose -f docker-compose-smriti.yml restart

# System automatically falls back to Layer 2 (file system)
```

### Permission denied

```bash
# Fix permissions
chmod +x scripts/**/*.mjs
chmod +x smriti-session-hook.sh
```

### Import errors

```bash
# Ensure workspace is in Python path
export PYTHONPATH="${WORKSPACE}:${PYTHONPATH}"
```

---

## 📁 File Structure

```
workspace/
├── neuron/
│   ├── bridge_connector.py      # ✅ Executable BRIDGE
│   ├── smriti.json              # Main config
│   ├── ouroboros.json           # Self-improvement config
│   ├── bridge.json              # Integration config
│   ├── .bridge_state.json       # Runtime state
│   ├── patterns.jsonl           # Pattern storage
│   ├── anti_patterns.jsonl      # Error database
│   ├── ouroboros_mutations.jsonl
│   ├── m1m4_log.jsonl            # Quality metrics
│   └── memory/
│       ├── layer2.json
│       ├── layer3.json
│       └── layer4.json
│
├── agents/
│   └── reflecty/
│       └── reflecty.py          # ✅ Executable pattern mining
│
├── smriti/
│   └── quality_tracker.py       # ✅ Executable quality metrics
│
├── scripts/
│   ├── ouroboros/
│   │   ├── mutation_engine.mjs  # ✅ Executable mutations
│   │   ├── auto_rollback.mjs
│   │   ├── morning_init.mjs
│   │   └── evening_feedback.mjs
│   └── smriti/
│       └── session_hook.mjs     # ✅ Auto-initialization
│
├── logs/                         # Production logs
├── data/memory/drafts/            # Layer 2 storage
├── docker-compose-smriti.yml     # Infrastructure
├── .smriti_env                   # Environment config
├── smriti-session-hook.sh        # OpenClaw integration
└── SMRITI_INTEGRATION.md         # Integration guide
```

---

## 🎓 Architecture

```
User Input
    ↓
┌─────────────────────────────────────────┐
│  Quality Engine (M1-M5)                 │
│  - Predictive Surprise                  │
│  - Denkraum-Expansion                   │
│  - Session Velocity                     │
│  - Paradigmen-Shift                     │
│  - Anti-Fragile Resonanz                │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Pattern Engine (Reflecty)              │
│  - L1: Pattern Detection                │
│  - L2: Cross-Domain Analogies         │
│  - L3: 7-Day Predictions                │
└─────────────────────────────────────────┘
    ↓ (confidence >= 0.9)
┌─────────────────────────────────────────┐
│  BRIDGE                                 │
│  - Event Routing                        │
│  - Conflict Detection                   │
│  - File Locking                         │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Improvement Engine (OUROBOROS)         │
│  - Signal Detection                     │
│  - Config Mutation (ACTUAL CHANGES)   │
│  - Auto-Rollback                        │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│  Memory (L2 + L3 + L4)                  │
│  - File System (always works)           │
│  - Semantic (mem0 with fallback)        │
│  - Graph (optional)                     │
└─────────────────────────────────────────┘
```

---

## ✅ Production Checklist

- [ ] Run `node install.mjs`
- [ ] Source `.smriti_env`
- [ ] Run `node test.mjs` — all tests pass
- [ ] Add `exec bash smriti-session-hook.sh` to AGENTS.md
- [ ] Verify: `python3 smriti/quality_tracker.py --test`
- [ ] Verify: `python3 agents/reflecty/reflecty.py --mode test`
- [ ] Verify: `node scripts/ouroboros/mutation_engine.mjs --dry-run`
- [ ] Check logs: `ls logs/`
- [ ] Done! 🎉

---

## 🎯 Comparison

| Feature | v3.0 | **v3.5** | v2.1 |
|---------|------|----------|------|
| **Executable Code** | ❌ Configs only | ✅ **Full implementation** | ✅ Full |
| **Auto-Install** | ❌ Manual | ✅ **One command** | ❌ Complex |
| **Real Mutations** | ❌ | ✅ **Actually changes files** | ✅ |
| **Error Handling** | ❌ Silent fails | ✅ **Graceful degradation** | ✅ |
| **Environment Config** | ❌ Hardcoded | ✅ **Environment variables** | ⚠️ Partial |
| **Fallback Systems** | ❌ | ✅ **Layer 2 always works** | ⚠️ Partial |
| **OpenClaw Hooks** | ❌ | ✅ **Ready to use** | ⚠️ Manual |
| **Production Logging** | ❌ | ✅ **Structured logs** | ✅ |
| **Test Suite** | ❌ | ✅ **Comprehensive** | ⚠️ Basic |
| **Setup Time** | — | **2 min** | 30 min |
| **Complexity** | Low | **Medium** | High |

**v3.5 = v2.1 power with v3.0 simplicity + production robustness**

---

## 💬 Support

- **Issues:** GitHub Issues
- **Logs:** Check `logs/` directory
- **Health:** Run `node test.mjs`
- **Integration:** See `SMRITI_INTEGRATION.md`

---

*Smriti v3.5. Intelligence that actually works.* 🧠
