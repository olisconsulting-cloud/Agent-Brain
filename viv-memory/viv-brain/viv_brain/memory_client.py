"""
Mem0 Client - Interface to self-improving memory layer
"""

import os
import json
from typing import List, Dict, Optional, Any
from datetime import datetime
import requests
from pydantic import BaseModel


class MemoryEntry(BaseModel):
    """A single memory entry from Mem0"""
    id: str
    content: str
    metadata: Dict[str, Any]
    created_at: datetime
    memory_type: str  # 'episodic', 'semantic', 'procedural'
    confidence: float
    

class Mem0Client:
    """
    Client for Mem0 memory layer.
    
    Mem0 automatically extracts:
    - User preferences ("Oli likes directness")
    - Facts ("Oli works on Mission Board")
    - Relationships ("Oli -> created -> Mission Board")
    """
    
    def __init__(self, base_url: str = None, user_id: str = "oli"):
        self.base_url = base_url or os.getenv("MEM0_URL", "http://localhost:8001")
        self.user_id = user_id
        self.session = requests.Session()
        
    def add(self, content: str, metadata: Dict = None, memory_type: str = "episodic") -> str:
        """
        Add a new memory. Mem0 will automatically extract entities and relationships.
        
        Args:
            content: The raw conversation/text to remember
            metadata: Additional context (emotion, project, etc.)
            memory_type: Type of memory being stored
            
        Returns:
            Memory ID
        """
        payload = {
            "messages": [{"role": "user", "content": content}],
            "user_id": self.user_id,
            "agent_id": "viveka",
            "metadata": metadata or {},
            "memory_type": memory_type,
        }
        
        response = self.session.post(
            f"{self.base_url}/v1/memories/",
            json=payload
        )
        response.raise_for_status()
        return response.json().get("id")
    
    def search(self, query: str, limit: int = 10) -> List[MemoryEntry]:
        """
        Semantic search across all memories.
        
        Args:
            query: Natural language query
            limit: Max results to return
            
        Returns:
            List of relevant memories with similarity scores
        """
        response = self.session.post(
            f"{self.base_url}/v1/memories/search/",
            json={
                "query": query,
                "user_id": self.user_id,
                "limit": limit,
            }
        )
        response.raise_for_status()
        
        results = []
        for item in response.json().get("results", []):
            results.append(MemoryEntry(
                id=item["id"],
                content=item["memory"],
                metadata=item.get("metadata", {}),
                created_at=datetime.fromisoformat(item["created_at"].replace("Z", "+00:00")),
                memory_type=item.get("memory_type", "episodic"),
                confidence=item.get("score", 0.5),
            ))
        return results
    
    def get_user_profile(self) -> Dict:
        """
        Get consolidated user profile.
        
        Returns all extracted preferences, facts, and traits about the user.
        """
        response = self.session.get(
            f"{self.base_url}/v1/users/{self.user_id}/"
        )
        response.raise_for_status()
        return response.json()
    
    def get_recent(self, hours: int = 24) -> List[MemoryEntry]:
        """Get memories from last N hours"""
        response = self.session.get(
            f"{self.base_url}/v1/memories/",
            params={
                "user_id": self.user_id,
                "start_date": (datetime.now() - __import__('datetime').timedelta(hours=hours)).isoformat(),
            }
        )
        response.raise_for_status()
        
        results = []
        for item in response.json().get("results", []):
            results.append(MemoryEntry(
                id=item["id"],
                content=item["memory"],
                metadata=item.get("metadata", {}),
                created_at=datetime.fromisoformat(item["created_at"].replace("Z", "+00:00")),
                memory_type=item.get("memory_type", "episodic"),
                confidence=item.get("score", 0.5),
            ))
        return results
    
    def delete(self, memory_id: str) -> bool:
        """Delete a specific memory"""
        response = self.session.delete(
            f"{self.base_url}/v1/memories/{memory_id}/"
        )
        return response.status_code == 204
    
    def update(self, memory_id: str, content: str) -> bool:
        """Update an existing memory"""
        response = self.session.patch(
            f"{self.base_url}/v1/memories/{memory_id}/",
            json={"memory": content}
        )
        return response.status_code == 200
