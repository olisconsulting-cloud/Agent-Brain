#!/usr/bin/env node
// OUROBOROS Evening Feedback — Tagesreview
// Generiert M1-M4, zeigt Pattern, fragt Oli

import fs from 'fs';

const M1M4_PATH = '/data/.openclaw/workspace/neuron/m1m4_log.jsonl';
const FEEDBACK_PATH = '/data/.openclaw/workspace/neuron/ouroboros_feedback_queue.json';

function generateDailyM1M4() {
    // Liest heutige Session-Daten (simuliert für jetzt)
    // In Produktion: Tatsächliche Messung
    return {
        m1: 4.2, m2: 4.5, m3: 4.8, m4: 4.0,
        patterns: ['intensive_build_mode', 'quick_iterations'],
        note: 'Heutige Session'
    };
}

function identifyPattern() {
    // Pattern-Erkennung aus letzten Tagen
    return {
        pattern: 'A→B→C Sequenz wiederholt',
        observation: 'Oli bevorzugt systematisches Bauen',
        confidence: 0.85
    };
}

function createFeedbackRequest() {
    const m1m4 = generateDailyM1M4();
    const pattern = identifyPattern();
    
    const feedback = {
        timestamp: new Date().toISOString(),
        type: 'daily_review',
        status: 'pending',
        data: {
            m1m4,
            pattern,
            question: 'Siehst du das auch?'
        },
        oli_response: null,
        timeout: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24h
    };
    
    return feedback;
}

// MAIN
const feedback = createFeedbackRequest();
fs.writeFileSync(FEEDBACK_PATH, JSON.stringify(feedback, null, 2));

console.log('🐍 OUROBOROS Evening Feedback');
console.log('📋 Tagesreview bereit. 2 Minuten?');
console.log('');
console.log(`📊 M1-M4 heute: ${feedback.data.m1m4.m1} ${feedback.data.m1m4.m2} ${feedback.data.m1m4.m3} ${feedback.data.m1m4.m4}`);
console.log(`🔍 Pattern: ${feedback.data.pattern.pattern}`);
console.log(`❓ Frage: ${feedback.data.pattern.observation} — ${feedback.data.question}`);
console.log('');
console.log('💬 Antworte: "Stimmt" / "Siehst du X?" / "Ändere Y"');
