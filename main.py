from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only. For production, use your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class BuildAgentRequest(BaseModel):
    feature: str

@app.post("/agent/build")
async def build_agent(request: BuildAgentRequest):
    # This echoes the feature you send from Swagger UI
    return {"message": f"Received: {request.feature}"}

@app.get("/")
async def root():
    return {"status": "Dev Agent API Running"}
