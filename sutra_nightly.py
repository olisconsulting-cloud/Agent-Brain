#!/usr/bin/env python3
"""
Sutra Nightly Consolidator v1.0
- Dedupliziert ähnliche Sessions
- Analysiert Patterns über Zeit
- Generiert OUROBOROS Mutation-Vorschläge
- Passt Thresholds an
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

def load_sutra():
    """Lade alle Sutra-Einträge"""
    sutra_path = Path('/data/.openclaw/workspace/neuron/sutra_session_memory.jsonl')
    
    if not sutra_path.exists():
        return []
    
    entries = []
    with open(sutra_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get('version', '').startswith('sutra'):
                    entries.append(entry)
            except json.JSONDecodeError:
                continue
    
    return entries

def find_similar_sessions(entries, threshold=0.7):
    """Finde ähnliche Sessions basierend auf Jaccard-Ähnlichkeit"""
    similar_pairs = []
    
    for i, entry1 in enumerate(entries):
        for entry2 in entries[i+1:]:
            similarity = calculate_similarity(entry1, entry2)
            if similarity >= threshold:
                similar_pairs.append((entry1, entry2, similarity))
    
    return similar_pairs

def calculate_similarity(entry1, entry2):
    """Berechne Jaccard-Ähnlichkeit zwischen zwei Sessions"""
    
    # Vergleiche Insights
    insights1 = set(entry1.get('insights', []))
    insights2 = set(entry2.get('insights', []))
    
    if not insights1 and not insights2:
        return 0.0
    
    intersection = len(insights1 & insights2)
    union = len(insights1 | insights2)
    
    return intersection / union if union > 0 else 0.0

def merge_similar_entries(entry1, entry2):
    """Merge zwei ähnliche Einträge zu einem"""
    
    merged = {
        'version': 'sutra-v1.0-merged',
        'session_id': f"{entry1['session_id'][:8]}_{entry2['session_id'][:8]}",
        'timestamp': max(entry1['timestamp'], entry2['timestamp']),
        'summary': f"Merged: {entry1['summary'][:50]} + {entry2['summary'][:50]}",
        'insights': list(set(entry1.get('insights', []) + entry2.get('insights', [])))[:7],
        'decisions': list(set(entry1.get('decisions', []) + entry2.get('decisions', [])))[:7],
        'patterns': list(set(entry1.get('patterns', []) + entry2.get('patterns', [])))[:5],
        'anti_patterns': list(set(entry1.get('anti_patterns', []) + entry2.get('anti_patterns', [])))[:5],
        'hebel': entry1.get('hebel', False) or entry2.get('hebel', False),
        'quality_score': max(entry1.get('quality_score', 0), entry2.get('quality_score', 0)),
        'merged_from': [entry1['session_id'], entry2['session_id']]
    }
    
    return merged

def analyze_patterns(entries):
    """Analysiere Patterns über alle Sessions"""
    
    all_insights = []
    all_patterns = []
    all_anti_patterns = []
    
    for entry in entries:
        all_insights.extend(entry.get('insights', []))
        all_patterns.extend(entry.get('patterns', []))
        all_anti_patterns.extend(entry.get('anti_patterns', []))
    
    # Zähle Häufigkeiten
    insight_counter = Counter([i[:50] for i in all_insights])  # Truncate for comparison
    pattern_counter = Counter([p[:50] for p in all_patterns])
    anti_pattern_counter = Counter([a[:50] for a in all_anti_patterns])
    
    # Finde wiederkehrende (mehr als 1x)
    recurring_insights = [(insight, count) for insight, count in insight_counter.items() if count > 1]
    recurring_patterns = [(pattern, count) for pattern, count in pattern_counter.items() if count > 1]
    recurring_anti_patterns = [(ap, count) for ap, count in anti_pattern_counter.items() if count > 1]
    
    return {
        'recurring_insights': recurring_insights[:5],
        'recurring_patterns': recurring_patterns[:5],
        'recurring_anti_patterns': recurring_anti_patterns[:5],
        'total_sessions': len(entries),
        'avg_quality': sum(e.get('quality_score', 0) for e in entries) / len(entries) if entries else 0
    }

def generate_ouroboros_mutations(analysis):
    """Generiere OUROBOROS Mutation-Vorschläge basierend auf Patterns"""
    
    mutations = []
    
    # Pattern-basierte Mutationen
    for pattern, count in analysis.get('recurring_patterns', []):
        if count >= 3:  # Starkes Pattern
            mutations.append({
                'type': 'B',  # Behavioral
                'trigger': f"Pattern detected {count}x: {pattern[:30]}...",
                'suggestion': f"Consider automating or optimizing this pattern",
                'confidence': min(count * 0.15, 0.8)  # Konservativer
            })
    
    # Anti-Pattern-basierte Mutationen
    for ap, count in analysis.get('recurring_anti_patterns', []):
        if count >= 2:  # Wiederkehrendes Problem
            mutations.append({
                'type': 'A',  # Architectural
                'trigger': f"Anti-Pattern {count}x: {ap[:30]}...",
                'suggestion': f"Implement guardrail to prevent this",
                'confidence': min(count * 0.2, 0.8)  # Konservativer
            })
    
    # Quality-basierte Mutation
    avg_quality = analysis.get('avg_quality', 0)
    if avg_quality < 0.6:
        mutations.append({
            'type': 'C',  # Config
            'trigger': f"Low avg quality: {avg_quality:.2f}",
            'suggestion': "Raise extraction thresholds or improve prompts",
            'confidence': 0.7
        })
    
    return mutations

def adjust_thresholds(entries):
    """Passe Thresholds basierend auf Quality-Scores an"""
    
    if len(entries) < 5:
        return None  # Nicht genug Daten
    
    scores = [e.get('quality_score', 0) for e in entries]
    avg_score = sum(scores) / len(scores)
    
    # Dynamische Thresholds
    if avg_score > 0.8:
        # Hohe Qualität → Erhöhe Mindestanforderungen
        return {
            'min_messages': 15,  # Statt 10
            'min_quality': 0.7,   # Statt 0.5
            'reason': f"High quality trend ({avg_score:.2f})"
        }
    elif avg_score < 0.5:
        # Niedrige Qualität → Senke Anforderungen
        return {
            'min_messages': 8,
            'min_quality': 0.4,
            'reason': f"Low quality trend ({avg_score:.2f})"
        }
    
    return None  # Keine Änderung nötig

def save_consolidated(entries, analysis, mutations, thresholds):
    """Speichere konsolidierte Daten"""
    
    consolidated = {
        'version': 'sutra-consolidated-v1.0',
        'timestamp': datetime.now().isoformat(),
        'session_count': len(entries),
        'analysis': analysis,
        'ouroboros_mutations': mutations,
        'threshold_adjustments': thresholds,
        'entries': entries[-20:]  # Letzte 20
    }
    
    output_path = Path('/data/.openclaw/workspace/neuron/sutra_consolidated.json')
    with open(output_path, 'w') as f:
        json.dump(consolidated, f, indent=2, ensure_ascii=False)
    
    return output_path

def main():
    """Hauptfunktion: Nightly-Konsolidierung"""
    
    log_file = Path('/data/.openclaw/workspace/smriti/logs/sutra_nightly.log')
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log(msg):
        print(msg)
        with open(log_file, 'a') as f:
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")
    
    log("🌙 Sutra Nightly Consolidation")
    log("=" * 40)
    
    # Lade Sutra
    entries = load_sutra()
    
    if len(entries) < 3:
        log(f"⏭️  Nur {len(entries)} Session(s), überspringe (min: 3)")
        return
    
    log(f"📊 Geladen: {len(entries)} Sessions")
    
    # Finde ähnliche Sessions
    similar = find_similar_sessions(entries, threshold=0.6)
    log(f"🔍 Ähnliche Sessions gefunden: {len(similar)}")
    
    # Merge ähnliche (max 1 pro Nacht, nur wenn >5 ähnliche)
    merged_count = 0
    if len(similar) >= 5:  # Höherer Threshold
        log("🔄 Merging ähnliche Sessions (max 1)...")
        # Nur das ähnlichste Paar
        similar.sort(key=lambda x: x[2], reverse=True)
        entry1, entry2, sim = similar[0]
        
        # Backup vor Merge
        sutra_path = Path('/data/.openclaw/workspace/neuron/sutra_session_memory.jsonl')
        backup_path = sutra_path.with_suffix('.jsonl.bak')
        import shutil
        shutil.copy(sutra_path, backup_path)
        
        merged = merge_similar_entries(entry1, entry2)
        entries = [e for e in entries if e['session_id'] not in [entry1['session_id'], entry2['session_id']]]
        entries.append(merged)
        merged_count = 1
        log(f"✅ 1 Session gemerged (Backup: {backup_path})")
    
    # Analysiere Patterns
    analysis = analyze_patterns(entries)
    log(f"📈 Analysis:")
    log(f"   - Recurring Insights: {len(analysis['recurring_insights'])}")
    log(f"   - Recurring Patterns: {len(analysis['recurring_patterns'])}")
    log(f"   - Recurring Anti-Patterns: {len(analysis['recurring_anti_patterns'])}")
    log(f"   - Avg Quality: {analysis['avg_quality']:.2f}")
    
    # Generiere OUROBOROS Mutationen
    mutations = generate_ouroboros_mutations(analysis)
    log(f"🐍 OUROBOROS Mutationen: {len(mutations)}")
    for m in mutations:
        log(f"   - [{m['type']}] {m['trigger'][:40]}...")
    
    # Passe Thresholds an
    thresholds = adjust_thresholds(entries)
    if thresholds:
        log(f"⚙️  Thresholds angepasst:")
        log(f"   - Min Messages: {thresholds['min_messages']}")
        log(f"   - Min Quality: {thresholds['min_quality']}")
        log(f"   - Grund: {thresholds['reason']}")
    
    # Speichere konsolidiert
    output_path = save_consolidated(entries, analysis, mutations, thresholds)
    log(f"💾 Gespeichert: {output_path}")
    
    log("=" * 40)
    log("✅ Nightly Consolidation abgeschlossen")

if __name__ == '__main__':
    main()
