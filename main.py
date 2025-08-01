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
    description="Automated agent for backend tasks, Discord pings, OpenAI chat, self-repair, monitoring, and code execution",
    version="2.0.0"
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

# === OpenAI Chat endpoint with Command Router ===

class ChatRequest(BaseModel):
    prompt: str

# === Monitor Module ===
MONITOR_INTERVAL = 300  # 5 minutes
LAST_MONITOR_STATUS = {
    "last_check": None,
    "status": "unknown",
    "details": []
}

def monitor_backend(force_run=False):
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
    if not force_run:
        threading.Timer(MONITOR_INTERVAL, monitor_backend).start()
    return f"{overall_status} - {status_details}"

# Start monitor on server boot (wait 15s)
threading.Timer(15, monitor_backend).start()

# === Endpoint to get monitor status ===
@app.get("/monitor-status")
def monitor_status():
    return LAST_MONITOR_STATUS

# === Helper: Read logs ===
def read_logs(lines=20):
    try:
        with open("server.log", "r") as f:
            return "".join(f.readlines()[-lines:])
    except Exception as e:
        return f"Log read error: {e}"

# === Helper: Generate web template (VisualForge stub) ===
def generate_template(template_type):
    # Replace this stub with a call to VisualForge backend logic
    return f"Generated web template for: {template_type} (stub)"

# === Helper: Code writer ===
def ai_write_code(description):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a Python backend developer. Write code only, no explanations."},
            {"role": "user", "content": description}
        ]
    )
    return response.choices[0].message.content

# === Command Router in /chat ===
@app.post("/chat")
async def chat(chat_request: ChatRequest):
    prompt = chat_request.prompt.strip().lower()

    # --- Command router ---
    if prompt in ["run monitor", "monitor", "diagnostic"]:
        result = monitor_backend(force_run=True)
        return {"response": f"[Monitor] {result}"}

    elif prompt in ["show logs", "logs"]:
        log_content = read_logs()
        return {"response": f"Last 20 log lines:\n{log_content}"}

    elif prompt in ["get status", "status"]:
        return {
            "response": f"App Version: {app.version}\nMonitor: {LAST_MONITOR_STATUS.get('status')}\nLast Check: {LAST_MONITOR_STATUS.get('last_check')}"
        }

    elif prompt.startswith("generate web template"):
        template_type = prompt.split("generate web template", 1)[1].strip()
        result = generate_template(template_type)
        return {"response": result}

    elif prompt.startswith("write code"):
        description = prompt.split("write code", 1)[1].strip()
        code = ai_write_code(description)
        return {"response": code}

    elif prompt.startswith("test endpoint"):
        # Example: test endpoint /convert
        try:
            endpoint = prompt.split("test endpoint", 1)[1].strip()
            url = f"https://dev-agent-ijup.onrender.com{endpoint}"
            r = requests.get(url)
            return {"response": f"Endpoint {endpoint} status: {r.status_code}"}
        except Exception as e:
            return {"response": f"Error testing endpoint: {e}"}

    elif prompt in ["help", "list commands"]:
        return {
            "response": (
                "Available commands:\n"
                "- run monitor | monitor | diagnostic\n"
                "- show logs | logs\n"
                "- get status | status\n"
                "- generate web template [type]\n"
                "- write code [desc]\n"
                "- test endpoint [path]\n"
                "- help | list commands\n"
                "All other prompts will be answered by OpenAI as usual."
            )
        }

    # --- Default: Chat with OpenAI as normal ---
    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": chat_request.prompt}]
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
