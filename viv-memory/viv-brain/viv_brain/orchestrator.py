"""
VIV Orchestrator - The Central Brain

Coordinates Mem0, Neo4j, Identity, and Langfuse
into a unified cognitive system.
"""

import os
import json
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from pathlib import Path

from .memory_client import Mem0Client
from .knowledge_graph import KnowledgeGraph
from .identity_manager import IdentityManager


class SessionContext:
    """Context for the current session"""
    def __init__(self, user_id: str = "oli", agent_id: str = "viveka"):
        self.user_id = user_id
        self.agent_id = agent_id
        self.started_at = datetime.now()
        self.project = None
        self.emotional_state = None
        self.referenced_memories = []
        self.new_learnings = []


class VivOrchestrator:
    """
    Central orchestrator for VIV's cognitive architecture.
    
    This is the entry point. All memory operations go through here.
    """
    
    def __init__(self):
        # Initialize all memory layers
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
        
        self.session = SessionContext()
        
    def bootstrap(self) -> str:
        """
        Load continuity context at session start.
        
        This is called when VIV 'wakes up' - after /new or restart.
        Returns a briefing to inject into the system prompt.
        """
        parts = []
        
        # 1. Get user profile from Mem0
        try:
            profile = self.mem0.get_user_profile()
            parts.append("## User Profile\n")
            parts.append(json.dumps(profile, indent=2))
        except Exception as e:
            parts.append(f"# Note: User profile unavailable ({e})\n")
        
        # 2. Get identity briefing
        try:
            identity_briefing = self.identity.get_continuity_briefing()
            parts.append("\n" + identity_briefing)
        except Exception as e:
            parts.append(f"\n# Note: Identity briefing unavailable ({e})\n")
        
        # 3. Get recent memories
        try:
            recent = self.mem0.get_recent(hours=24)
            if recent:
                parts.append("\n## Recent Memories (24h)\n")
                for mem in recent[:5]:
                    parts.append(f"- {mem.content[:100]}...\n")
        except Exception as e:
            parts.append(f"\n# Note: Recent memories unavailable ({e})\n")
        
        # 4. Get active projects from knowledge graph
        try:
            projects = self.kg.get_related("Oli", rel_type="WORKS_ON")
            if projects:
                parts.append("\n## Active Projects\n")
                for proj in projects:
                    parts.append(f"- {proj.name}\n")
        except Exception:
            pass  # Silent fail for optional feature
        
        return ''.join(parts)
    
    def recall(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Multi-layer recall: semantic search + graph traversal.
        
        Args:
            query: What are we looking for?
            limit: Max results
            
        Returns:
            Combined results from all memory layers
        """
        results = []
        
        # Layer 1: Semantic search via Mem0
        try:
            mem_results = self.mem0.search(query, limit=limit)
            for mem in mem_results:
                results.append({
                    "source": "semantic_memory",
                    "content": mem.content,
                    "confidence": mem.confidence,
                    "timestamp": mem.created_at,
                    "type": mem.memory_type,
                })
        except Exception as e:
            print(f"Mem0 search error: {e}")
        
        # Layer 2: Graph traversal for relationships
        try:
            # Extract potential entity names from query
            words = query.lower().split()
            for word in words:
                if len(word) > 3:  # Skip short words
                    related = self.kg.get_related(word)
                    for entity in related[:3]:
                        results.append({
                            "source": "knowledge_graph",
                            "content": f"{word} is related to {entity.name} ({entity.type})",
                            "confidence": 0.7,
                            "timestamp": entity.last_seen,
                            "type": "relationship",
                        })
        except Exception as e:
            print(f"Graph search error: {e}")
        
        # Sort by confidence and recency
        results.sort(key=lambda x: (x["confidence"], x["timestamp"]), reverse=True)
        return results[:limit]
    
    def remember_interaction(self, user_input: str, viv_response: str,
                            metadata: Dict = None) -> Dict:
        """
        Store an interaction across all memory layers.
        
        Args:
            user_input: What Oli said
            viv_response: What VIV replied
            metadata: Additional context (emotion, project, etc.)
            
        Returns:
            Summary of what was stored
        """
        summary = {"stored": []}
        
        # Combine into one memory
        combined = f"Oli: {user_input}\nVIV: {viv_response}"
        
        # Layer 1: Store in Mem0 (semantic memory)
        try:
            mem_id = self.mem0.add(
                content=combined,
                metadata=metadata,
                memory_type="episodic"
            )
            summary["stored"].append(f"mem0:{mem_id}")
        except Exception as e:
            summary["mem0_error"] = str(e)
        
        # Layer 2: Extract entities and store in graph
        try:
            # Simple entity extraction (can be enhanced with NER)
            if metadata and "project" in metadata:
                self.kg.add_entity("Project", metadata["project"])
                self.kg.add_relationship(
                    "Oli", metadata["project"], "WORKS_ON"
                )
                summary["stored"].append(f"kg:project:{metadata['project']}")
            
            if metadata and "emotion" in metadata:
                self.kg.add_entity("Emotion", metadata["emotion"])
                self.kg.add_relationship(
                    "Oli", metadata["emotion"], "EXPERIENCED"
                )
        except Exception as e:
            summary["kg_error"] = str(e)
        
        # Layer 3: Update identity if we learned something
        try:
            # Look for explicit learning statements
            if "learned" in user_input.lower() or "prefer" in user_input.lower():
                belief = self.identity.add_belief(
                    content=combined,
                    confidence=0.8,
                    source="explicit"
                )
                summary["stored"].append(f"identity:belief:{belief.id}")
        except Exception as e:
            summary["identity_error"] = str(e)
        
        return summary
    
    def learn_pattern(self, description: str, trigger: str,
                     response: str) -> Dict:
        """Explicitly teach VIV a behavioral pattern"""
        pattern = self.identity.add_pattern(
            description=description,
            trigger=trigger,
            response=response,
            confidence=0.9
        )
        return {
            "pattern_id": pattern.id,
            "description": pattern.description,
            "confidence": pattern.confidence,
        }
    
    def contradict(self, belief_content: str) -> Dict:
        """Mark a belief as incorrect"""
        # Find belief by content hash
        belief_id = str(hash(belief_content) % 10000000000)
        result = self.identity.contradict_belief(belief_id)
        if result:
            return {
                "belief_id": belief_id,
                "new_confidence": result.confidence,
                "times_contradicted": result.times_contradicted,
            }
        return {"error": "Belief not found"}
    
    def get_morning_briefing(self) -> str:
        """Generate a morning briefing for continuity"""
        return self.bootstrap()
    
    def close(self):
        """Clean shutdown"""
        self.kg.close()


# Singleton instance
_orchestrator: Optional[VivOrchestrator] = None


def get_orchestrator() -> VivOrchestrator:
    """Get or create the singleton orchestrator"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = VivOrchestrator()
    return _orchestrator
