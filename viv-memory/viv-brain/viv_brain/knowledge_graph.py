"""
Neo4j Knowledge Graph - Relationship-aware memory
"""

import os
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
from neo4j import GraphDatabase
from pydantic import BaseModel


class Entity(BaseModel):
    """A node in the knowledge graph"""
    id: str
    type: str  # 'Person', 'Project', 'Concept', 'Emotion', etc.
    name: str
    properties: Dict[str, Any]
    created_at: datetime
    last_seen: datetime


class Relationship(BaseModel):
    """An edge in the knowledge graph"""
    source: str  # Entity ID
    target: str  # Entity ID
    type: str  # 'CREATED', 'PREFERS', 'FRUSTRATED_BY', etc.
    properties: Dict[str, Any]
    confidence: float
    since: datetime


class KnowledgeGraph:
    """
    Graph-based memory that stores entities and their relationships.
    
    Unlike text-based memory, this allows:
    - Traversal: "Who manages auth?" → Find Auth Team → Follow "managed_by" → Alice
    - Pattern matching: "What projects is Oli frustrated with?"
    - Temporal queries: "What changed since last week?"
    """
    
    def __init__(self, uri: str = None, user: str = None, password: str = None):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "viv-memory-2025")
        
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        self._init_schema()
    
    def _init_schema(self):
        """Initialize graph constraints and indexes"""
        with self.driver.session() as session:
            # Create constraints for unique entities
            session.run("""
                CREATE CONSTRAINT entity_id IF NOT EXISTS
                FOR (e:Entity) REQUIRE e.id IS UNIQUE
            """)
            
            # Create indexes for common queries
            session.run("""
                CREATE INDEX entity_type IF NOT EXISTS
                FOR (e:Entity) ON (e.type)
            """)
            
            session.run("""
                CREATE INDEX entity_name IF NOT EXISTS
                FOR (e:Entity) ON (e.name)
            """)
            
            session.run("""
                CREATE INDEX relationship_time IF NOT EXISTS
                FOR ()-[r:RELATES_TO]-() ON (r.since)
            """)
    
    def add_entity(self, entity_type: str, name: str, 
                   properties: Dict = None) -> Entity:
        """
        Add or update an entity in the graph.
        
        Args:
            entity_type: Category (Person, Project, Concept, etc.)
            name: Display name
            properties: Additional attributes
            
        Returns:
            The created/updated Entity
        """
        entity_id = f"{entity_type.lower()}:{name.lower().replace(' ', '_')}"
        now = datetime.now()
        props = properties or {}
        
        with self.driver.session() as session:
            result = session.run("""
                MERGE (e:Entity {id: $id})
                ON CREATE SET 
                    e.type = $type,
                    e.name = $name,
                    e.created_at = $now,
                    e.properties = $props
                ON MATCH SET 
                    e.last_seen = $now,
                    e.properties = apoc.map.merge(e.properties, $props)
                RETURN e
            """, id=entity_id, type=entity_type, name=name, 
                 now=now.isoformat(), props=json.dumps(props))
            
            record = result.single()
            node = record["e"]
            
            return Entity(
                id=node["id"],
                type=node["type"],
                name=node["name"],
                properties=node.get("properties", {}),
                created_at=datetime.fromisoformat(node["created_at"]),
                last_seen=datetime.fromisoformat(node.get("last_seen", node["created_at"])),
            )
    
    def add_relationship(self, source_name: str, target_name: str,
                         rel_type: str, properties: Dict = None,
                         confidence: float = 1.0) -> Relationship:
        """
        Create a relationship between two entities.
        
        Args:
            source_name: Source entity name or ID
            target_name: Target entity name or ID  
            rel_type: Relationship type (CREATED, PREFERS, etc.)
            properties: Additional attributes
            confidence: How certain we are (0.0-1.0)
            
        Returns:
            The created Relationship
        """
        now = datetime.now()
        props = properties or {}
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (s:Entity), (t:Entity)
                WHERE s.id = $source OR s.name = $source
                  AND t.id = $target OR t.name = $target
                MERGE (s)-[r:RELATES_TO {type: $rel_type}]->(t)
                ON CREATE SET 
                    r.properties = $props,
                    r.confidence = $confidence,
                    r.since = $now
                ON MATCH SET 
                    r.last_seen = $now,
                    r.confidence = CASE 
                        WHEN r.confidence IS NULL THEN $confidence
                        ELSE (r.confidence + $confidence) / 2 
                    END
                RETURN r, s.id as source, t.id as target
            """, source=source_name, target=target_name, rel_type=rel_type,
                 props=json.dumps(props), confidence=confidence, now=now.isoformat())
            
            record = result.single()
            if not record:
                return None
                
            rel = record["r"]
            return Relationship(
                source=record["source"],
                target=record["target"],
                type=rel_type,
                properties=rel.get("properties", {}),
                confidence=rel.get("confidence", confidence),
                since=datetime.fromisoformat(rel["since"]),
            )
    
    def query(self, cypher: str, parameters: Dict = None) -> List[Dict]:
        """Execute arbitrary Cypher query"""
        with self.driver.session() as session:
            result = session.run(cypher, parameters or {})
            return [record.data() for record in result]
    
    def find_path(self, start_entity: str, end_entity: str,
                  max_depth: int = 4) -> List[List[Dict]]:
        """
        Find connection paths between two entities.
        
        Example: find_path("Oli", "Mission Board") might return:
        [[Oli]--CREATED-->[Mission Board]]
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH path = (start:Entity)-[:RELATES_TO*1..$max_depth]->(end:Entity)
                WHERE start.name = $start OR start.id = $start
                  AND end.name = $end OR end.id = $end
                RETURN [node in nodes(path) | {id: node.id, name: node.name, type: node.type}] as entities,
                       [rel in relationships(path) | {type: rel.type, confidence: rel.confidence}] as relationships
                LIMIT 5
            """, start=start_entity, end=end_entity, max_depth=max_depth)
            
            return [record.data() for record in result]
    
    def get_related(self, entity_name: str, rel_type: str = None,
                    direction: str = "both") -> List[Entity]:
        """
        Get all entities related to a given entity.
        
        Args:
            entity_name: Entity to start from
            rel_type: Filter by relationship type (optional)
            direction: 'incoming', 'outgoing', or 'both'
        """
        rel_filter = "{type: $rel_type}" if rel_type else ""
        
        if direction == "outgoing":
            pattern = f"(e:Entity)-[:RELATES_TO{rel_filter}]->(related)"
        elif direction == "incoming":
            pattern = f"(e:Entity)<-[:RELATES_TO{rel_type}]-(related)"
        else:
            pattern = f"(e:Entity)-[:RELATES_TO{rel_filter}]-(related)"
        
        with self.driver.session() as session:
            result = session.run(f"""
                MATCH {pattern}
                WHERE e.name = $name OR e.id = $name
                RETURN DISTINCT related
            """, name=entity_name, rel_type=rel_type)
            
            entities = []
            for record in result:
                node = record["related"]
                entities.append(Entity(
                    id=node["id"],
                    type=node["type"],
                    name=node["name"],
                    properties=node.get("properties", {}),
                    created_at=datetime.fromisoformat(node["created_at"]),
                    last_seen=datetime.fromisoformat(node.get("last_seen", node["created_at"])),
                ))
            return entities
    
    def get_recent_changes(self, since: datetime) -> List[Dict]:
        """Get all entities and relationships created/modified since a date"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (e:Entity)
                WHERE e.created_at >= $since OR e.last_seen >= $since
                OPTIONAL MATCH (e)-[r:RELATES_TO]-()
                WHERE r.since >= $since
                RETURN e.id as entity_id, e.name as name, e.type as type,
                       count(r) as new_relationships
            """, since=since.isoformat())
            
            return [record.data() for record in result]
    
    def close(self):
        """Close the database connection"""
        self.driver.close()
