from fastapi import FastAPI, Request
import json

app = FastAPI(title="OpenEnv Minimal Inference API")

@app.post("/reset")
async def reset(request: Request):
    """
    OpenEnv reset endpoint. 
    Must work regardless of whether a body is provided.
    """
    try:
        # Gracefully handle body if present, but do not require it
        await request.json()
    except:
        pass
    
    return {"status": "success"}

@app.post("/infer")
@app.post("/step")
async def infer(request: Request):
    """
    OpenEnv inference/step endpoint.
    """
    return {"output": "ok", "status": "success"}

@app.get("/api/health")
@app.get("/")
async def health():
    return {"status": "online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
