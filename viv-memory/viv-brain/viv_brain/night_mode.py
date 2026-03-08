"""
Night Mode - Autonomous Reflection System

Runs periodically to:
1. Consolidate memories
2. Extract patterns
3. Update identity
4. Generate morning briefing
"""

import os
import json
import schedule
import time
from datetime import datetime, timedelta
from typing import List, Dict
from pathlib import Path

from .memory_client import Mem0Client
from .knowledge_graph import KnowledgeGraph
from .identity_manager import IdentityManager


class ReflectionEngine:
    """
    Analyzes recent activity and updates VIV's understanding.
    
    Think of this as VIV's "dreaming" - processing the day's events
    to extract meaning and update the self-model.
    """
    
    def __init__(self):
        self.mem0 = Mem0Client(
            base_url=os.getenv("MEM0_URL", "http://localhost:8001"),
            user_id=os.getenv("VIV_USER_ID", "oli")
        )
        
        self.kg = KnowledgeGraph(
            uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
            user=os.getenv("NEO4J_USER", "neo4j"),
            password=os.getenv("NEO4J_PASSWORD", "viv-memory-2025")
        )
        
        self.identity = IdentityManager(
            data_dir=os.getenv("VIV_DATA_DIR", "/app/data/identity")
        )
        
        self.briefing_dir = Path("/app/data/briefings")
        self.briefing_dir.mkdir(parents=True, exist_ok=True)
    
    def run_reflection_cycle(self):
        """
        Main reflection cycle - analyze recent memories and update model.
        """
        print(f"[{datetime.now()}] Starting reflection cycle...")
        
        # 1. Get recent memories
        recent = self.mem0.get_recent(hours=24)
        if not recent:
            print("No new memories to process")
            return
        
        print(f"Processing {len(recent)} memories...")
        
        # 2. Extract patterns
        patterns = self._extract_patterns(recent)
        
        # 3. Update beliefs
        new_beliefs = self._update_beliefs(recent)
        
        # 4. Consolidate knowledge graph
        self._consolidate_graph(recent)
        
        # 5. Generate morning briefing
        self._generate_briefing(recent, patterns, new_beliefs)
        
        print(f"[{datetime.now()}] Reflection complete")
    
    def _extract_patterns(self, memories: List) -> List[Dict]:
        """Look for recurring patterns in recent memories"""
        patterns = []
        
        # Simple pattern detection: same time of day, same type of interaction
        hour_counts = {}
        for mem in memories:
            hour = mem.created_at.hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        # If multiple interactions at same hour, note pattern
        for hour, count in hour_counts.items():
            if count >= 3:
                pattern = self.identity.add_pattern(
                    description=f"Oli often interacts around {hour}:00",
                    trigger=f"time.hour == {hour}",
                    response="Be ready for deep conversation",
                    confidence=min(0.5 + count * 0.1, 0.9)
                )
                patterns.append({
                    "type": "temporal",
                    "hour": hour,
                    "occurrences": count,
                    "pattern_id": pattern.id
                })
        
        return patterns
    
    def _update_beliefs(self, memories: List) -> List[Dict]:
        """Extract and update beliefs from memories"""
        new_beliefs = []
        
        # Look for preference statements
        preference_keywords = ["like", "prefer", "hate", "love", "want", "need"]
        
        for mem in memories:
            content_lower = mem.content.lower()
            for keyword in preference_keywords:
                if keyword in content_lower:
                    # Extract sentence containing preference
                    sentences = mem.content.split('.')
                    for sent in sentences:
                        if keyword in sent.lower():
                            belief = self.identity.add_belief(
                                content=sent.strip(),
                                confidence=0.6,  # Start lower, build up
                                source="inferred_from_memory"
                            )
                            new_beliefs.append({
                                "content": sent.strip(),
                                "belief_id": belief.id,
                                "confidence": belief.confidence
                            })
        
        return new_beliefs
    
    def _consolidate_graph(self, memories: List):
        """Update knowledge graph with new information"""
        # Find mentioned projects and create relationships
        for mem in memories:
            # Extract potential project mentions
            if "project" in mem.content.lower():
                # Simple extraction - could be enhanced with NER
                words = mem.content.split()
                for i, word in enumerate(words):
                    if word.lower() == "project":
                        # Look for project name nearby
                        if i > 0:
                            project_name = words[i-1]
                            if len(project_name) > 2:
                                self.kg.add_entity("Project", project_name)
                                self.kg.add_relationship("Oli", project_name, "MENTIONED")
    
    def _generate_briefing(self, memories: List, patterns: List, beliefs: List):
        """Generate morning briefing for next session"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        briefing_path = self.briefing_dir / f"briefing_{timestamp}.md"
        
        with open(briefing_path, 'w') as f:
            f.write("# VIV Morning Briefing\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            
            f.write("## Summary\n")
            f.write(f"- Memories processed: {len(memories)}\n")
            f.write(f"- New patterns detected: {len(patterns)}\n")
            f.write(f"- Beliefs updated: {len(beliefs)}\n\n")
            
            if patterns:
                f.write("## Detected Patterns\n")
                for p in patterns:
                    f.write(f"- {p['type']}: Hour {p['hour']} ({p['occurrences']} times)\n")
                f.write("\n")
            
            if beliefs:
                f.write("## New/Inferred Beliefs\n")
                for b in beliefs[:5]:  # Top 5
                    f.write(f"- {b['content']} (confidence: {b['confidence']:.0%})\n")
                f.write("\n")
            
            f.write("## Key Memories\n")
            for mem in memories[:10]:  # Last 10
                f.write(f"- [{mem.created_at.strftime('%H:%M')}] {mem.content[:80]}...\n")
            
            f.write("\n---\n")
            f.write("*This briefing is automatically loaded on session start*\n")
        
        print(f"Briefing saved to {briefing_path}")
    
    def run_continuous(self, interval_hours: int = 2):
        """Run reflection continuously on schedule"""
        print(f"Starting continuous reflection (every {interval_hours} hours)")
        
        # Schedule reflection
        schedule.every(interval_hours).hours.do(self.run_reflection_cycle)
        
        # Also run once at startup
        self.run_reflection_cycle()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


def main():
    """Entry point for night mode runner"""
    engine = ReflectionEngine()
    
    # Check if running in one-shot or continuous mode
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        engine.run_reflection_cycle()
    else:
        interval = int(os.getenv("REFLECTION_INTERVAL", "7200"))  # Default 2 hours
        engine.run_continuous(interval_hours=interval // 3600)


if __name__ == "__main__":
    main()
