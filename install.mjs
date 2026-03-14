#!/usr/bin/env node
/**
 * SMRITI v3.5 — ONE-CLICK INSTALLER v2.0
 * 
 * Usage: node install.mjs
 * 
 * Dieses Skript:
 * 1. Prüft OpenClaw-Umgebung
 * 2. Installiert alle Komponenten
 * 3. Startet Memory-Infrastruktur
 * 4. Aktiviert Quality/Pattern/Bridge/OUROBOROS
 * 5. Verifiziert Installation
 * 6. Erstellt OpenClaw-Integration
 */

import { execSync, spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ═══════════════════════════════════════════════════════════════════
// CONFIGURATION
// ═══════════════════════════════════════════════════════════════════

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || '/data/.openclaw/workspace';
const NEURON_DIR = path.join(WORKSPACE, 'neuron');
const AGENTS_DIR = path.join(WORKSPACE, 'agents');
const SCRIPTS_DIR = path.join(WORKSPACE, 'scripts');
const SMRITI_DIR = path.join(WORKSPACE, 'smriti');

const SOURCE_DIR = __dirname;

console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║  SMRITI v3.5 — ONE-CLICK INSTALLER v2.0                    ║');
console.log('║  Cognitive OS for OpenClaw Agents                         ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log();

// ═══════════════════════════════════════════════════════════════════
// STEP 1: Environment Check
// ═══════════════════════════════════════════════════════════════════
console.log('🔍 Step 1: Environment Check');

try {
  const nodeVersion = execSync('node --version', { encoding: 'utf8' }).trim();
  console.log(`   ✅ Node.js: ${nodeVersion}`);
} catch {
  console.error('   ❌ Node.js not found. Please install Node.js 18+');
  process.exit(1);
}

try {
  const pythonVersion = execSync('python3 --version', { encoding: 'utf8' }).trim();
  console.log(`   ✅ Python: ${pythonVersion}`);
} catch {
  console.error('   ❌ Python3 not found. Please install Python 3.10+');
  process.exit(1);
}

// Check OpenClaw Workspace
if (!fs.existsSync(WORKSPACE)) {
  console.error(`   ❌ OpenClaw Workspace not found: ${WORKSPACE}`);
  console.error(`   Set OPENCLAW_WORKSPACE environment variable or create ${WORKSPACE}`);
  process.exit(1);
}
console.log(`   ✅ Workspace: ${WORKSPACE}`);

// Check Docker
try {
  execSync('docker --version', { stdio: 'ignore' });
  console.log('   ✅ Docker available');
} catch {
  console.log('   ⚠️  Docker not found — memory services will need manual setup');
}

// ═══════════════════════════════════════════════════════════════════
// STEP 2: Create Directory Structure
// ═══════════════════════════════════════════════════════════════════
console.log();
console.log('📁 Step 2: Creating Directory Structure');

const dirs = [
  NEURON_DIR,
  path.join(NEURON_DIR, 'memory'),
  path.join(NEURON_DIR, 'archive'),
  AGENTS_DIR,
  path.join(AGENTS_DIR, 'reflecty'),
  SCRIPTS_DIR,
  path.join(SCRIPTS_DIR, 'ouroboros'),
  path.join(SCRIPTS_DIR, 'smriti'),
  SMRITI_DIR,
  path.join(SMRITI_DIR, 'quality_metrics'),
  path.join(WORKSPACE, 'data', 'memory', 'drafts'),
  path.join(WORKSPACE, 'logs'),
];

for (const dir of dirs) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`   📂 Created: ${path.relative(WORKSPACE, dir)}`);
  }
}

// ═══════════════════════════════════════════════════════════════════
// STEP 3: Install Python Components
// ═══════════════════════════════════════════════════════════════════
console.log();
console.log('🐍 Step 3: Installing Python Components');

const pythonComponents = [
  { src: 'src/python/bridge_connector.py', dest: 'neuron/bridge_connector.py' },
  { src: 'src/python/reflecty/reflecty.py', dest: 'agents/reflecty/reflecty.py' },
  { src: 'src/python/smriti/quality_tracker.py', dest: 'smriti/quality_tracker.py' },
];

for (const { src, dest } of pythonComponents) {
  const srcPath = path.join(SOURCE_DIR, src);
  const destPath = path.join(WORKSPACE, dest);
  
  if (fs.existsSync(srcPath)) {
    fs.copyFileSync(srcPath, destPath);
    fs.chmodSync(destPath, 0o755);
    console.log(`   ✅ Installed: ${dest}`);
  } else {
    console.log(`   ❌ Source not found: ${src}`);
    process.exit(1);
  }
}

// ═══════════════════════════════════════════════════════════════════
// STEP 4: Install JavaScript Components
// ═══════════════════════════════════════════════════════════════════
console.log();
console.log('📜 Step 4: Installing JavaScript Components');

const jsComponents = [
  { src: 'src/js/ouroboros/mutation_engine.mjs', dest: 'scripts/ouroboros/mutation_engine.mjs' },
  { src: 'src/js/ouroboros/auto_rollback.mjs', dest: 'scripts/ouroboros/auto_rollback.mjs' },
  { src: 'src/js/ouroboros/morning_init.mjs', dest: 'scripts/ouroboros/morning_init.mjs' },
  { src: 'src/js/ouroboros/evening_feedback.mjs', dest: 'scripts/ouroboros/evening_feedback.mjs' },
  { src: 'src/js/smriti/session_hook.mjs', dest: 'scripts/smriti/session_hook.mjs' },
];

for (const { src, dest } of jsComponents) {
  const srcPath = path.join(SOURCE_DIR, src);
  const destPath = path.join(WORKSPACE, dest);
  
  if (fs.existsSync(srcPath)) {
    fs.copyFileSync(srcPath, destPath);
    fs.chmodSync(destPath, 0o755);
    console.log(`   ✅ Installed: ${dest}`);
  } else {
    console.log(`   ⚠️  Source not found: ${src}`);
  }
}

// ═══════════════════════════════════════════════════════════════════
// STEP 5: Install Configuration Files
// ═══════════════════════════════════════════════════════════════════
console.log();
console.log('⚙️  Step 5: Installing Configuration Files');

const configs = [
  { src: 'src/config/smriti.json', dest: 'neuron/smriti.json' },
  { src: 'src/config/ouroboros.json', dest: 'neuron/ouroboros.json' },
  { src: 'src/config/bridge.json', dest: 'neuron/bridge.json' },
  { src: 'src/config/memory/layer2.json', dest: 'neuron/memory/layer2.json' },
  { src: 'src/config/memory/layer3.json', dest: 'neuron/memory/layer3.json' },
  { src: 'src/config/memory/layer4.json', dest: 'neuron/memory/layer4.json' },
];

for (const { src, dest } of configs) {
  const srcPath = path.join(SOURCE_DIR, src);
  const destPath = path.join(WORKSPACE, dest);
  
  // Only copy if not exists (preserve user changes)
  if (!fs.existsSync(destPath) && fs.existsSync(srcPath)) {
    fs.copyFileSync(srcPath, destPath);
    console.log(`   ✅ Installed: ${dest}`);
  } else if (fs.existsSync(destPath)) {
    console.log(`   ⏭️  Skipped (exists): ${dest}`);
  } else {
    console.log(`   ❌ Source not found: ${src}`);
  }
}

// ═══════════════════════════════════════════════════════════════════
// STEP 6: Create Data Files
// ═══════════════════════════════════════════════════════════════════
console.log();
console.log('💾 Step 6: Creating Data Files');

const dataFiles = [
  'neuron/patterns.jsonl',
  'neuron/anti_patterns.jsonl',
  'neuron/ouroboros_mutations.jsonl',
  'neuron/ouroboros_validations.jsonl',
  'neuron/bridge_events.jsonl',
  'neuron/bridge_health.jsonl',
  'neuron/m1m4_log.jsonl',
  'neuron/meta_learn_log.jsonl',
];

for (const file of dataFiles) {
  const filePath = path.join(WORKSPACE, file);
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, '');
    console.log(`   ✅ Created: ${file}`);
  }
}

// Initialize bridge state
const bridgeStatePath = path.join(NEURON_DIR, '.bridge_state.json');
if (!fs.existsSync(bridgeStatePath) || fs.readFileSync(bridgeStatePath, 'utf8').trim() === '') {
  const initialState = {
    bridge_id: `orb_${Date.now()}`,
    active_mutations: [],
    pending_patterns: [],
    conflicts: [],
    learning_cycles: 0,
    last_sync: new Date().toISOString(),
    version: '3.5',
    status: 'initialized'
  };
  fs.writeFileSync(bridgeStatePath, JSON.stringify(initialState, null, 2));
  console.log('   ✅ Initialized: .bridge_state.json');
}

// Initialize ouroboros state
const ouroborosStatePath = path.join(NEURON_DIR, 'ouroboros_state.json');
if (!fs.existsSync(ouroborosStatePath)) {
  const initialState = {
    version: '3.5',
    initialized: new Date().toISOString(),
    mutations_count: 0,
    last_mutation: null,
    auto_rollback_enabled: true
  };
  fs.writeFileSync(ouroborosStatePath, JSON.stringify(initialState, null, 2));
  console.log('   ✅ Initialized: ouroboros_state.json');
}

// ═══════════════════════════════════════════════════════════════════
// STEP 7: Start Memory Infrastructure
// ═══════════════════════════════════════════════════════════════════
console.log();
console.log('🐳 Step 7: Starting Memory Infrastructure');

const composeFile = path.join(SOURCE_DIR, 'docker-compose.yml');
const destCompose = path.join(WORKSPACE, 'docker-compose-smriti.yml');

if (fs.existsSync(composeFile)) {
  fs.copyFileSync(composeFile, destCompose);
  console.log('   ✅ Docker Compose copied');
  
  try {
    console.log('   🚀 Starting containers...');
    execSync(`docker-compose -f ${destCompose} up -d`, { 
      cwd: WORKSPACE,
      stdio: 'pipe'
    });
    console.log('   ✅ Containers started');
    
    // Wait for services
    console.log('   ⏳ Waiting for services (10s)...');
    await new Promise(r => setTimeout(r, 10000));
  } catch (e) {
    console.log('   ⚠️  Docker start issue (may already be running)');
  }
} else {
  console.log('   ⚠️  docker-compose.yml not found');
}

// ═══════════════════════════════════════════════════════════════════
// STEP 8: Create Environment File
// ═══════════════════════════════════════════════════════════════════
console.log();
console.log('📝 Step 8: Creating Environment Configuration');

const envContent = `# Smriti v3.5 Environment Configuration
# Generated: ${new Date().toISOString()}

# Core Paths
SMRITI_WORKSPACE=${WORKSPACE}
OPENCLAW_WORKSPACE=${WORKSPACE}

# Memory Services
SMRITI_MEM0_URL=http://localhost:8000
SMRITI_QDRANT_URL=http://localhost:6333
SMRITI_NEO4J_URL=http://localhost:7474

# User Configuration
SMRITI_USER_ID=default
SMRITI_LOG_LEVEL=info

# Feature Flags
SMRITI_AUTO_MUTATION=true
SMRITI_QUALITY_TRACKING=true
SMRITI_PATTERN_MINING=true
`;

const envPath = path.join(WORKSPACE, '.smriti_env');
fs.writeFileSync(envPath, envContent);
console.log(`   ✅ Created: .smriti_env`);

// ═══════════════════════════════════════════════════════════════════
// STEP 9: Create OpenClaw Integration
// ═══════════════════════════════════════════════════════════════════
console.log();
console.log('🔌 Step 9: Creating OpenClaw Integration');

// Session Hook for AGENTS.md
const sessionHook = `#!/bin/bash
# SMRITI v3.5 — Session Integration Hook
# Add this to AGENTS.md or run at session start

export SMRITI_ENABLED=true
export SMRITI_VERSION="3.5"

# Load environment
if [ -f "${WORKSPACE}/.smriti_env" ]; then
    source "${WORKSPACE}/.smriti_env"
fi

# Initialize Bridge
echo "🧠 Initializing Smriti v3.5..."

python3 -c "
import sys
import os
sys.path.insert(0, '${WORKSPACE}')
os.chdir('${WORKSPACE}')
from neuron.bridge_connector import bridge_init
print(bridge_init())
" 2>/dev/null || echo "⚠️  Bridge init skipped (normal on first run)"

# Run session hook
node "${WORKSPACE}/scripts/smriti/session_hook.mjs" 2>/dev/null || echo "⚠️  Session hook skipped"

echo "✅ Smriti v3.5 ready"
`;

const hookPath = path.join(WORKSPACE, 'smriti-session-hook.sh');
fs.writeFileSync(hookPath, sessionHook);
fs.chmodSync(hookPath, 0o755);
console.log('   ✅ Created: smriti-session-hook.sh');

// OpenClaw integration instructions
const integrationGuide = `# Smriti v3.5 — OpenClaw Integration

## Quick Start

Add to your AGENTS.md session start:

\`\`\`bash
exec bash smriti-session-hook.sh
\`\`\`

Or manually:

\`\`\`bash
# Initialize
export SMRITI_WORKSPACE=${WORKSPACE}
node scripts/smriti/session_hook.mjs

# Use components
python3 neuron/bridge_connector.py
python3 agents/reflecty/reflecty.py --mode test
python3 smriti/quality_tracker.py --test
node scripts/ouroboros/mutation_engine.mjs --dry-run
\`\`\`

## Environment Variables

- SMRITI_WORKSPACE — Workspace path
- SMRITI_MEM0_URL — mem0 endpoint
- SMRITI_USER_ID — User ID for mem0
- SMRITI_LOG_LEVEL — debug|info|warn|error

## Troubleshooting

1. **mem0 not responding**
   - Check: curl http://localhost:8000/health
   - Fix: docker-compose -f docker-compose-smriti.yml restart

2. **Bridge not initializing**
   - Check: python3 -c "from neuron.bridge_connector import get_bridge; print(get_bridge().get_status())"
   - Fix: Ensure .smriti_env is loaded

3. **Permission errors**
   - Fix: chmod +x scripts/**/*.mjs smriti-session-hook.sh
`;

const guidePath = path.join(WORKSPACE, 'SMRITI_INTEGRATION.md');
fs.writeFileSync(guidePath, integrationGuide);
console.log('   ✅ Created: SMRITI_INTEGRATION.md');

// ═══════════════════════════════════════════════════════════════════
// STEP 10: Verification
// ═══════════════════════════════════════════════════════════════════
console.log();
console.log('✅ Step 10: Verification');

const checks = [
  { name: 'Bridge Connector', path: 'neuron/bridge_connector.py' },
  { name: 'Reflecty Agent', path: 'agents/reflecty/reflecty.py' },
  { name: 'Quality Tracker', path: 'smriti/quality_tracker.py' },
  { name: 'Mutation Engine', path: 'scripts/ouroboros/mutation_engine.mjs' },
  { name: 'Session Hook', path: 'scripts/smriti/session_hook.mjs' },
  { name: 'Main Config', path: 'neuron/smriti.json' },
  { name: 'Bridge State', path: 'neuron/.bridge_state.json' },
  { name: 'Environment File', path: '.smriti_env' },
];

let allOk = true;
for (const check of checks) {
  const checkPath = path.join(WORKSPACE, check.path);
  const exists = fs.existsSync(checkPath);
  console.log(`   ${exists ? '✅' : '❌'} ${check.name}`);
  if (!exists) allOk = false;
}

// Health Check
console.log();
console.log('🏥 Health Check');

try {
  const health = execSync('curl -s http://localhost:8000/health 2>/dev/null', { 
    encoding: 'utf8',
    timeout: 5000 
  });
  console.log(`   ✅ mem0: ${health.trim()}`);
} catch {
  console.log('   ⚠️  mem0: Not responding (will use Layer 2 fallback)');
}

try {
  const qdrantHealth = execSync('curl -s http://localhost:6333/healthz 2>/dev/null', {
    encoding: 'utf8',
    timeout: 5000
  });
  console.log(`   ✅ Qdrant: ${qdrantHealth.trim()}`);
} catch {
  console.log('   ⚠️  Qdrant: Not responding');
}

// Test Python imports
try {
  execSync(`cd ${WORKSPACE} && python3 -c "import sys; sys.path.insert(0, '${WORKSPACE}'); from neuron.bridge_connector import BridgeConnector; print('   ✅ Python imports OK')"`, {
    encoding: 'utf8',
    timeout: 5000
  });
} catch {
  console.log('   ⚠️  Python imports: Check required');
}

// ═══════════════════════════════════════════════════════════════════
// DONE
// ═══════════════════════════════════════════════════════════════════
console.log();
console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║  INSTALLATION COMPLETE                                     ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log();
console.log('📋 Next Steps:');
console.log('   1. Source environment: source .smriti_env');
console.log('   2. Add to AGENTS.md: exec bash smriti-session-hook.sh');
console.log('   3. Read integration guide: cat SMRITI_INTEGRATION.md');
console.log('   4. Run tests: node test.mjs');
console.log();
console.log('🧠 Smriti v3.5 is ready!');
console.log();

if (allOk) {
  console.log('✅ All components installed successfully');
  console.log();
  console.log('Quick test:');
  console.log('   python3 smriti/quality_tracker.py --test');
  process.exit(0);
} else {
  console.log('⚠️  Some components missing — check logs above');
  process.exit(1);
}
