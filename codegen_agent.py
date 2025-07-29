from openai import OpenAI
import os

# Use your actual project directory path below:
PROJECT_DIR = "F:/code/3dshapesnap-ui2/3dshapesnap-ui2"  # <-- Edit if your path is different

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def codegen_chat(feature_desc):
    ai = OpenAI(api_key=OPENAI_API_KEY)
    prompt = (
        f"You are a senior software engineer and devops agent for a SaaS startup. "
        f"Given this feature request, write and modify the necessary code in our project. "
        f"Be safe, modular, do not break existing logic, and always explain your changes at the end. "
        f"Feature request:\n{feature_desc}\n\n"
        f"The project code is located at: {PROJECT_DIR}. "
        f"If code suggestions include file paths, use this root path."
    )
    try:
        response = ai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_notes = response.choices[0].message.content.strip()
        # --- For now: Print out suggestions for developer to copy-paste ---
        print("\n--- AI CODE SUGGESTIONS ---\n")
        print(ai_notes)
        changed_files = ["(copy-paste from notes above)"]
        # --- Optionally, script can auto-edit files here ---
        return changed_files, ai_notes
    except Exception as e:
        print("AI codegen failed:", e)
        return [], str(e)
