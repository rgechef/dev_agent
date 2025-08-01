import os
import requests
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import threading
import time

app = FastAPI(
    title="Dev Agent",
    description="Automated agent for backend tasks, Discord pings, OpenAI chat, self-repair, and auto-monitoring",
    version="1.1.0"
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

# === OpenAI Chat endpoint with Pydantic model for Swagger ===

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
async def chat(chat_request: ChatRequest):
    prompt = chat_request.prompt
    if not prompt:
        return {"error": "No prompt provided."}
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or "gpt-4o" if you have access
            messages=[{"role": "user", "content": prompt}]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

# === Monitor Module ===

MONITOR_INTERVAL = 300  # Every 5 minutes (in seconds)
LAST_MONITOR_STATUS = {
    "last_check": None,
    "status": "unknown",
    "details": []
}

def monitor_backend():
    global LAST_MONITOR_STATUS
    status_details = []
    success = True
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Check root endpoint
        r = requests.get("https://dev-agent-ijup.onrender.com/")
        if r.status_code == 200:
            status_details.append(f"/ OK [{r.status_code}]")
        else:
            status_details.append(f"/ FAIL [{r.status_code}]")
            send_discord_ping(f"❌ Dev Agent root endpoint FAILED! [{r.status_code}]")
            success = False

        # Check /chat endpoint
        r = requests.post("https://dev-agent-ijup.onrender.com/chat", json={"prompt": "ping"})
        if r.status_code == 200 and "response" in r.json():
            status_details.append("/chat OK")
        else:
            status_details.append(f"/chat FAIL [{r.status_code}]")
            send_discord_ping("❌ /chat endpoint FAILED!")
            success = False

        # Optional: Check /convert (uncomment & add sample file path if desired)
        # with open("test.png", "rb") as f:
        #     files = {'file': f}
        #     r = requests.post("https://dev-agent-ijup.onrender.com/convert", files=files)
        #     if r.status_code == 200 and "download_url" in r.json():
        #         status_details.append("/convert OK")
        #     else:
        #         status_details.append(f"/convert FAIL [{r.status_code}]")
        #         send_discord_ping("❌ /convert endpoint FAILED!")
        #         success = False

        overall_status = "OK" if success else "FAIL"
        print(f"[Monitor] {now}: {overall_status} - {status_details}")
        LAST_MONITOR_STATUS = {
            "last_check": now,
            "status": overall_status,
            "details": status_details
        }
    except Exception as e:
        send_discord_ping(f"❌ Monitor exception: {e}")
        LAST_MONITOR_STATUS = {
            "last_check": now,
            "status": "EXCEPTION",
            "details": [str(e)]
        }
    # Schedule next check
    threading.Timer(MONITOR_INTERVAL, monitor_backend).start()

# Start monitor on server boot (wait 15s to avoid race with server start)
threading.Timer(15, monitor_backend).start()

# === Endpoint to get monitor status ===
@app.get("/monitor-status")
def monitor_status():
    return LAST_MONITOR_STATUS
