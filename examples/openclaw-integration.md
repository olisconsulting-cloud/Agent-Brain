# OpenClaw Integration Guide

## Quick Integration (Recommended)

Add this single line to your `AGENTS.md`:

```markdown
## 🧠 Smriti v3.5 Integration

**Auto-initialize on session start:**
```
exec bash smriti-session-hook.sh
```
```

That's it! Smriti will automatically:
- Load environment variables
- Initialize all 5 systems
- Start monitoring
- Log to appropriate files

## Manual Integration

If you prefer manual control:

### Step 1: Environment Setup

```bash
# In your shell profile or session start
export OPENCLAW_WORKSPACE=/path/to/workspace
export SMRITI_USER_ID=your_name
export SMRITI_LOG_LEVEL=info
```

### Step 2: Initialize Components

```bash
# Initialize BRIDGE
python3 -c "
import sys
sys.path.insert(0, '.')
from neuron.bridge_connector import bridge_init
print(bridge_init())
"

# Run session hook
node scripts/smriti/session_hook.mjs
```

### Step 3: Use in Conversations

Smriti now automatically:
- Scans for quality triggers
- Mines patterns
- Tracks metrics
- Suggests improvements

## Verification

Check that Smriti is running:

```bash
# Check BRIDGE status
python3 -c "
from neuron.bridge_connector import bridge_status
print(bridge_status())
"

# Check logs
tail -f logs/smriti.log

# Check M1-M4 metrics
tail -f neuron/m1m4_log.jsonl
```

## Troubleshooting

### "smriti-session-hook.sh not found"

```bash
# Ensure you're in the workspace directory
cd $OPENCLAW_WORKSPACE

# Or use full path
exec bash $OPENCLAW_WORKSPACE/smriti-session-hook.sh
```

### "mem0 not responding"

```bash
# Start memory services
docker-compose -f docker-compose-smriti.yml up -d

# Or use fallback (Layer 2)
# Smriti automatically falls back to file system
```

### "Permission denied"

```bash
# Fix permissions
chmod +x smriti-session-hook.sh
chmod +x scripts/**/*.mjs
```

## Advanced: Custom Integration

### Custom Quality Triggers

Edit `neuron/smriti.json`:

```json
{
  "system_1_quality": {
    "triggers": {
      "my_custom_trigger": {
        "level": "high",
        "keywords": ["custom", "specific"],
        "action": "custom reflection"
      }
    }
  }
}
```

### Custom Pattern Detection

Extend `agents/reflecty/reflecty.py`:

```python
def _detect_my_patterns(self, messages):
    # Your custom pattern detection
    pass
```

### Custom Mutations

Extend `scripts/ouroboros/mutation_engine.mjs`:

```javascript
function myCustomMutation(signal) {
  // Your mutation logic
}
```

## Full Example AGENTS.md

```markdown
# My OpenClaw Agent

## Identity
- Name: MyAgent
- Version: 1.0

## 🧠 Smriti v3.5 Integration

**Initialize on session start:**
```
exec bash smriti-session-hook.sh
```

**Check status:**
```
exec python3 -c "from neuron.bridge_connector import bridge_status; print(bridge_status())"
```

## Tools
- web_search
- file_read
- file_write

## Memory
- Use memory_search for context
- Store insights via Reflecty

## Quality
- Always reflect on strategic topics
- Use 3 perspectives for decisions
- Log anti-patterns immediately
```

## Support

- [README.md](../README.md)
- [FINAL_COURT_REVIEW.md](../FINAL_COURT_REVIEW.md)
- GitHub Issues
