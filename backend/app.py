from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
import json
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Google credentials from Render environment
creds = Credentials.from_service_account_info(json.loads(os.environ["SERVICE_ACCOUNT_JSON"]))
gc = gspread.authorize(creds)

# Optional: if you want to get the sheet object directly
def get_sheet_by_client(client):
    sheet_map = {
        "roamer.dk": "1mjHTz2J-IErgGjcJKbpBxav-sagNqRBU_Ll-m1d3vXs",
        "karlskicks": "1SHEET_ID_FOR_KARLSKICKS"
    }
    sheet_id = sheet_map.get(client.lower())
    if sheet_id:
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}"
    return None

@app.route("/")
def index():
    return "✅ Flask backend is live!"

@app.route("/upload", methods=["POST"])
def upload_csv():
    file = request.files["file"]
    client = request.form["client"]

    filename = f"{client.lower().replace(' ', '-')}.csv"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        # Run the full research pipeline
        result = subprocess.run(
            ["python", "run_pipeline.py", filepath, client],
            capture_output=True,
            text=True,
            timeout=300
        )
        print(result.stdout)

        # Return sheet link
        sheet_url = get_sheet_by_client(client)
        return jsonify({
            "status": "success",
            "report_url": sheet_url
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
