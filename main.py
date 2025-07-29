from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI(title="Dev Agent API")

# Allow all origins for demo; restrict for production!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/agent/build")
async def build_agent(request: Request):
    data = await request.json()
    feature_desc = data.get("feature_desc", "")
    if not feature_desc:
        return JSONResponse({"error": "Missing feature_desc"}, status_code=400)
    try:
        result = subprocess.run(
            ["python", "chat_cli.py"],
            input=feature_desc.encode(),
            capture_output=True, timeout=300
        )
        return {
            "status": "ok",
            "stdout": result.stdout.decode(),
            "stderr": result.stderr.decode()
        }
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/")
async def root():
    return {"status": "Dev Agent API Running"}
