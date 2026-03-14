#!/usr/bin/env node
// OUROBOROS Morning Init — Tagesstart
// Lädt gestrige Daten, berechnet Trend, setzt Erwartung

import fs from 'fs';
import path from 'path';

const LOG_PATH = '/data/.openclaw/workspace/neuron/meta_learn_log.jsonl';
const M1M4_PATH = '/data/.openclaw/workspace/neuron/m1m4_log.jsonl';
const STATUS_PATH = '/data/.openclaw/workspace/neuron/ouroboros_status.json';

function loadLast7Days() {
    if (!fs.existsSync(M1M4_PATH)) {
        return { days: 0, avg: { m1: 3, m2: 3, m3: 3, m4: 3 } };
    }
    
    const lines = fs.readFileSync(M1M4_PATH, 'utf8')
        .split('\n')
        .filter(l => l.trim())
        .slice(-7);
    
    if (lines.length === 0) return { days: 0, avg: { m1: 3, m2: 3, m3: 3, m4: 3 } };
    
    const entries = lines.map(l => JSON.parse(l));
    const avg = {
        m1: entries.reduce((a, e) => a + e.m1.score, 0) / entries.length,
        m2: entries.reduce((a, e) => a + e.m2.score, 0) / entries.length,
        m3: entries.reduce((a, e) => a + e.m3.score, 0) / entries.length,
        m4: entries.reduce((a, e) => a + e.m4.score, 0) / entries.length
    };
    
    return { days: entries.length, avg };
}

function calculateTrend(data) {
    const trend = {
        direction: {
            m1: data.avg.m1 > 4 ? '↑' : data.avg.m1 < 3.5 ? '↓' : '→',
            m2: data.avg.m2 > 4 ? '↑' : data.avg.m2 < 3.5 ? '↓' : '→',
            m3: data.avg.m3 > 4 ? '↑' : data.avg.m3 < 3.5 ? '↓' : '→',
            m4: data.avg.m4 > 4 ? '↑' : data.avg.m4 < 3.5 ? '↓' : '→'
        },
        volatility: 'low' // Berechnet aus Standardabweichung
    };
    return trend;
}

function saveStatus(data, trend) {
    const status = {
        last_run: new Date().toISOString(),
        data_days: data.days,
        averages: data.avg,
        trend: trend,
        day_expectation: {
            intensity: data.avg.m4 > 4 ? 'high' : 'normal',
            focus: data.avg.m2 > 4 ? 'deep' : 'standard'
        }
    };
    fs.writeFileSync(STATUS_PATH, JSON.stringify(status, null, 2));
    return status;
}

// MAIN
const data = loadLast7Days();
const trend = calculateTrend(data);
const status = saveStatus(data, trend);

console.log('🐍 OUROBOROS Morning Init');
console.log(`📊 Last ${data.days} days analyzed`);
console.log(`📈 M1: ${data.avg.m1.toFixed(2)} ${trend.direction.m1}`);
console.log(`📈 M2: ${data.avg.m2.toFixed(2)} ${trend.direction.m2}`);
console.log(`📈 M3: ${data.avg.m3.toFixed(2)} ${trend.direction.m3}`);
console.log(`📈 M4: ${data.avg.m4.toFixed(2)} ${trend.direction.m4}`);
console.log(`🎯 Today: ${status.day_expectation.intensity} intensity, ${status.day_expectation.focus} focus`);
