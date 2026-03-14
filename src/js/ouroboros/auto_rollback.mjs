#!/usr/bin/env node
// OUROBOROS Auto-Rollback — Safety-Net

import fs from 'fs';

const M1M4_PATH = '/data/.openclaw/workspace/neuron/m1m4_log.jsonl';
const SNAPSHOT_DIR = '/data/.openclaw/workspace/temporal/snapshots';
const LOG_PATH = '/data/.openclaw/workspace/neuron/meta_learn_log.jsonl';

function checkRollbackCondition() {
    // Prüfe letzte 48h seit Mutation
    if (!fs.existsSync(LOG_PATH)) return { rollback: false };
    
    const logs = fs.readFileSync(LOG_PATH, 'utf8')
        .split('\n')
        .filter(l => l.trim())
        .map(l => JSON.parse(l));
    
    const lastMutation = logs.reverse().find(l => l.mutation);
    if (!lastMutation) return { rollback: false };
    
    const hoursSinceMutation = (Date.now() - new Date(lastMutation.timestamp)) / (1000 * 60 * 60);
    if (hoursSinceMutation > 48) return { rollback: false }; // Zeitfenster vorbei
    
    // Prüfe M3
    if (!fs.existsSync(M1M4_PATH)) return { rollback: false };
    
    const m1m4Lines = fs.readFileSync(M1M4_PATH, 'utf8')
        .split('\n')
        .filter(l => l.trim())
        .slice(-5); // Letzte 5 Sessions
    
    const entries = m1m4Lines.map(l => JSON.parse(l));
    const avgM3 = entries.reduce((a, e) => a + e.m3.score, 0) / entries.length;
    
    if (avgM3 < 4.0) {
        return {
            rollback: true,
            reason: `M3 dropped to ${avgM3.toFixed(2)} (threshold: 4.0)`,
            mutation: lastMutation,
            hours_since: hoursSinceMutation
        };
    }
    
    return { rollback: false };
}

function performRollback(info) {
    // Finde Snapshot vor Mutation
    const snapshots = fs.readdirSync(SNAPSHOT_DIR)
        .filter(d => d.match(/^\d{4}-\d{2}$/))
        .sort()
        .reverse();
    
    if (snapshots.length === 0) {
        console.log('❌ No snapshot found for rollback');
        return false;
    }
    
    const latestSnapshot = snapshots[0];
    console.log(`🔄 Rolling back to snapshot: ${latestSnapshot}`);
    
    // Logge Rollback
    const rollbackLog = {
        timestamp: new Date().toISOString(),
        type: 'auto_rollback',
        reason: info.reason,
        mutation_id: info.mutation.mutation_id,
        snapshot_restored: latestSnapshot,
        hours_since_mutation: info.hours_since
    };
    
    fs.appendFileSync(LOG_PATH, JSON.stringify(rollbackLog) + '\n');
    
    // Hier: Tatsächlicher Restore-Code
    console.log('✅ Rollback logged. Manual restore: ./scripts/restore_snapshot.sh ' + latestSnapshot);
    return true;
}

// MAIN
const check = checkRollbackCondition();

if (check.rollback) {
    console.log('🚨 OUROBOROS Auto-Rollback TRIGGERED');
    console.log(`⚠️  Reason: ${check.reason}`);
    console.log(`⏰ Hours since mutation: ${check.hours_since.toFixed(1)}`);
    performRollback(check);
} else {
    console.log('🐍 OUROBOROS Auto-Rollback');
    console.log('✅ All systems within thresholds');
}
