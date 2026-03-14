# Basic Usage Example

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/smriti-v3.5.git
cd smriti-v3.5

# Install (one command)
node install.mjs

# Source environment
source .smriti_env
```

## Verify Installation

```bash
# Run test suite
node test.mjs

# Expected output:
# ✅ All tests passed
```

## Initialize Session

```bash
# Manual initialization
node scripts/smriti/session_hook.mjs

# Or via OpenClaw integration
# Add to AGENTS.md:
# exec bash smriti-session-hook.sh
```

## Use Components

### Quality Tracker

```bash
# Test mode
python3 smriti/quality_tracker.py --test

# Analyze a session file
python3 smriti/quality_tracker.py --session-file path/to/session.json
```

### Reflecty (Pattern Mining)

```bash
# Test mode
python3 agents/reflecty/reflecty.py --mode test

# Daily synthesis
python3 agents/reflecty/reflecty.py --mode daily_synthesis
```

### OUROBOROS (Self-Improvement)

```bash
# Dry run (preview mutations)
node scripts/ouroboros/mutation_engine.mjs --dry-run

# Actual execution
node scripts/ouroboros/mutation_engine.mjs

# Force execution (skip approval)
node scripts/ouroboros/mutation_engine.mjs --force
```

### BRIDGE

```bash
# Check status
python3 -c "
from neuron.bridge_connector import bridge_status
print(bridge_status())
"
```

## Next Steps

- See [quality-metrics.md](./quality-metrics.md) for M1-M5 details
- See [pattern-mining.md](./pattern-mining.md) for Reflecty usage
- See [self-improvement.md](./self-improvement.md) for OUROBOROS
