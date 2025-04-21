import sys
import os

def run_pipeline(filepath, client):
    print(f"🔁 Running pipeline for: {client}")
    os.system("python load_roamer.py")
    os.system("python phase2.py")
    os.system("python phase3_sheet.py")
    os.system("python phase4_synthesis.py")
    print("✅ Pipeline complete for", client)

if __name__ == "__main__":
    filepath = sys.argv[1]
    client = sys.argv[2]
    run_pipeline(filepath, client)
