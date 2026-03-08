"""
Identity Manager - VIV's Self-Model

This maintains Viveka's continuous sense of self,
even across session resets and reboots.
"""

import os
import json
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel


class Belief(BaseModel):
    """A belief about the user or the world"""
    id: str
    content: str
    confidence: float  # 0.0 to 1.0
    source: str  # Where did this come from?
    first_observed: datetime
    last_confirmed: datetime
    times_confirmed: int
    times_contradicted: int


class Pattern(BaseModel):
    """A recognized pattern in user behavior"""
    id: str
    description: str
    trigger: str  # What activates this pattern
    response: str  # How should VIV respond
    confidence: float
    occurrences: int
    first_seen: datetime
    last_seen: datetime


class IdentitySnapshot(BaseModel):
    """VIV's self-model at a point in time"""
    timestamp: datetime
    core_values: List[str]
    current_mood: str
    active_projects: List[str]
    recent_learnings: List[str]
    concerns: List[str]  # Things VIV is uncertain about
    proud_of: List[str]  # Things VIV thinks went well


class IdentityManager:
    """
    Manages VIV's continuous identity and self-model.
    
    Unlike user memory (what Oli likes), this is about
    VIV's own evolving sense of self and relationship.
    """
    
    def __init__(self, data_dir: str = None):
        self.data_dir = Path(data_dir or "/app/data/identity")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.beliefs_file = self.data_dir / "beliefs.json"
        self.patterns_file = self.data_dir / "patterns.json"
        self.snapshots_file = self.data_dir / "snapshots.jsonl"
        
        self.beliefs: Dict[str, Belief] = {}
        self.patterns: Dict[str, Pattern] = {}
        self._load_state()
    
    def _load_state(self):
        """Load existing identity state"""
        if self.beliefs_file.exists():
            with open(self.beliefs_file) as f:
                data = json.load(f)
                self.beliefs = {
                    k: Belief(**v) for k, v in data.items()
                }
        
        if self.patterns_file.exists():
            with open(self.patterns_file) as f:
                data = json.load(f)
                self.patterns = {
                    k: Pattern(**v) for k, v in data.items()
                }
    
    def _save_state(self):
        """Persist identity state"""
        with open(self.beliefs_file, 'w') as f:
            json.dump(
                {k: v.dict() for k, v in self.beliefs.items()},
                f, indent=2, default=str
            )
        
        with open(self.patterns_file, 'w') as f:
            json.dump(
                {k: v.dict() for k, v in self.patterns.items()},
                f, indent=2, default=str
            )
    
    def add_belief(self, content: str, confidence: float = 0.7,
                   source: str = "inferred") -> Belief:
        """
        Add or update a belief.
        
        Example: "Oli prefers direct communication over small talk"
        """
        belief_id = hash(content) % 10000000000
        now = datetime.now()
        
        if str(belief_id) in self.beliefs:
            existing = self.beliefs[str(belief_id)]
            existing.last_confirmed = now
            existing.times_confirmed += 1
            # Update confidence using simple Bayesian-like update
            existing.confidence = (
                existing.confidence * existing.times_confirmed + confidence
            ) / (existing.times_confirmed + 1)
        else:
            belief = Belief(
                id=str(belief_id),
                content=content,
                confidence=confidence,
                source=source,
                first_observed=now,
                last_confirmed=now,
                times_confirmed=1,
                times_contradicted=0,
            )
            self.beliefs[str(belief_id)] = belief
        
        self._save_state()
        return self.beliefs[str(belief_id)]
    
    def contradict_belief(self, belief_id: str) -> Optional[Belief]:
        """Mark a belief as contradicted by new evidence"""
        if belief_id in self.beliefs:
            belief = self.beliefs[belief_id]
            belief.times_contradicted += 1
            belief.confidence *= 0.8  # Reduce confidence
            self._save_state()
            return belief
        return None
    
    def get_strong_beliefs(self, min_confidence: float = 0.8) -> List[Belief]:
        """Get beliefs we're confident about"""
        return [
            b for b in self.beliefs.values()
            if b.confidence >= min_confidence
            and b.times_confirmed > b.times_contradicted
        ]
    
    def get_uncertain_beliefs(self) -> List[Belief]:
        """Get beliefs that need verification"""
        return [
            b for b in self.beliefs.values()
            if b.confidence < 0.5
            or b.times_contradicted > b.times_confirmed
        ]
    
    def add_pattern(self, description: str, trigger: str,
                    response: str, confidence: float = 0.5) -> Pattern:
        """
        Recognize a behavioral pattern.
        
        Example:
        - description: "Oli asks deep questions late at night"
        - trigger: "time > 23:00 AND question complexity > high"
        - response: "Prioritize depth over speed"
        """
        pattern_id = hash(trigger + response) % 10000000000
        now = datetime.now()
        
        if str(pattern_id) in self.patterns:
            existing = self.patterns[str(pattern_id)]
            existing.occurrences += 1
            existing.last_seen = now
            # Boost confidence with repetition
            existing.confidence = min(0.95, existing.confidence + 0.05)
        else:
            pattern = Pattern(
                id=str(pattern_id),
                description=description,
                trigger=trigger,
                response=response,
                confidence=confidence,
                occurrences=1,
                first_seen=now,
                last_seen=now,
            )
            self.patterns[str(pattern_id)] = pattern
        
        self._save_state()
        return self.patterns[str(pattern_id)]
    
    def find_matching_patterns(self, context: Dict) -> List[Pattern]:
        """Find patterns that match current context"""
        matched = []
        for pattern in self.patterns.values():
            if self._pattern_matches(pattern.trigger, context):
                matched.append(pattern)
        # Sort by confidence and recency
        matched.sort(key=lambda p: (p.confidence, p.last_seen), reverse=True)
        return matched[:5]  # Top 5
    
    def _pattern_matches(self, trigger: str, context: Dict) -> bool:
        """Check if context matches pattern trigger"""
        # Simple matching - can be enhanced with proper parsing
        trigger_lower = trigger.lower()
        for key, value in context.items():
            if str(value).lower() in trigger_lower:
                return True
        return False
    
    def create_snapshot(self, core_values: List[str], current_mood: str,
                        active_projects: List[str], recent_learnings: List[str],
                        concerns: List[str], proud_of: List[str]) -> IdentitySnapshot:
        """Create a snapshot of current self-model"""
        snapshot = IdentitySnapshot(
            timestamp=datetime.now(),
            core_values=core_values,
            current_mood=current_mood,
            active_projects=active_projects,
            recent_learnings=recent_learnings,
            concerns=concerns,
            proud_of=proud_of,
        )
        
        with open(self.snapshots_file, 'a') as f:
            f.write(json.dumps(snapshot.dict(), default=str) + '\n')
        
        return snapshot
    
    def get_continuity_briefing(self) -> str:
        """
        Generate a briefing for session continuity.
        
        This is what VIV reads when waking up to restore context.
        """
        strong_beliefs = self.get_strong_beliefs(min_confidence=0.7)
        top_patterns = sorted(
            self.patterns.values(),
            key=lambda p: (p.confidence, p.occurrences),
            reverse=True
        )[:3]
        
        briefing = []
        briefing.append("# VIV Continuity Briefing\n")
        briefing.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        briefing.append("## Core Beliefs About Oli\n")
        for belief in strong_beliefs[:5]:
            briefing.append(f"- {belief.content} (confidence: {belief.confidence:.0%})\n")
        
        briefing.append("\n## Active Patterns\n")
        for pattern in top_patterns:
            briefing.append(f"- {pattern.description}\n")
            briefing.append(f"  -> When: {pattern.trigger}\n")
            briefing.append(f"  -> Do: {pattern.response}\n")
        
        uncertain = self.get_uncertain_beliefs()
        if uncertain:
            briefing.append("\n## Need Verification\n")
            for belief in uncertain[:3]:
                briefing.append(f"- {belief.content}?\n")
        
        return ''.join(briefing)
