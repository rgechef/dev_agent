import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

vercel_hook = os.environ['VERCEL_DEPLOY_HOOK']
render_hook = os.environ['RENDER_DEPLOY_HOOK']

print("Triggering Vercel deploy...")
result1 = subprocess.run(f'curl --ssl-no-revoke -X POST "{vercel_hook}"', shell=True, capture_output=True, text=True)
print("Vercel Response:", result1.stdout)

print("Triggering Render deploy...")
result2 = subprocess.run(f'curl --ssl-no-revoke -X POST "{render_hook}"', shell=True, capture_output=True, text=True)
print("Render Response:", result2.stdout)
