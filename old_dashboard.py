print(" ***DASHBOARD FILE LOADED***")
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
app = FastAPI()

@app.get("/")
def home():
    return {"status": "working"}

from datetime import datetime, UTC
import json
import html

from validator import validate_signal
from samachar_input_adapter import load_data, convert_to_signals
from sanskar_engine import analyze_patterns
from integration_adapter import run_engine
from error_handler import error_response




# -------------------------------
# SAFE STRING (XSS PROTECTION)F
# -------------------------------
def safe(v):
    if isinstance(v, (dict, list)):
        return html.escape(json.dumps(v, default=str))
    return html.escape(str(v))


# -------------------------------
# LOGGING
# -------------------------------
def log_data(filename, log_type, data):
    try:
        log_entry = {
            "trace_id": data.get("trace_id", "N/A"),
            "timestamp": datetime.now(UTC).isoformat(),
            "type": log_type,
            "data": data
        }
        with open(f"logs/{filename}", "a") as f:
            f.write(json.dumps(log_entry, default=str) + "\n")
    except:
        pass


# ------------------------@app.get(-------
# ✅ FIXED ZONE DETECTION (MATCHES ENGINE)
# -------------------------------
def detect_zone(signal):
    try:
        lat = float(signal.get("latitude", 0))

        if lat > 23:
            return "North"
        elif lat > 20:
            return "Central"
        else:
            return "South"

    except:
        return "Unknown"


# -------------------------------
# DASHBOARD
# -------------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    import traceback 
    try:
        print("STEP 1: loading data")
        weather, aqi = load_data()

        print("STEP 2: converting signals")
        signals = convert_to_signals(weather, aqi)

        print("STEP 3: signals sample:", signals[:2])

        if not isinstance(signals, list) or not signals:
            return HTMLResponse("<h3>No data / invalid input</h3>")

        rows = ""
        processed_outputs = []

        for signal in signals[:20]:

            if not isinstance(signal, dict):
                continue

            validation = validate_signal(signal)

            #  SHOW INVALID
            if validation.get("status") == "ERROR":
                rows += f"""
                <tr style="background-color:#ffcccc;">
                    <td>{safe(signal.get("signal_id"))}</td>
                    <td>Unknown</td>
                    <td>INVALID</td>
                    <td>-</td>
                    <td>-</td>
                    <td>Validation Failed</td>
                    <td>-</td>
                </tr>
                """
                continue

            analysis = run_engine(validation)
            print("ANALYSIS:", analysis)
            
            if not isinstance(analysis, dict):
                print("ERROR: analysis not dict", analysis)
                continue

            if not isinstance(analysis, dict) or analysis.get("status") == "ERROR":
                continue

            zone = detect_zone(signal)
            risk = analysis.get("risk_level", "LOW")

            # ✅ ACTION MAPPING (CORRECT)
            action_type = analysis.get("recommendation_signal", "monitor")
            action_label = action_type.replace("_", " ").title()

        # Keep UI color (based on risk ONLY for display)
            

            if risk == "HIGH":
                row_color = "#ffe6e6"
            elif risk == "MEDIUM":
                row_color = "#fff5cc"
            else:
                row_color = ""

            # pattern input
            processed_outputs.append({
                "signal_id": signal.get("signal_id"),
                "trace_id": validation.get("trace_id"),
                "risk_level": risk,
                "latitude": signal.get("latitude"),
                "longitude": signal.get("longitude"),
                "anomaly_score": analysis.get("anomaly_score", 0)
            })

            # logging
            log_data("validation_logs.json", "VALIDATION", validation)
            log_data("anomaly_logs.json", "ANALYSIS", analysis)

            rows += f"""
            <tr style="background-color:{row_color};">
                <td>{safe(signal.get("signal_id"))}</td>
                <td>{safe(zone)}</td>
                <td>{safe(validation.get("status"))}</td>
                <td>{safe(risk)}</td>
                <td>{safe(analysis.get("anomaly_type"))}</td>
                <td>{safe(analysis.get("explanation"))}</td>

                <!-- ✅ ADD THIS LINE -->
                <td>{safe(analysis.get("recommendation_signal"))}</td>

                <td>
                    <button onclick="sendAction('{safe(validation.get("trace_id"))}','{action_type}')">
                        {action_label}
                    </button>   
                </td>
            </tr>
            """

        # -------------------------------
        # PATTERN ANALYSIS
        # -------------------------------
        try:
            pattern = analyze_patterns(processed_outputs) if processed_outputs else {}
        except:
            pattern = {}

        pattern_id = safe(pattern.get("pattern_id", "N/A"))
        pattern_type = safe(pattern.get("pattern_type", "NONE"))
        pattern_summary = safe(pattern.get("pattern_summary", "No data"))
        pattern_count = safe(pattern.get("anomaly_count", 0))

        # -------------------------------
        # OBSERVABILITY
        # -------------------------------
        total_signals = len(signals)
        total_anomalies = len(
            [o for o in processed_outputs if o["risk_level"] != "LOW"]
        )

        try:
            with open("logs/action_logs.json") as f:
                action_count = len(f.readlines())
        except:
            action_count = 0

        # -------------------------------
        # HTML
        # -------------------------------
        html_content = f"""
        <html>
        <head>
            <title>NICAI Dashboard</title>

            <script>
            async function sendAction(trace_id, action_type) {{
                await fetch("/action", {{
                    method: "POST",
                    headers: {{"Content-Type": "application/json"}},
                    body: JSON.stringify({{
                        trace_id: trace_id,
                        action_type: action_type
                    }})
                }});
                alert("Action logged successfully");
                location.reload();
            }}
            </script>
        </head>

        <body>

        <h2>NICAI Intelligence Dashboard</h2>

        <h3>System Observability</h3>
        <p>Total Signals: {total_signals}</p>
        <p>Total Anomalies: {total_anomalies}</p>
        <p>Actions Logged: {action_count}</p>

        <h3>Pattern</h3>
        <p>ID: {pattern_id}</p>
        <p>Count: {pattern_count}</p>
        <p>Type: {pattern_type}</p>
        <p>Summary: {pattern_summary}</p>

        <h3>Signals</h3>

        <table border="1" cellpadding="5">
        <tr>
            <th>ID</th><th>Zone</th><th>Status</th>
            <th>Risk</th><th>Type</th><th>Explanation</th><th>Recommendation</th><th>Action</th>
        </tr>

        {rows}

        </table>

        </body>
        </html>
        """

        return HTMLResponse(content=html_content)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return HTMLResponse(f"<h2>ERROR:</h2><pre>{str(e)}</pre>")
