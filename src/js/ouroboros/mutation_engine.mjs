#!/usr/bin/env node
/**
 * OUROBOROS Mutation Engine v2.0 — EXECUTABLE
 * 
 * Erkennt Signale und führt tatsächliche Mutationen durch.
 * 
 * Usage:
 *   node mutation_engine.mjs                    # Auto-Modus
 *   node mutation_engine.mjs --dry-run          # Simulieren
 *   node mutation_engine.mjs --force            # Ohne Approval
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

// ═══════════════════════════════════════════════════════════════════
// CONFIGURATION (Environment-based, not hardcoded)
// ═══════════════════════════════════════════════════════════════════

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || process.env.HOME + '/.openclaw/workspace';
const NEURON_DIR = path.join(WORKSPACE, 'neuron');
const LOG_DIR = path.join(WORKSPACE, 'logs');

const PATHS = {
  m1m4: process.env.SMRITI_M1M4_LOG || path.join(NEURON_DIR, 'm1m4_log.jsonl'),
  metaLearn: process.env.SMRITI_META_LOG || path.join(NEURON_DIR, 'meta_learn_log.jsonl'),
  approvalQueue: process.env.SMRITI_APPROVAL_QUEUE || path.join(NEURON_DIR, 'ouroboros_approval_queue.json'),
  mutations: path.join(NEURON_DIR, 'ouroboros_mutations.jsonl'),
  smritiConfig: path.join(NEURON_DIR, 'smriti.json'),
  qualityTriggers: path.join(NEURON_DIR, 'quality_triggers.json'),
  bridgeConfig: path.join(NEURON_DIR, 'bridge.json'),
  ouroborosConfig: path.join(NEURON_DIR, 'ouroboros.json'),
};

const DRY_RUN = process.argv.includes('--dry-run');
const FORCE = process.argv.includes('--force');

// ═══════════════════════════════════════════════════════════════════
// LOGGER
// ═══════════════════════════════════════════════════════════════════

function log(level, message, data = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    level,
    message,
    ...data
  };
  
  console.log(`[${level}] ${message}`);
  
  // Persist to log
  try {
    if (!fs.existsSync(LOG_DIR)) {
      fs.mkdirSync(LOG_DIR, { recursive: true });
    }
    const logFile = path.join(LOG_DIR, 'ouroboros.log');
    fs.appendFileSync(logFile, JSON.stringify(entry) + '\n');
  } catch (e) {
    // Silent fail for logging
  }
}

// ═══════════════════════════════════════════════════════════════════
// SIGNAL DETECTION
// ═══════════════════════════════════════════════════════════════════

function checkSignalStrength() {
  log('INFO', 'Checking signal strength...');
  
  // Check M1M4 log
  if (!fs.existsSync(PATHS.m1m4)) {
    log('WARN', 'M1M4 log not found, creating...');
    fs.writeFileSync(PATHS.m1m4, '');
    return { signal: 0, type: null, reason: 'no_data' };
  }
  
  const content = fs.readFileSync(PATHS.m1m4, 'utf8').trim();
  if (!content) {
    log('INFO', 'M1M4 log empty, no signals yet');
    return { signal: 0, type: null, reason: 'empty_log' };
  }
  
  const lines = content.split('\n').filter(l => l.trim());
  if (lines.length < 3) {
    log('INFO', `Only ${lines.length} entries, need 3 for pattern detection`);
    return { signal: 0, type: null, reason: 'insufficient_data' };
  }
  
  // Parse last 3 entries
  const entries = [];
  for (const line of lines.slice(-3)) {
    try {
      entries.push(JSON.parse(line));
    } catch (e) {
      log('ERROR', 'Failed to parse M1M4 entry', { line: line.substring(0, 100) });
    }
  }
  
  if (entries.length < 3) {
    return { signal: 0, type: null, reason: 'parse_errors' };
  }
  
  // Signal Type A: M1 consistently low (predictive accuracy issue)
  const avgM1 = entries.reduce((a, e) => a + (e.m1?.score || 3), 0) / entries.length;
  const allM1Low = entries.every(e => (e.m1?.score || 3) < 3.5);
  
  if (allM1Low && avgM1 < 3.0) {
    return {
      signal: 0.92,
      type: 'A',
      pattern: 'M1 consistently low — predictive accuracy needs tuning',
      suggested: 'Lower confidence thresholds for quality triggers',
      target: 'quality_triggers.json',
      change: 'threshold_adjustment',
      currentValue: 0.8,
      newValue: 0.75,
      auto: true,
      rollback_possible: true
    };
  }
  
  // Signal Type B: M3 consistently high (system stable)
  const avgM3 = entries.reduce((a, e) => a + (e.m3?.score || 3), 0) / entries.length;
  const allM3High = entries.every(e => (e.m3?.score || 3) > 4.5);
  
  if (allM3High && avgM3 > 4.7) {
    return {
      signal: 0.95,
      type: 'B',
      pattern: 'M3 consistently high — system stable for structural change',
      suggested: 'Increase reflection depth for high-confidence patterns',
      target: 'smriti.json',
      change: 'reflection_depth_increase',
      path: 'system_1_quality.deliberate_disagreement.activation',
      currentValue: 0.8,
      newValue: 0.75,
      auto: true,
      rollback_possible: true
    };
  }
  
  // Signal Type C: Bridge conflicts increasing
  const bridgeState = loadBridgeState();
  if (bridgeState.conflicts && bridgeState.conflicts.length > 5) {
    return {
      signal: 0.88,
      type: 'C',
      pattern: 'High conflict rate — manual resolution needed',
      suggested: 'Add conflict auto-resolution rules',
      target: 'bridge.json',
      change: 'add_auto_resolution',
      auto: false, // Requires approval
      rollback_possible: true
    };
  }
  
  return { signal: 0, type: null, reason: 'no_significant_pattern' };
}

function loadBridgeState() {
  try {
    const statePath = path.join(NEURON_DIR, '.bridge_state.json');
    if (fs.existsSync(statePath)) {
      return JSON.parse(fs.readFileSync(statePath, 'utf8'));
    }
  } catch (e) {
    log('WARN', 'Failed to load bridge state', { error: e.message });
  }
  return {};
}

// ═══════════════════════════════════════════════════════════════════
// MUTATION EXECUTION
// ═══════════════════════════════════════════════════════════════════

function executeMutation(mutation) {
  log('INFO', `Executing mutation: ${mutation.id}`, { type: mutation.type });
  
  if (DRY_RUN) {
    log('INFO', 'DRY RUN — No actual changes made');
    return { success: true, dryRun: true };
  }
  
  try {
    switch (mutation.target) {
      case 'quality_triggers.json':
        return mutateQualityTriggers(mutation);
      case 'smriti.json':
        return mutateSmritiConfig(mutation);
      case 'bridge.json':
        return mutateBridgeConfig(mutation);
      default:
        throw new Error(`Unknown target: ${mutation.target}`);
    }
  } catch (error) {
    log('ERROR', 'Mutation failed', { error: error.message });
    return { success: false, error: error.message };
  }
}

function mutateQualityTriggers(mutation) {
  const configPath = PATHS.qualityTriggers;
  
  // Load or create
  let config = {};
  if (fs.existsSync(configPath)) {
    config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  }
  
  // Apply mutation
  if (mutation.change === 'threshold_adjustment') {
    config.global_threshold = mutation.newValue;
    config.previous_threshold = mutation.currentValue;
    config.last_mutation = new Date().toISOString();
  }
  
  // Backup old config
  const backupPath = `${configPath}.backup.${Date.now()}`;
  if (fs.existsSync(configPath)) {
    fs.copyFileSync(configPath, backupPath);
  }
  
  // Write new config
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  
  log('SUCCESS', `Quality triggers updated: ${mutation.currentValue} → ${mutation.newValue}`);
  log('INFO', `Backup created: ${backupPath}`);
  
  return { success: true, backup: backupPath };
}

function mutateSmritiConfig(mutation) {
  const configPath = PATHS.smritiConfig;
  
  if (!fs.existsSync(configPath)) {
    throw new Error('smriti.json not found');
  }
  
  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  
  // Navigate path and update
  const pathParts = mutation.path.split('.');
  let current = config;
  for (let i = 0; i < pathParts.length - 1; i++) {
    current = current[pathParts[i]];
    if (!current) throw new Error(`Path not found: ${mutation.path}`);
  }
  
  const lastKey = pathParts[pathParts.length - 1];
  const oldValue = current[lastKey];
  current[lastKey] = mutation.newValue;
  
  // Backup
  const backupPath = `${configPath}.backup.${Date.now()}`;
  fs.copyFileSync(configPath, backupPath);
  
  // Write
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
  
  log('SUCCESS', `smriti.json updated: ${mutation.path}`);
  log('INFO', `Value: ${oldValue} → ${mutation.newValue}`);
  
  return { success: true, backup: backupPath, oldValue, newValue: mutation.newValue };
}

function mutateBridgeConfig(mutation) {
  // For Type C mutations, just log for now (requires manual implementation)
  log('INFO', 'Bridge config mutation logged (Type C requires manual review)');
  return { success: true, manualReviewRequired: true };
}

// ═══════════════════════════════════════════════════════════════════
// APPROVAL SYSTEM
// ═══════════════════════════════════════════════════════════════════

function requestApproval(mutation) {
  const approval = {
    mutation_id: mutation.id,
    timestamp: new Date().toISOString(),
    type: mutation.type,
    description: mutation.suggested,
    target: mutation.target,
    change: mutation.change,
    current_value: mutation.currentValue,
    new_value: mutation.newValue,
    rationale: mutation.pattern,
    risk: mutation.type === 'C' ? 'High' : 'Low',
    status: 'pending',
    timeout: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
  };
  
  fs.writeFileSync(PATHS.approvalQueue, JSON.stringify(approval, null, 2));
  
  log('INFO', 'Approval requested', { 
    mutationId: mutation.id,
    queue: PATHS.approvalQueue 
  });
  
  return approval;
}

function checkExistingApproval(mutation) {
  if (!fs.existsSync(PATHS.approvalQueue)) {
    return null;
  }
  
  try {
    const approval = JSON.parse(fs.readFileSync(PATHS.approvalQueue, 'utf8'));
    if (approval.status === 'approved' && approval.mutation_id === mutation.id) {
      return approval;
    }
    if (approval.status === 'pending') {
      log('INFO', 'Previous approval still pending');
      return 'pending';
    }
  } catch (e) {
    // Invalid approval file
  }
  
  return null;
}

// ═══════════════════════════════════════════════════════════════════
// MAIN
// ═══════════════════════════════════════════════════════════════════

console.log('╔════════════════════════════════════════════════════════════╗');
console.log('║  OUROBOROS Mutation Engine v2.0                          ║');
console.log('║  Self-Improvement Through Executable Mutation              ║');
console.log('╚════════════════════════════════════════════════════════════╝');
console.log();

// Ensure directories exist
if (!fs.existsSync(NEURON_DIR)) {
  fs.mkdirSync(NEURON_DIR, { recursive: true });
}

// Check signal
const signal = checkSignalStrength();

if (signal.signal === 0) {
  console.log('📊 No significant signals detected');
  console.log(`   Reason: ${signal.reason}`);
  process.exit(0);
}

console.log(`🔔 Signal detected: ${signal.signal} (Type ${signal.type})`);
console.log(`   Pattern: ${signal.pattern}`);
console.log(`   Suggested: ${signal.suggested}`);
console.log();

// Generate mutation
const mutation = {
  id: `mut_${Date.now()}`,
  ...signal
};

// Check if auto-approved
if (signal.auto || FORCE) {
  console.log('✅ Auto-executing mutation...');
  
  if (DRY_RUN) {
    console.log('   (Dry run mode — no changes)');
  }
  
  const result = executeMutation(mutation);
  
  if (result.success) {
    // Log to mutations
    const mutationLog = {
      ...mutation,
      executed: new Date().toISOString(),
      result: result.success ? 'success' : 'failed',
      dryRun: DRY_RUN || false
    };
    
    fs.appendFileSync(PATHS.mutations, JSON.stringify(mutationLog) + '\n');
    
    console.log();
    console.log('✅ Mutation completed successfully');
    if (result.backup) {
      console.log(`   Backup: ${result.backup}`);
    }
  } else {
    console.log('❌ Mutation failed:', result.error);
    process.exit(1);
  }
} else {
  // Request approval
  console.log('⏳ Requesting approval...');
  const approval = requestApproval(mutation);
  
  console.log();
  console.log('📋 Approval queued:');
  console.log(`   File: ${PATHS.approvalQueue}`);
  console.log(`   Review and run with --force to apply`);
}

console.log();
console.log('🐍 OUROBOROS complete');
