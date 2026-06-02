import pandas as pd
from datetime import datetime, timedelta  
from bucket_emitter import emit_bucket_artifact
import uuid

# -----------------------------
# 1️ LOAD DATA
# -----------------------------
def load_data():
    try:
        weather = pd.read_csv("clean_weather.csv")
        aqi = pd.read_csv("clean_aqi.csv")

        print(" Data Loaded Successfully")
        return weather, aqi

    except Exception as e:
        print("❌ Error loading data:", e)
        return None, None


# -----------------------------
# 2️ CONVERT TO NICAI SIGNALS
# -----------------------------
def convert_to_signals(weather, aqi):

    signals = []

    print(f" Using WEATHER dataset only (aligned data)")

    for i, row in weather.iterrows():

        temp = row.get("temperature", 0)
        aqi_val = row.get("aqi", 0)

        # handle missing
        if pd.isna(temp):
            temp = 0

        if pd.isna(aqi_val):
            aqi_val = 0

        # 🔴 FIX unrealistic temperature (important)
        if temp > 60:   # likely wrong data
            temp = temp / 2   # simple correction (demo-safe)
        # 🔥 ADD TIME VARIATION
        base_date = datetime.strptime(str(row.get("date", "2024-01-01")), "%Y-%m-%d")
        timestamp = base_date + timedelta(minutes=i)
        
        trace_id = f"trace_{uuid.uuid4().hex[:8]}"

        signal = {
            "signal_id": f"S_{i}",
            "trace_id": trace_id,
            "timestamp": str(timestamp),
            "value": {
                "temperature": float(temp),
                "aqi": float(aqi_val)
            },
            "location": row.get("city", "unknown")
        }

        '''emit_bucket_artifact(
            "ingestion_logs.json",
            "INGESTION",
            signal
        )'''

        signals.append(signal)
        '''signals.append({
            "signal_id": f"S_{i}",
            "timestamp": str(timestamp),
            "value": {
                "temperature": float(temp),
                "aqi": float(aqi_val)
            },
            "location": row.get("city", "unknown")
        })'''

    print(f" Combined Signals Created: {len(signals)}")
    # ✅ PHASE 2 VALIDATION CHECKS
    missing_fields = 0
    invalid_timestamps = 0
    invalid_locations = 0

    for s in signals[:100]:  # sample check
        if not s.get("signal_id") or not s.get("timestamp") or not s.get("value"):
            missing_fields += 1

        if not isinstance(s.get("timestamp"), str):
            invalid_timestamps += 1

        if not s.get("location") or s.get("location") == "unknown":
            invalid_locations += 1

    print(f"[CHECK] Missing fields: {missing_fields}")
    print(f"[CHECK] Invalid timestamps: {invalid_timestamps}")
    print(f"[CHECK] Invalid locations: {invalid_locations}")
    # ✅ VALUE STRUCTURE CHECK
    bad_values = 0

    for s in signals[:100]:
        val = s.get("value", {})
        if "temperature" not in val or "aqi" not in val:
            bad_values += 1

    print(f"[CHECK] Bad value structures: {bad_values}")


# ✅ CITY DISTRIBUTION CHECK
    cities = [s["location"] for s in signals]
    unique_cities = set(cities)

    print(f"[CHECK] Unique cities: {len(unique_cities)}")
    print(f"[CHECK] Sample cities: {list(unique_cities)[:5]}")
    return signals