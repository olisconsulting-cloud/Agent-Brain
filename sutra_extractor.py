#!/usr/bin/env python3
"""
Sutra Session Extractor v1.0
Auto-extrahiert Essenz aus Session für sutra_session_memory.jsonl
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def extract_session_essence(session_data):
    """Extrahiere Insights, Decisions, Patterns, Anti-Patterns aus Session"""
    
    messages = session_data.get('messages', [])
    
    insights = []
    decisions = []
    patterns = []
    anti_patterns = []
    
    # Generiere Summary aus ersten 3 Nachrichten
    summary = generate_summary(messages)
    
    for msg in messages:
        if msg.get('role') == 'assistant':
            content = msg.get('content', [])
            for item in content:
                if item.get('type') == 'text':
                    text = item.get('text', '')
                    
                    # Skip: Zu kurz, keine Substanz
                    if len(text) < 20:
                        continue
                    
                    # Insights erkennen (🐾 oder Erkenntnis-Sätze)
                    if '🐾' in text or 'Erkenntnis' in text or 'gelernt' in text.lower():
                        insights.append(text[:100])  # Kürzer für Kompaktheit
                    
                    # Decisions erkennen (Entscheidung, beschlossen, festgelegt)
                    if any(word in text.lower() for word in ['entschieden', 'beschlossen', 'festgelegt', 'aktualisiert', 'erledigt', 'implementiert']):
                        decisions.append(text[:100])
                    
                    # Patterns erkennen (Pattern:, Muster:, immer wieder)
                    if 'Pattern' in text or 'Muster' in text or 'immer wieder' in text.lower():
                        patterns.append(text[:100])
                    
                    # Anti-Patterns erkennen (Fehler, Problem, nicht funktioniert)
                    if any(word in text.lower() for word in ['fehler', 'problem', 'nicht funktioniert', 'behoben', 'bug']):
                        anti_patterns.append(text[:100])
    
    return {
        'summary': summary,
        'insights': list(set(insights))[:5],  # Max 5, dedupliziert
        'decisions': list(set(decisions))[:5],
        'patterns': list(set(patterns))[:3],
        'anti_patterns': list(set(anti_patterns))[:3]
    }

def generate_summary(messages):
    """Generiere Summary aus ersten 3 Nachrichten"""
    summary_parts = []
    
    for msg in messages[:3]:
        content = msg.get('content', [])
        for item in content:
            if item.get('type') == 'text':
                text = item.get('text', '')
                # Extrahiere erste Zeile oder ersten Satz
                first_line = text.split('\n')[0][:80]
                if first_line:
                    summary_parts.append(first_line)
    
    return ' | '.join(summary_parts)[:150] if summary_parts else 'Session abgeschlossen'

def append_to_sutra(session_id, essence):
    """Füge extrahierte Essenz zu sutra_session_memory.jsonl hinzu"""
    
    sutra_path = Path('/data/.openclaw/workspace/neuron/sutra_session_memory.jsonl')
    
    # Duplikat-Check
    if session_exists(sutra_path, session_id):
        print(f"⚠️  Session {session_id[:8]}... bereits in Sutra")
        return None
    
    # Berechne Quality-Score (Heuristik)
    score = calculate_quality_score(essence)
    
    entry = {
        'version': 'sutra-v1.0',
        'session_id': session_id,
        'timestamp': datetime.now().isoformat(),
        'summary': essence.get('summary', 'Session abgeschlossen'),
        'insights': essence.get('insights', []),
        'decisions': essence.get('decisions', []),
        'patterns': essence.get('patterns', []),
        'anti_patterns': essence.get('anti_patterns', []),
        'hebel': len(essence.get('insights', [])) > 0,
        'quality_score': score
    }
    
    # Atomares Append (Temp → Rename)
    temp_path = sutra_path.with_suffix('.tmp')
    
    # Kopiere existierende + neue Zeile
    existing = []
    if sutra_path.exists():
        with open(sutra_path, 'r') as f:
            existing = [line for line in f if line.strip()]
    
    existing.append(json.dumps(entry, ensure_ascii=False) + '\n')
    
    # Rotation
    if len(existing) > 20:
        existing = existing[-20:]
    
    # Schreibe atomar
    with open(temp_path, 'w') as f:
        f.writelines(existing)
    
    temp_path.rename(sutra_path)
    
    return entry

def session_exists(sutra_path, session_id):
    """Prüfe ob Session-ID bereits existiert"""
    if not sutra_path.exists():
        return False
    
    with open(sutra_path, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get('session_id') == session_id:
                    return True
            except:
                continue
    return False

def calculate_quality_score(essence):
    """Berechne Quality-Score basierend auf Inhalt"""
    score = 0.0
    
    # Insights = 0.2 pro Stück, max 1.0
    score += min(len(essence.get('insights', [])) * 0.2, 1.0)
    
    # Decisions = 0.15 pro Stück, max 0.6
    score += min(len(essence.get('decisions', [])) * 0.15, 0.6)
    
    # Patterns/Anti-Patterns = 0.1 pro Stück, max 0.4
    score += min(len(essence.get('patterns', [])) * 0.1, 0.2)
    score += min(len(essence.get('anti_patterns', [])) * 0.1, 0.2)
    
    return min(round(score, 2), 1.0)

def rotate_sutra(sutra_path, max_entries=20):
    """FIFO-Rotation: Behalte nur letzte N Einträge"""
    
    if not sutra_path.exists():
        return
    
    lines = []
    with open(sutra_path, 'r') as f:
        lines = [line for line in f if line.strip()]
    
    if len(lines) > max_entries:
        lines = lines[-max_entries:]  # Behalte nur letzte N
        with open(sutra_path, 'w') as f:
            f.writelines(lines)

def main():
    """Hauptfunktion: Lese Session, extrahiere, speichere"""
    
    if len(sys.argv) < 2:
        print("Usage: sutra_extractor.py <session_file.jsonl>")
        sys.exit(1)
    
    session_file = Path(sys.argv[1])
    
    if not session_file.exists():
        print(f"❌ Error: Session file not found: {session_file}")
        sys.exit(1)
    
    # Lese Session (JSONL Format - mehrere JSON-Objekte)
    try:
        messages = []
        with open(session_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    messages.append(msg)
                except json.JSONDecodeError:
                    continue
        
        # Baue Session-Data
        session_data = {
            'session_id': session_file.stem,
            'messages': messages
        }
    except Exception as e:
        print(f"❌ Error reading session file: {e}")
        sys.exit(1)
    
    session_id = session_file.stem  # Aus Dateiname
    
    # Extrahiere Essenz
    essence = extract_session_essence(session_data)
    
    # Füge zu Sutra hinzu
    entry = append_to_sutra(session_id, essence)
    
    if entry:
        print(f"🧵 Sutra: Session {session_id[:8]}... extrahiert")
        print(f"   Summary: {entry['summary'][:50]}...")
        print(f"   Insights: {len(entry['insights'])}")
        print(f"   Decisions: {len(entry['decisions'])}")
        print(f"   Patterns: {len(entry['patterns'])}")
        print(f"   Anti-Patterns: {len(entry['anti_patterns'])}")
        print(f"   Quality: {entry['quality_score']}")
    else:
        print(f"⏭️  Sutra: Session {session_id[:8]}... übersprungen (Duplikat)")

if __name__ == '__main__':
    main()
