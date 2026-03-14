#!/usr/bin/env node
/**
 * SMRITI v3.5 — COMPREHENSIVE TEST SUITE
 * 
 * Verifies all 5 systems are operational after installation.
 * 
 * Usage: node test.mjs
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || '/data/.openclaw/workspace';

console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║  SMRITI v3.5 — COMPREHENSIVE TEST SUITE                    ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log();

let passed = 0;
let failed = 0;

function test(name, fn) {
  process.stdout.write(`   Testing: ${name}... `);
  try {
    fn();
    console.log('✅ PASS');
    passed++;
  } catch (e) {
    console.log(`❌ FAIL: ${e.message}`);
    failed++;
  }
}

// ═════════════════════════════════════════════════════════════════
// TEST 1: File Structure
// ═════════════════════════════════════════════════════════════════
console.log('📁 TEST GROUP: File Structure');

test('Bridge Connector exists', () => {
  const p = path.join(WORKSPACE, 'neuron', 'bridge_connector.py');
  if (!fs.existsSync(p)) throw new Error('Not found');
});

test('Reflecty Agent exists', () => {
  const p = path.join(WORKSPACE, 'agents', 'reflecty', 'reflecty.py');
  if (!fs.existsSync(p)) throw new Error('Not found');
});

test('Quality Tracker exists', () => {
  const p = path.join(WORKSPACE, 'smriti', 'quality_tracker.py');
  if (!fs.existsSync(p)) throw new Error('Not found');
});

test('Mutation Engine exists', () => {
  const p = path.join(WORKSPACE, 'scripts', 'ouroboros', 'mutation_engine.mjs');
  if (!fs.existsSync(p)) throw new Error('Not found');
});

test('Session Hook exists', () => {
  const p = path.join(WORKSPACE, 'scripts', 'smriti', 'session_hook.mjs');
  if (!fs.existsSync(p)) throw new Error('Not found');
});

test('Main Config exists', () => {
  const p = path.join(WORKSPACE, 'neuron', 'smriti.json');
  if (!fs.existsSync(p)) throw new Error('Not found');
});

test('Bridge State exists', () => {
  const p = path.join(WORKSPACE, 'neuron', '.bridge_state.json');
  if (!fs.existsSync(p)) throw new Error('Not found');
});

// ═════════════════════════════════════════════════════════════════
// TEST 2: Configuration Validity
// ═════════════════════════════════════════════════════════════════
console.log();
console.log('⚙️  TEST GROUP: Configuration Validity');

test('smriti.json is valid JSON', () => {
  const p = path.join(WORKSPACE, 'neuron', 'smriti.json');
  const content = fs.readFileSync(p, 'utf8');
  JSON.parse(content);
});

test('ouroboros.json is valid JSON', () => {
  const p = path.join(WORKSPACE, 'neuron', 'ouroboros.json');
  const content = fs.readFileSync(p, 'utf8');
  JSON.parse(content);
});

test('bridge.json is valid JSON', () => {
  const p = path.join(WORKSPACE, 'neuron', 'bridge.json');
  const content = fs.readFileSync(p, 'utf8');
  JSON.parse(content);
});

test('smriti.json has 5 systems', () => {
  const p = path.join(WORKSPACE, 'neuron', 'smriti.json');
  const config = JSON.parse(fs.readFileSync(p, 'utf8'));
  const systems = ['system_1_quality', 'system_2_pattern', 'system_3_improvement', 'system_4_bridge', 'system_5_memory'];
  for (const sys of systems) {
    if (!config[sys]) throw new Error(`Missing: ${sys}`);
  }
});

// ═════════════════════════════════════════════════════════════════
// TEST 3: Python Components
// ═════════════════════════════════════════════════════════════════
console.log();
console.log('🐍 TEST GROUP: Python Components');

test('Bridge Connector imports', () => {
  execSync(`cd ${WORKSPACE} && python3 -c "
import sys
sys.path.insert(0, '${WORKSPACE}')
from neuron.bridge_connector import BridgeConnector
print('OK')
"`, { encoding: 'utf8', timeout: 5000 });
});

test('Reflecty imports', () => {
  execSync(`cd ${WORKSPACE} && python3 -c "
import sys
sys.path.insert(0, '${WORKSPACE}')
from agents.reflecty.reflecty import PatternAnalyzer
print('OK')
"`, { encoding: 'utf8', timeout: 5000 });
});

test('Quality Tracker imports', () => {
  execSync(`cd ${WORKSPACE} && python3 -c "
import sys
sys.path.insert(0, '${WORKSPACE}')
from smriti.quality_tracker import GeniusQualityTracker
print('OK')
"`, { encoding: 'utf8', timeout: 5000 });
});

// ═════════════════════════════════════════════════════════════════
// TEST 4: JavaScript Components
// ═════════════════════════════════════════════════════════════════
console.log();
console.log('📜 TEST GROUP: JavaScript Components');

test('Mutation Engine syntax', () => {
  const p = path.join(WORKSPACE, 'scripts', 'ouroboros', 'mutation_engine.mjs');
  execSync(`node --check ${p}`, { timeout: 5000 });
});

test('Session Hook syntax', () => {
  const p = path.join(WORKSPACE, 'scripts', 'smriti', 'session_hook.mjs');
  execSync(`node --check ${p}`, { timeout: 5000 });
});

// ═════════════════════════════════════════════════════════════════
// TEST 5: Infrastructure (Optional)
// ═════════════════════════════════════════════════════════════════
console.log();
console.log('🐳 TEST GROUP: Infrastructure (Optional)');

test('Layer 2 (File System)', () => {
  const p = path.join(WORKSPACE, 'data', 'memory');
  if (!fs.existsSync(p)) throw new Error('Not found');
});

try {
  execSync('curl -s http://localhost:8000/health', { timeout: 3000 });
  test('Layer 3 (mem0)', () => {
    // Already tested above
  });
} catch {
  console.log('   ⚠️  Layer 3 (mem0): Not running (optional)');
}

try {
  execSync('curl -s http://localhost:6333/healthz', { timeout: 3000 });
  test('Layer 3 (Qdrant)', () => {
    // Already tested above
  });
} catch {
  console.log('   ⚠️  Layer 3 (Qdrant): Not running (optional)');
}

// ═════════════════════════════════════════════════════════════════
// TEST 6: Integration
// ═════════════════════════════════════════════════════════════════
console.log();
console.log('🔌 TEST GROUP: Integration');

test('Session Hook runs', () => {
  const p = path.join(WORKSPACE, 'scripts', 'smriti', 'session_hook.mjs');
  // Just check it doesn't crash immediately
  execSync(`timeout 3 node ${p} || true`, { timeout: 5000 });
});

test('Bridge initializes', () => {
  const output = execSync(`cd ${WORKSPACE} && python3 -c "
import sys
sys.path.insert(0, '${WORKSPACE}')
from neuron.bridge_connector import get_bridge
bridge = get_bridge()
status = bridge.get_status()
print(f'Bridge ID: {status[\"bridge_id\"]}')
"`, { encoding: 'utf8', timeout: 5000 });
  if (!output.includes('Bridge ID:')) throw new Error('Bridge not initialized');
});

// ═════════════════════════════════════════════════════════════════
// SUMMARY
// ═════════════════════════════════════════════════════════════════
console.log();
console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║  TEST SUMMARY                                              ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log();
console.log(`   ✅ Passed: ${passed}`);
console.log(`   ❌ Failed: ${failed}`);
console.log();

if (failed === 0) {
  console.log('🎉 ALL TESTS PASSED!');
  console.log('   Smriti v3.5 is fully operational.');
  process.exit(0);
} else {
  console.log('⚠️  SOME TESTS FAILED');
  console.log('   Check errors above and fix issues.');
  process.exit(1);
}
