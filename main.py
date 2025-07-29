
from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class BuildAgentRequest(BaseModel):
    feature: str

@app.post("/agent/build")
async def build_agent(request: BuildAgentRequest):
    # Do whatever you want with request.feature
    return {"message": f"Received: {request.feature}"}

@app.get("/")
async def root():
    return {"message": "Dev Agent is running!"}
