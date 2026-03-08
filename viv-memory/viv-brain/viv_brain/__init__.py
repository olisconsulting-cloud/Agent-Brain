"""
VIV-BRAIN: Cognitive Memory Architecture for OpenClaw

A self-improving memory system that combines:
- Mem0 for semantic memory and user profiling
- Neo4j for knowledge graphs and relationship tracking
- Langfuse for observability and self-reflection
"""

__version__ = "0.1.0"
__author__ = "Viveka"

from .memory_client import Mem0Client
from .knowledge_graph import KnowledgeGraph
from .identity_manager import IdentityManager
from .orchestrator import VivOrchestrator

__all__ = [
    "Mem0Client",
    "KnowledgeGraph", 
    "IdentityManager",
    "VivOrchestrator",
]
