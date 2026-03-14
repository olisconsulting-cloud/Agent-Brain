#!/usr/bin/env node
/**
 * Auto-Optimizer v3.5 — Autonome System-Optimierung
 * 
 * Läuft automatisch im Hintergrund:
 * - Überwacht M1-M5 Scores
 * - Erstellt Mutationen bei niedrigen Werten
 * - Optimiert ohne menschliches Zutun
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || '/data/.openclaw/workspace';
const NEURON_DIR = path.join(WORKSPACE, 'neuron');
const M1M4_LOG = path.join(NEURON_DIR, 'm1m4_log.jsonl');
const MUTATION_QUEUE = path.join(NEURON_DIR, 'ouroboros_auto_mutations.jsonl');

// Thresholds für Auto-Optimization
const THRESHOLDS = {
  m1: { warning: 3.0, critical: 2.0 },
  m2: { warning: 3.0, critical: 2.0 },
  m3: { warning: 3.0, critical: 2.0 },
  m4: { warning: 3.0, critical: 2.0 },
  m5: { warning: 3.0, critical: 2.0 }
};

function loadRecentMetrics(hours = 24) {
  if (!fs.existsSync(M1M4_LOG)) {
    return [];
  }
  
  const cutoff = Date.now() - (hours * 60 * 60 * 1000);
  const lines = fs.readFileSync(M1M4_LOG, 'utf8')
    .split('\n')
    .filter(l => l.trim())
    .map(l => JSON.parse(l))
    .filter(e => new Date(e.timestamp).getTime() > cutoff);
  
  return lines;
}

function calculateAverages(metrics) {
  if (metrics.length === 0) return null;
  
  return {
    m1: metrics.reduce((a, e) => a + (e.m1 || e.m1_predictive_surprise || 0), 0) / metrics.length,
    m2: metrics.reduce((a, e) => a + (e.m2 || e.m2_denkraum_expansion || 0), 0) / metrics.length,
    m3: metrics.reduce((a, e) => a + (e.m3 || e.m3_paradigm_shift || 0), 0) / metrics.length,
    m4: metrics.reduce((a, e) => a + (e.m4 || e.m4_session_velocity || 0), 0) / metrics.length,
    m5: metrics.reduce((a, e) => a + (e.m5 || e.m5_anti_fragile_resonanz || 0), 0) / metrics.length,
    count: metrics.length
  };
}

function generateOptimizationMutation(metric, value, threshold) {
  const mutations = {
    m1: {
      type: 'A',
      action: 'lower_quality_threshold',
      description: 'M1 zu niedrig → Threshold senken für mehr Überraschungen',
      config_change: { path: 'system_1_quality.threshold', delta: -0.1 }
    },
    m2: {
      type: 'A',
      action: 'enable_more_frameworks',
      description: 'M2 zu niedrig → Mehr Frameworks aktivieren',
      config_change: { path: 'system_1_quality.frameworks', add: ['first_principles', 'systems_thinking'] }
    },
    m3: {
      type: 'A',
      action: 'increase_shift_sensitivity',
      description: 'M3 zu niedrig → Shift-Erkennung empfindlicher',
      config_change: { path: 'system_1_quality.shift_sensitivity', value: 0.8 }
    },
    m4: {
      type: 'A',
      action: 'reduce_reflection_depth',
      description: 'M4 zu niedrig → Schnellere Iterationen',
      config_change: { path: 'system_1_quality.reflection_depth', delta: -1 }
    },
    m5: {
      type: 'A',
      action: 'enable_anti_fragile_mode',
      description: 'M5 zu niedrig → Anti-fragile Mode aktivieren',
      config_change: { path: 'system_1_quality.anti_fragile_mode', value: true }
    }
  };
  
  return mutations[metric];
}

function applyOptimization(mutation) {
  const configPath = path.join(NEURON_DIR, 'smriti.json');
  
  try {
    // Load current config
    let config = {};
    if (fs.existsSync(configPath)) {
      config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    }
    
    // Apply change
    const change = mutation.config_change;
    if (change.delta) {
      // Delta change
      const current = getNestedValue(config, change.path) || 0.8;
      setNestedValue(config, change.path, current + change.delta);
    } else if (change.add) {
      // Add to array
      const current = getNestedValue(config, change.path) || [];
      setNestedValue(config, change.path, [...new Set([...current, ...change.add])]);
    } else if (change.value !== undefined) {
      // Set value
      setNestedValue(config, change.path, change.value);
    }
    
    // Save config
    fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
    
    return { success: true, config: configPath };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

function getNestedValue(obj, path) {
  return path.split('.').reduce((o, p) => o && o[p], obj);
}

function setNestedValue(obj, path, value) {
  const parts = path.split('.');
  const last = parts.pop();
  const target = parts.reduce((o, p) => {
    if (!o[p]) o[p] = {};
    return o[p];
  }, obj);
  target[last] = value;
}

function logMutation(mutation, result) {
  const entry = {
    timestamp: new Date().toISOString(),
    mutation,
    result,
    auto_executed: true
  };
  
  fs.appendFileSync(MUTATION_QUEUE, JSON.stringify(entry) + '\n');
}

// MAIN
console.log('🔧 Auto-Optimizer v3.5');
console.log('');

const metrics = loadRecentMetrics(24);
if (metrics.length === 0) {
  console.log('ℹ️  Keine Metriken in den letzten 24h');
  process.exit(0);
}

const avg = calculateAverages(metrics);
console.log(`📊 ${metrics.length} Sessions analysiert`);
console.log(`   M1: ${avg.m1.toFixed(2)} | M2: ${avg.m2.toFixed(2)} | M3: ${avg.m3.toFixed(2)} | M4: ${avg.m4.toFixed(2)} | M5: ${avg.m5.toFixed(2)}`);
console.log('');

let optimizations = 0;

// Check each metric
for (const [metric, thresholds] of Object.entries(THRESHOLDS)) {
  const value = avg[metric];
  
  if (value < thresholds.critical) {
    console.log(`🔴 ${metric.toUpperCase()} kritisch (${value.toFixed(2)} < ${thresholds.critical})`);
    
    const mutation = generateOptimizationMutation(metric, value, thresholds);
    const result = applyOptimization(mutation);
    
    logMutation(mutation, result);
    
    if (result.success) {
      console.log(`   ✅ Auto-Optimierung: ${mutation.description}`);
      optimizations++;
    } else {
      console.log(`   ❌ Fehler: ${result.error}`);
    }
  } else if (value < thresholds.warning) {
    console.log(`🟡 ${metric.toUpperCase()} niedrig (${value.toFixed(2)} < ${thresholds.warning})`);
    console.log(`   💡 Empfehlung: ${generateOptimizationMutation(metric, value, thresholds).description}`);
  }
}

console.log('');
if (optimizations > 0) {
  console.log(`✅ ${optimizations} Auto-Optimierungen durchgeführt`);
} else {
  console.log('✅ Alle Metriken im grünen Bereich');
}
