import os
from dotenv import load_dotenv
import subprocess

load_dotenv()  # This will load variables from .env in the same folder

vercel_hook = os.environ['VERCEL_DEPLOY_HOOK']
render_hook = os.environ['RENDER_DEPLOY_HOOK']

# Deploy to Vercel
subprocess.run(f'curl --ssl-no-revoke -X POST "{vercel_hook}"', shell=True)
# Deploy to Render
subprocess.run(f'curl --ssl-no-revoke -X POST "{render_hook}"', shell=True)
