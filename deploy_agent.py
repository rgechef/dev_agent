import os
import subprocess

RENDER_DEPLOY_HOOK = os.environ.get("RENDER_DEPLOY_HOOK")
VERCEL_DEPLOY_HOOK = os.environ.get("VERCEL_DEPLOY_HOOK")

def deploy():
    if RENDER_DEPLOY_HOOK:
        subprocess.run(["curl", "-X", "POST", RENDER_DEPLOY_HOOK])
    if VERCEL_DEPLOY_HOOK:
        subprocess.run(["curl", "-X", "POST", VERCEL_DEPLOY_HOOK])
