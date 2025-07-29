import sys
from codegen_agent import codegen_chat
from testing_agent import run_tests         # <-- UPDATED import!
from deploy_agent import deploy
from alert_agent import send_alert
from backup_agent import backup

def main():
    print("Welcome to 3DShapeSnap.AI Dev Agent Chat!")
    print("Describe the feature you want to build or update:")
    feature_desc = input("> ")

    print("\n[1/5] Creating backup...")
    backup()
    print("[OK] Backup complete.\n")

    print("[2/5] Generating code...")
    changed_files, ai_notes = codegen_chat(feature_desc)
    print("[OK] Code generated. Files changed:", changed_files)

    print("[3/5] Running tests...")
    tests_passed, test_output = run_tests()
    print(test_output)
    if not tests_passed:
        send_alert(f"❌ Tests FAILED after codegen for: {feature_desc}\n\n{test_output}")
        print("Tests failed. Rollback advised.")
        sys.exit(1)
    print("[OK] All tests passed.\n")

    print("[4/5] Deploying changes...")
    deploy()
    print("[OK] Deploy triggered.\n")

    print("[5/5] Sending alerts...")
    send_alert(f"✅ Feature added & deployed: {feature_desc}\n\nFiles changed: {changed_files}\n\nAI Notes:\n{ai_notes}\n\nTest results:\n{test_output}")
    print("All done! You’ll get an email shortly.\n")

if __name__ == "__main__":
    main()
