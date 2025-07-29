import os
from dotenv import load_dotenv
import subprocess
from datetime import datetime

load_dotenv()

vercel_hook = os.environ['VERCEL_DEPLOY_HOOK']
render_hook = os.environ['RENDER_DEPLOY_HOOK']

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

log("Triggering Vercel deploy...")
result1 = subprocess.run(f'curl --ssl-no-revoke -X POST "{vercel_hook}"', shell=True, capture_output=True, text=True)
log(f"Vercel Response: {result1.stdout.strip() or result1.stderr.strip()}")

log("Triggering Render deploy...")
result2 = subprocess.run(f'curl --ssl-no-revoke -X POST "{render_hook}"', shell=True, capture_output=True, text=True)
log(f"Render Response: {result2.stdout.strip() or result2.stderr.strip()}")

log("Deploy agent finished!")
