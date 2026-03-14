#!/usr/bin/env python3
"""
Reflecty v2.0 — Pattern Mining Sub-Agent

Analysiert Sessions, extrahiert Muster und Anti-Patterns,
speichert Erkenntnisse in Smriti (mem0).

Usage:
    python reflecty.py --session <session_key> --mode analyze
    python reflecty.py --mode daily_synthesis
    python reflecty.py --mode test

Environment Variables:
    SMRITI_MEM0_URL — mem0 endpoint (default: http://localhost:8000)
    SMRITI_USER_ID — User ID for mem0 (default: default)
    SMRITI_WORKSPACE — Workspace path (default: ~/.openclaw/workspace)
"""

import json
import hashlib
import argparse
import urllib.request
import urllib.parse
import os
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION (Environment-based)
# ═══════════════════════════════════════════════════════════════════

MEM0_URL = os.environ.get('SMRITI_MEM0_URL', 'http://localhost:8000')
USER_ID = os.environ.get('SMRITI_USER_ID', 'default')
AGENT_ID = 'reflecty'
WORKSPACE = os.environ.get('SMRITI_WORKSPACE', str(Path.home() / '.openclaw/workspace'))

# ═══════════════════════════════════════════════════════════════════
# ERROR HANDLING
# ═══════════════════════════════════════════════════════════════════

class SmritiError(Exception):
    """Base error for Smriti operations"""
    pass

class Mem0ConnectionError(SmritiError):
    """Failed to connect to mem0"""
    pass

class ConfigError(SmritiError):
    """Configuration error"""
    pass

# ═══════════════════════════════════════════════════════════════════
# DATA CLASSES
# ═══════════════════════════════════════════════════════════════════

@dataclass
class Pattern:
    """Ein erkanntes Verhaltensmuster"""
    pattern_id: str
    pattern_type: str  # behavioral|communication|technical|meta
    description: str
    frequency: int
    confidence: float
    examples: List[str]
    related_patterns: List[str]
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AntiPattern:
    """Ein identifiziertes Anti-Pattern"""
    anti_pattern_id: str
    description: str
    root_cause: str
    impact: str  # low|medium|high|critical
    mitigation: str
    depth: int  # 1-5
    occurrences: List[Dict[str, str]]
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AnalysisResult:
    """Ergebnis einer Session-Analyse"""
    patterns_found: int
    anti_patterns_found: int
    patterns: List[Dict]
    anti_patterns: List[Dict]
    insights: List[str]
    timestamp: str
    mem0_status: str
    fallback_used: bool

# ═══════════════════════════════════════════════════════════════════
# SMRITI CLIENT
# ═══════════════════════════════════════════════════════════════════

class SmritiClient:
    """Client für mem0 Integration mit Fallback zu File-System"""
    
    def __init__(self, base_url: str = MEM0_URL, user_id: str = USER_ID):
        self.base_url = base_url
        self.user_id = user_id
        self.agent_id = AGENT_ID
        self.fallback_mode = False
        self.fallback_dir = Path(WORKSPACE) / 'data' / 'memory' / 'reflecty'
        self.fallback_dir.mkdir(parents=True, exist_ok=True)
        
        # Test connection
        self._test_connection()
    
    def _test_connection(self) -> bool:
        """Test mem0 connection, enable fallback if unavailable"""
        try:
            response = self._request("GET", "/health", timeout=5)
            if response and response.get('status') == 'ok':
                self.fallback_mode = False
                return True
        except Exception:
            pass
        
        self.fallback_mode = True
        print(f"⚠️  mem0 unavailable, using file fallback: {self.fallback_dir}")
        return False
    
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                 params: Optional[Dict] = None, timeout: int = 10) -> Optional[Dict]:
        """Generic HTTP request handler with error handling"""
        try:
            url = f"{self.base_url}{endpoint}"
            if params:
                query = "&".join(f"{k}={urllib.parse.quote(str(v))}" for k, v in params.items())
                url = f"{url}?{query}"
            
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            
            if data:
                body = json.dumps(data).encode('utf-8')
                req = urllib.request.Request(url, data=body, method=method, headers=headers)
            else:
                req = urllib.request.Request(url, method=method, headers=headers)
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.URLError as e:
            raise Mem0ConnectionError(f"Cannot connect to mem0: {e}")
        except Exception as e:
            raise SmritiError(f"Request failed: {e}")
    
    def search(self, query: str, limit: int = 20) -> List[Dict]:
        """Suche nach relevanten Memories"""
        if self.fallback_mode:
            return self._fallback_search(query, limit)
        
        try:
            result = self._request("POST", "/search", data={
                "query": query,
                "user_id": self.user_id,
                "limit": limit
            }, timeout=10)
            return result.get("results", []) if result else []
        except Mem0ConnectionError:
            self.fallback_mode = True
            return self._fallback_search(query, limit)
    
    def _fallback_search(self, query: str, limit: int) -> List[Dict]:
        """File-based search fallback"""
        results = []
        query_lower = query.lower()
        
        for file in self.fallback_dir.glob('*.json'):
            try:
                with open(file) as f:
                    data = json.load(f)
                    content = data.get('content', '').lower()
                    if query_lower in content:
                        results.append(data)
            except Exception:
                continue
        
        return results[:limit]
    
    def store_insight(self, insight: str, metadata: Dict) -> bool:
        """Speichert eine Erkenntnis in Smriti oder Fallback"""
        if self.fallback_mode:
            return self._fallback_store(insight, metadata)
        
        try:
            payload = {
                "messages": [{"role": "assistant", "content": insight}],
                "user_id": self.user_id,
                "agent_id": self.agent_id,
                "metadata": {
                    **metadata,
                    "timestamp": datetime.now().isoformat(),
                    "agent": "reflecty"
                }
            }
            result = self._request("POST", "/memories", data=payload, timeout=15)
            return result is not None
        except Mem0ConnectionError:
            self.fallback_mode = True
            return self._fallback_store(insight, metadata)
    
    def _fallback_store(self, insight: str, metadata: Dict) -> bool:
        """File-based storage fallback"""
        try:
            filename = f"insight_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(insight) % 10000:04d}.json"
            filepath = self.fallback_dir / filename
            
            data = {
                "content": insight,
                "metadata": metadata,
                "timestamp": datetime.now().isoformat(),
                "user_id": self.user_id
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"❌ Fallback storage failed: {e}")
            return False
    
    def get_memories(self, limit: int = 100) -> List[Dict]:
        """Hole alle Memories für den User"""
        if self.fallback_mode:
            return self._fallback_get_memories(limit)
        
        try:
            result = self._request("GET", "/memories", 
                                  params={"user_id": self.user_id, "limit": limit},
                                  timeout=10)
            return result.get("results", []) if result else []
        except Mem0ConnectionError:
            self.fallback_mode = True
            return self._fallback_get_memories(limit)
    
    def _fallback_get_memories(self, limit: int) -> List[Dict]:
        """Get memories from file fallback"""
        memories = []
        
        for file in sorted(self.fallback_dir.glob('*.json'), reverse=True)[:limit]:
            try:
                with open(file) as f:
                    memories.append(json.load(f))
            except Exception:
                continue
        
        return memories

# ═══════════════════════════════════════════════════════════════════
# PATTERN ANALYZER
# ═══════════════════════════════════════════════════════════════════

class PatternAnalyzer:
    """Kern-Logik für Pattern-Erkennung"""
    
    def __init__(self, smriti: SmritiClient):
        self.smriti = smriti
        self.patterns: List[Pattern] = []
        self.anti_patterns: List[AntiPattern] = []
    
    def analyze_session(self, messages: List[Dict]) -> AnalysisResult:
        """Analysiert eine Session auf Patterns"""
        print(f"🔍 Analysiere {len(messages)} Nachrichten...")
        
        self._detect_communication_patterns(messages)
        self._detect_behavioral_patterns(messages)
        self._detect_anti_patterns(messages)
        self._detect_quality_patterns(messages)
        
        insights = self._generate_insights()
        store_success = self._store_patterns_in_smriti()
        
        return AnalysisResult(
            patterns_found=len(self.patterns),
            anti_patterns_found=len(self.anti_patterns),
            patterns=[p.to_dict() for p in self.patterns],
            anti_patterns=[ap.to_dict() for ap in self.anti_patterns],
            insights=insights,
            timestamp=datetime.now().isoformat(),
            mem0_status="fallback" if self.smriti.fallback_mode else "connected",
            fallback_used=self.smriti.fallback_mode
        )
    
    def _detect_communication_patterns(self, messages: List[Dict]):
        """Erkennt Kommunikationsmuster"""
        quality_keywords = ["strategisch", "risiko", "entscheidung", "innovation", "system", 
                           "strategic", "risk", "decision", "innovation", "architecture"]
        quality_count = sum(1 for m in messages if any(kw in m.get("content", "").lower() for kw in quality_keywords))
        
        if quality_count >= 3:
            self.patterns.append(Pattern(
                pattern_id=self._hash("quality_focus"),
                pattern_type="communication",
                description="Hoher Anteil an strategischen/qualitäts-relevanten Begriffen",
                frequency=quality_count, confidence=0.85,
                examples=["Wort-Level-Trigger erkannt"],
                related_patterns=[],
                created_at=datetime.now().isoformat()
            ))
        
        tech_keywords = ["code", "api", "docker", "json", "script", "python", "javascript", "implement"]
        tech_count = sum(1 for m in messages if any(kw in m.get("content", "").lower() for kw in tech_keywords))
        
        if len(messages) > 0 and tech_count > len(messages) * 0.4:
            self.patterns.append(Pattern(
                pattern_id=self._hash("tech_heavy"),
                pattern_type="behavioral",
                description=f"Session mit hohem technischen Fokus ({tech_count}/{len(messages)} Nachrichten)",
                frequency=1, confidence=0.75,
                examples=["Code/Implementierung dominiert"],
                related_patterns=[],
                created_at=datetime.now().isoformat()
            ))
    
    def _detect_behavioral_patterns(self, messages: List[Dict]):
        """Erkennt Verhaltensmuster"""
        if len(messages) >= 2:
            self.patterns.append(Pattern(
                pattern_id=self._hash("session_length"),
                pattern_type="behavioral",
                description=f"Kontinuierliche Session mit {len(messages)} Nachrichten",
                frequency=len(messages), confidence=0.95,
                examples=["Aktiver Austausch ohne Unterbrechung"],
                related_patterns=[],
                created_at=datetime.now().isoformat()
            ))
        
        # Detect long messages pattern
        long_msgs = [m for m in messages if len(m.get("content", "")) > 500]
        if len(long_msgs) > len(messages) * 0.3:
            self.patterns.append(Pattern(
                pattern_id=self._hash("detailed_responses"),
                pattern_type="behavioral",
                description=f"Detaillierte Antworten ({len(long_msgs)} lange Nachrichten)",
                frequency=len(long_msgs), confidence=0.80,
                examples=["Präferenz für Tiefe vs. Kürze"],
                related_patterns=[],
                created_at=datetime.now().isoformat()
            ))
    
    def _detect_anti_patterns(self, messages: List[Dict]):
        """Erkennt Anti-Patterns"""
        user_msgs = [m for m in messages if m.get("role") == "user"]
        if len(user_msgs) >= 5:
            contents = [m.get("content", "")[:30].lower() for m in user_msgs]
            
            # Check for repetition
            seen = set()
            duplicates = []
            for c in contents:
                if c in seen:
                    duplicates.append(c)
                seen.add(c)
            
            if duplicates:
                self.anti_patterns.append(AntiPattern(
                    anti_pattern_id=self._hash("repeated_questions"),
                    description="Wiederholte ähnliche Anfragen ohne Kontext-Nutzung",
                    root_cause="Vorherige Erklärungen wurden nicht verarbeitet oder Memory nicht genutzt",
                    impact="medium",
                    mitigation="Memory-System explizit referenzieren vor Antwort; Kontext zusammenfassen",
                    depth=3,
                    occurrences=[{"timestamp": datetime.now().isoformat(), "context": f"{len(duplicates)} Wiederholungen erkannt"}],
                    created_at=datetime.now().isoformat()
                ))
    
    def _detect_quality_patterns(self, messages: List[Dict]):
        """Erkennt Qualitätsmuster"""
        # Check for reflection markers
        reflection_keywords = ["reflexion", "reflection", "denke", "überlege", "betrachte"]
        reflection_count = sum(1 for m in messages if any(kw in m.get("content", "").lower() for kw in reflection_keywords))
        
        if reflection_count >= 2:
            self.patterns.append(Pattern(
                pattern_id=self._hash("reflection_focus"),
                pattern_type="meta",
                description="Session mit expliziter Reflexion",
                frequency=reflection_count, confidence=0.90,
                examples=["Meta-Kognition erkannt"],
                related_patterns=[],
                created_at=datetime.now().isoformat()
            ))
    
    def _generate_insights(self) -> List[str]:
        """Generiert lesbare Insights"""
        insights = []
        for p in self.patterns:
            insights.append(f"Pattern: {p.description} (Konfidenz: {p.confidence:.0%})")
        for ap in self.anti_patterns:
            insights.append(f"Anti-Pattern: {ap.description} — {ap.root_cause}")
        return insights
    
    def _store_patterns_in_smriti(self) -> bool:
        """Speichert alle Patterns in Smriti"""
        success = True
        
        for p in self.patterns:
            if not self.smriti.store_insight(f"[PATTERN] {p.description}", {
                "pattern_id": p.pattern_id, "type": "pattern",
                "pattern_type": p.pattern_type, "confidence": p.confidence
            }):
                success = False
        
        for ap in self.anti_patterns:
            if not self.smriti.store_insight(f"[ANTI-PATTERN] {ap.description}", {
                "anti_pattern_id": ap.anti_pattern_id, "type": "anti_pattern",
                "impact": ap.impact, "depth": ap.depth
            }):
                success = False
        
        return success
    
    def _hash(self, content: str) -> str:
        return hashlib.md5(content.encode()).hexdigest()[:8]

# ═══════════════════════════════════════════════════════════════════
# CONTEXT MANAGER (P0/P1/P2 Hierarchical Loading)
# ═══════════════════════════════════════════════════════════════════

class ContextManager:
    """
    Verwaltet hierarchischen Kontext für Sessions
    
    P0: Immer laden (Core)
    P1: On-Demand (bei Trigger)
    P2: Search (semantisch)
    """
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace or WORKSPACE)
        self.max_p0_lines = 150
        
        # P0: Core files (always loaded)
        self.p0_files = [
            self.workspace / 'SOUL.md',
            self.workspace / 'USER.md',
            self.workspace / 'AGENTS.md',
        ]
        
        # P1: On-demand files (by trigger)
        self.p1_files = {
            'strategisch': self.workspace / 'neuron' / 'core_mission.json',
            'fehler': self.workspace / 'neuron' / 'anti_patterns_v3.jsonl',
            'subagent': self.workspace / 'neuron' / 'subagent_factory.py',
            'heartbeat': self.workspace / 'neuron' / 'HEARTBEAT.md',
        }
    
    def get_core_context(self) -> str:
        """Lädt P0-Kontext (immer)"""
        parts = []
        total_lines = 0
        
        for file in self.p0_files:
            if file.exists():
                try:
                    with open(file) as f:
                        content = f.read()
                        lines = content.count('\n')
                        
                        # Compress if over limit
                        if total_lines + lines > self.max_p0_lines:
                            allowed = self.max_p0_lines - total_lines
                            content = self._compress_content(content, allowed)
                            lines = allowed
                        
                        parts.append(f"\n\n=== {file.name} ===\n\n{content}")
                        total_lines += lines
                        
                except Exception as e:
                    parts.append(f"\n\n=== {file.name} ===\n\n[Error: {e}]")
        
        return '\n'.join(parts)
    
    def load_on_demand(self, trigger: str) -> Optional[str]:
        """Lädt P1-Kontext bei Trigger"""
        if trigger in self.p1_files:
            file = self.p1_files[trigger]
            if file.exists():
                try:
                    with open(file) as f:
                        return f.read()
                except Exception:
                    pass
        return None
    
    def search_memory(self, query: str, max_results: int = 3) -> List[Dict]:
        """Semantische Suche in MEMORY.md"""
        results = []
        memory_file = self.workspace / 'MEMORY.md'
        
        if memory_file.exists():
            try:
                with open(memory_file) as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if query.lower() in line.lower():
                                start = max(0, i - 2)
                                end = min(len(lines), i + 3)
                                context = '\n'.join(lines[start:end])
                                results.append({
                                    'source': 'MEMORY.md',
                                    'context': context,
                                    'line': i
                                })
                                if len(results) >= max_results:
                                    break
            except Exception:
                pass
        
        return results
    
    def _compress_content(self, content: str, max_lines: int) -> str:
        """Komprimiert Inhalt auf max_lines"""
        lines = content.split('\n')
        
        if len(lines) <= max_lines:
            return content
        
        # Strategy: Header + Essence + Footer
        header_lines = lines[:20]
        footer_lines = lines[-10:]
        
        # Middle: Only important lines
        middle = [l for l in lines[20:-10] if l.strip() and not l.strip().startswith('#')]
        
        middle_budget = max_lines - len(header_lines) - len(footer_lines) - 5
        
        if len(middle) > middle_budget:
            middle = middle[:middle_budget]
            middle.append("\n... [gekürzt] ...\n")
        
        return '\n'.join(header_lines + middle + footer_lines)
    
    def get_context_report(self) -> str:
        """Zeigt aktuellen Kontext-Status"""
        lines = [
            "╔════════════════════════════════════════════════════════════╗",
            "║  REFLECTY CONTEXT MANAGER                                  ║",
            "╚════════════════════════════════════════════════════════════╝",
            "",
            f"P0 (Always): {len(self.p0_files)} files",
            f"P1 (On-Demand): {len(self.p1_files)} triggers",
            f"Max P0 Lines: {self.max_p0_lines}",
            "",
            "P1 Triggers:"
        ]
        
        for trigger, file in self.p1_files.items():
            exists = "✅" if file.exists() else "❌"
            lines.append(f"  {exists} {trigger} → {file.name}")
        
        lines.append("")
        return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Reflecty v2.0 — Pattern Mining Agent")
    parser.add_argument("--mode", choices=["analyze", "daily_synthesis", "test"], 
                       default="test", help="Betriebsmodus")
    parser.add_argument("--session", type=str, help="Session Key zu analysieren")
    parser.add_argument("--output", type=str, default="stdout", 
                       help="Output: stdout oder file path")
    parser.add_argument("--mem0-url", type=str, default=MEM0_URL,
                       help="mem0 URL (default: env SMRITI_MEM0_URL or http://localhost:8000)")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🧠 REFLECTY v2.0 — Pattern Mining Agent")
    print("=" * 60)
    print(f"   Workspace: {WORKSPACE}")
    print(f"   mem0 URL: {args.mem0_url}")
    print(f"   User ID: {USER_ID}")
    
    smriti = SmritiClient(base_url=args.mem0_url, user_id=USER_ID)
    
    # Connection status
    print(f"\n📡 Verbinde mit Smriti...")
    if smriti.fallback_mode:
        print(f"   ⚠️  Using file fallback (mem0 unavailable)")
    else:
        print(f"   ✅ Connected to mem0")
    
    if args.mode == "test":
        print("\n🧪 TEST-MODUS: Simulierte Session-Analyse")
        
        test_messages = [
            {"role": "user", "content": "Können wir das Memory-System verbessern?", "timestamp": "2026-03-10T18:00:00"},
            {"role": "assistant", "content": "Ja, Smriti hat 4 Ebenen...", "timestamp": "2026-03-10T18:01:00"},
            {"role": "user", "content": "Was ist mit der Performance?", "timestamp": "2026-03-10T18:02:00"},
            {"role": "assistant", "content": "Die Embedding-Latenz ist bei 3-5s...", "timestamp": "2026-03-10T18:03:00"},
            {"role": "user", "content": "Können wir das optimieren?", "timestamp": "2026-03-10T18:04:00"},
            {"role": "assistant", "content": "Ja, wir könnten Redis als Cache hinzufügen.", "timestamp": "2026-03-10T18:05:00"},
            {"role": "user", "content": "Strategisch gesehen, lohnt sich das?", "timestamp": "2026-03-10T18:06:00"},
        ]
        
        analyzer = PatternAnalyzer(smriti)
        result = analyzer.analyze_session(test_messages)
        
        print(f"\n📊 ERGEBNIS:")
        print(f"   Patterns gefunden: {result.patterns_found}")
        print(f"   Anti-Patterns gefunden: {result.anti_patterns_found}")
        print(f"   Storage: {result.mem0_status}")
        
        if result.insights:
            print(f"\n💡 Insights:")
            for insight in result.insights:
                print(f"   • {insight}")
        
        output_json = json.dumps(result.__dict__, indent=2, ensure_ascii=False, default=str)
        
        if args.output == "stdout":
            print(f"\n📄 Vollständige Analyse:")
            print(output_json[:2000] + "..." if len(output_json) > 2000 else output_json)
        else:
            with open(args.output, 'w') as f:
                f.write(output_json)
            print(f"\n✅ Gespeichert in: {args.output}")
    
    elif args.mode == "analyze" and args.session:
        print(f"\n🔍 Analysiere Session: {args.session}")
        print("   (OpenClaw Session-History Integration erforderlich)")
        print("   Hinweis: Verwende --mode test für Demo-Daten")
    
    elif args.mode == "daily_synthesis":
        print("\n📅 Tägliche Synthese...")
        memories = smriti.get_memories(limit=100)
        print(f"   {len(memories)} Memories geladen")
        print("   (Multi-Session Aggregation würde hier laufen)")
    
    elif args.mode == "context":
        print("\n🧠 Context Management...")
        cm = ContextManager()
        print(cm.get_context_report())
        print("\n" + "=" * 60)
        print("P0 Core Context (erste 500 Zeichen):")
        print("=" * 60)
        core = cm.get_core_context()
        print(core[:500] + "...")
    
    print("\n" + "=" * 60)
    print("✅ Reflecty abgeschlossen")
    print("=" * 60)
    return 0

if __name__ == "__main__":
    try:
        exit(main())
    except SmritiError as e:
        print(f"\n❌ Reflecty Error: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
