import React, { useState } from "react";
import "./App.css";

function App() {
  const [clientName, setClientName] = useState("");
  const [csvFile, setCsvFile] = useState(null);
  const [status, setStatus] = useState("");
  const [progress, setProgress] = useState(0);
  const [reportUrl, setReportUrl] = useState("");

  const simulatePipeline = async () => {
    if (!csvFile || !clientName) {
      alert("Please enter client name and upload CSV file.");
      return;
    }

    setStatus("Uploading CSV...");
    setProgress(10);

    const formData = new FormData();
    formData.append("file", csvFile);
    formData.append("client", clientName);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();

      if (result.status === "success") {
        setStatus("✅ Complete!");
        setProgress(100);
        setReportUrl(result.report_url);
      } else {
        setStatus("❌ Error: " + result.message);
      }
    } catch (error) {
      setStatus("❌ Failed to connect to backend.");
      console.error(error);
    }
  };

  return (
    <div className="App">
      <h1>🧠 DivisionMedia Research Tool</h1>

      <div style={{ marginBottom: 16 }}>
        <label>Client Name: </label>
        <input
          type="text"
          value={clientName}
          onChange={(e) => setClientName(e.target.value)}
        />
      </div>

      <div style={{ marginBottom: 16 }}>
        <label>Upload Onboarding CSV: </label>
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setCsvFile(e.target.files[0])}
        />
      </div>

      <button onClick={simulatePipeline}>🚀 Run Research</button>

      {status && (
        <div style={{ marginTop: 20 }}>
          <p><strong>Status:</strong> {status}</p>
          <progress value={progress} max="100" style={{ width: "100%" }} />
          {reportUrl && (
            <p>
              <a href={reportUrl} target="_blank" rel="noreferrer">
                📄 View Google Sheet Report
              </a>
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
