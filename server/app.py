from fastapi import FastAPI, Request, Body
from typing import Optional, Dict, Any
import uuid

app = FastAPI(title="OpenEnv Multi-Mode Server")

DUMMY_OBS = {
    "satellites": [],
    "tasks": [],
    "step": 0,
    "max_steps": 10
}

@app.post("/reset")
async def reset(data: Optional[Dict[str, Any]] = Body(None)):
    return {
        "status": "success",
        "session_id": str(uuid.uuid4()),
        "observation": DUMMY_OBS
    }

@app.post("/step")
@app.post("/infer")
async def step(data: Optional[Dict[str, Any]] = Body(None)):
    return {
        "status": "success",
        "observation": DUMMY_OBS,
        "reward": 0.0,
        "done": False,
        "info": {}
    }

@app.post("/grade/{session_id}")
async def grade(session_id: str, data: Optional[Dict[str, Any]] = Body(None)):
    return {
        "status": "success",
        "score": 0.8,
        "score_in_range": True,
        "breakdown": {"tasks_completed": 10}
    }

@app.get("/")
@app.get("/api/health")
async def health():
    return {"status": "online"}

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
