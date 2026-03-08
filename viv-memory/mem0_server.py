#!/usr/bin/env python3
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict
from mem0 import Memory
import uvicorn

app = FastAPI(title="Smriti Mem0 API")
mem0 = Memory.from_config({
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "temperature": 0.1
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "url": "http://localhost:6333"
        }
    }
})

class Message(BaseModel):
    role: str
    content: str

class MemoryInput(BaseModel):
    messages: List[Message]
    user_id: str = "oli"
    agent_id: str = "viveka"
    metadata: Optional[Dict] = None

@app.get("/health")
async def health():
    return {"status": "ok", "service": "mem0", "mode": "openai"}

@app.post("/v1/memories/")
async def add_memory(input: MemoryInput):
    try:
        result = mem0.add(
            messages=[{"role": m.role, "content": m.content} for m in input.messages],
            user_id=input.user_id,
            agent_id=input.agent_id,
            metadata=input.metadata
        )
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.post("/v1/memories/search/")
async def search_memories(query: str, user_id: str = "oli"):
    results = mem0.search(query=query, user_id=user_id)
    return {"status": "success", "data": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
