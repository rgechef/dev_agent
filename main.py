import os
import requests
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
import openai

app = FastAPI(
    title="Dev Agent",
    description="Automated agent for backend tasks, Discord pings, OpenAI chat, and self-repair",
    version="1.0.0"
)

# === CORS configuration ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Discord ping logic ===
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_ping(message: str):
    if DISCORD_WEBHOOK_URL:
        try:
            requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        except Exception as e:
            print("Ping failed:", e)

@app.get("/test-ping")
def test_ping(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_discord_ping, "✅ Dev Agent: Ping test — agent is live and automated!")
    return {"status": "Ping sent (check Discord channel)"}

# === Root endpoint (health check) ===
@app.get("/")
def read_root():
    return {"status": "Dev Agent is running"}

# === OpenAI Chat endpoint ===
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    if not prompt:
        return {"error": "No prompt provided."}
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4o" if you have access
            messages=[{"role": "user", "content": prompt}]
        )
        return {"response": completion['choices'][0]['message']['content']}
    except Exception as e:
        return {"error": str(e)}
