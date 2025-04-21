from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

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

    # Call your real pipeline here
    try:
        result = subprocess.run(
            ["python", "run_pipeline.py", filepath, client],
            capture_output=True, text=True, timeout=300
        )
        print(result.stdout)
        return jsonify({"status": "success", "report_url": get_sheet_url(client)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def get_sheet_url(client):
    # Match client to their Google Sheet ID
    sheet_map = {
        "roamer.dk": "1mjHTz2J-IErgGjcJKbpBxav-sagNqRBU_Ll-m1d3vXs",
        "karlskicks": "1defKarlsKicksGoogleSheetId987654321"
    }
    sheet_id = sheet_map.get(client.lower())
    if sheet_id:
        return f"https://docs.google.com/spreadsheets/d/{sheet_id}"
    return None

if __name__ == "__main__":
    app.run(debug=True)
