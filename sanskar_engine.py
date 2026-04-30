"""
sanskar_engine.py — Sanskar Intelligence Engine
Sanskar Pandey

The core ML/analytics engine. Receives pre-mapped input from integration_adapter.py.
Do NOT call this directly from routes — always go through integration_adapter.run_engine().

Input format (from integration_adapter.map_nicai_to_engine_input):
  {
    "temperature": float,
    "pollution": float,
    "trend": float (0.0-1.0),
    "zone": [str]
  }

Output format:
  {
    "risk_level": "HIGH|MEDIUM|LOW",
    "anomaly_type": str,
    "temporal_context": "RISING|STABLE|FALLING",
    "spatial_context": str,
    "confidence_score": float,
    "explanation": str,
    "recommendation_signal": "eligible_for_escalation|requires_review|monitor"
  }
"""


class SanskarEngine:

    def __init__(self):
        pass

    def process(self, signals: dict) -> dict:
        """
        Main entry point. Runs full analysis pipeline.
        Returns NICAI-compatible output dict. Never raises.
        """
        try:
            processed = self.preprocess(signals)

            anomaly = self.detect_anomaly(processed)
            temporal = self.analyze_temporal(processed)
            spatial = self.analyze_spatial(processed)
            risk = self.calculate_risk(processed, anomaly, temporal)
            confidence = self.calculate_confidence(processed,anomaly)
            explanation = self.generate_explanation(processed, anomaly, temporal, spatial)

            if risk == "HIGH":
                recommendation = "eligible_for_escalation"
            elif risk == "MEDIUM":
                recommendation = "requires_review"
            else:
                recommendation = "monitor"

            return {
                "risk_level": risk,
                "anomaly_type": anomaly,
                "temporal_context": temporal,
                "spatial_context": spatial,
                "confidence_score": confidence,
                "explanation": explanation,
                "recommendation_signal": recommendation,
            }

        except Exception as e:
            return {
                "risk_level": "LOW",
                "anomaly_type": "engine_error",
                "temporal_context": "STABLE",
                "spatial_context": "unknown",
                "confidence_score": 0.0,
                "explanation": f"Engine processing error: {str(e)}",
                "recommendation_signal": "monitor",
            }

    def preprocess(self, signals: dict) -> dict:
        """Coerce all numeric fields to float."""
        result = {}
        for k, v in signals.items():
            if isinstance(v, (int, float)):
                result[k] = float(v)
            else:
                result[k] = v
        return result

    def detect_anomaly(self, signals: dict) -> str:
        """Multi-signal anomaly detection with priority logic."""
        pollution = signals.get("pollution", 0)
        temp = signals.get("temperature", 0)

        # Multi-signal FIRST (highest priority)
        if pollution >= 300 and temp >= 35:
            return "severe_environmental_risk"

        if pollution >= 200 and temp >= 30:
            return "high_pollution_with_heat"

        # Single-signal fallback
        if pollution >= 300:
            return "severe_pollution"

        if pollution >= 200:
            return "high_pollution"

        if pollution >= 150:
            return "moderate_pollution"
        
        if temp >= 40:
            return "heat_risk"

        if temp >= 35:
            return "elevated_temperature"

        return "normal"

    def analyze_temporal(self, signals: dict) -> str:
        """Classify trend direction from 0.0-1.0 trend value."""
        trend = signals.get("trend", 0.5)
        if trend > 0.7:
            return "RISING"
        elif trend < 0.3:
            return "FALLING"
        return "STABLE"

    def analyze_spatial(self, signals: dict) -> str:
        """Determine spatial context from zone list."""
        zone = signals.get("zone", ["unknown"])
        if isinstance(zone, list):
            if len(zone) > 1:
                return "CLUSTERED"
            return str(zone[0]) if zone else "unknown"
        return "unknown"

    def calculate_risk(self, signals: dict, anomaly: str, temporal: str) -> str:
        """
        Risk = base risk from anomaly type, adjusted by temporal trend.
        RISING escalates MEDIUM -> HIGH.
        FALLING de-escalates HIGH -> MEDIUM, MEDIUM -> LOW.
        """
        severe_anomalies = {
            "severe_environmental_risk",
            "severe_pollution",
            "high_pollution_with_heat",
            "heat_risk",  
        }

        if anomaly in severe_anomalies:
            base = "HIGH"
        elif anomaly in ("high_pollution", "moderate_pollution", "elevated_temperature"):
            base = "MEDIUM"
        else:
            base = "LOW"

        if temporal == "RISING":
            if base == "MEDIUM":
                return "HIGH"
        elif temporal == "FALLING":
            if base == "HIGH":
                return "MEDIUM"
            if base == "MEDIUM":
                return "LOW"

        return base

    def calculate_confidence(self, signals: dict, anomaly: str) -> float:
        """Confidence score based on signal severity."""
        pollution = signals.get("pollution", 0)
        temp = signals.get("temperature", 0)
        trend = signals.get("trend", 0.5)

        if pollution >= 300 and temp >= 35:
            return 0.95
        
        if anomaly == "high_pollution_with_heat":
            return 0.90
        
        if anomaly == "heat_risk":
            return 0.85
        
        if pollution >= 200:
            return 0.90 if trend > 0.5 else 0.85
        if pollution >= 150:
            return 0.75
        
        return 0.60

    def generate_explanation(self, signals: dict, anomaly: str, temporal: str, spatial: str) -> str:
        pollution = signals.get("pollution", 0)
        temp = signals.get("temperature", 0)

        location = spatial if spatial != "unknown" else "the area"

        reasons = []

        if pollution >= 150:
            reasons.append(f"AQI {int(pollution)} (high pollution)")

        if temp >= 40:
            reasons.append(f"{int(temp)}°C (extreme heat)")
        elif temp >= 35:
            reasons.append(f"{int(temp)}°C (elevated temperature)")

        if temporal == "RISING":
            reasons.append("conditions are worsening")
        elif temporal == "FALLING":
            reasons.append("conditions are improving")

        if spatial == "CLUSTERED":
            reasons.append("impact across multiple areas")

        reason_text = ", ".join(reasons) if reasons else "normal conditions"

        #  HUMANIZED OUTPUTS

        if anomaly == "heat_risk":
            return f"Extreme heat in {location} ({int(temp)}°C) may cause health stress. Stay hydrated and limit outdoor exposure."

        if anomaly == "high_pollution_with_heat":
            return f"Air quality in {location} is unhealthy (AQI {int(pollution)}) along with high temperature ({int(temp)}°C). This combination can impact health. Caution is advised."

        if anomaly == "severe_environmental_risk":
            return f"Air quality in {location} is extremely poor (AQI {int(pollution)}), combined with high temperature ({int(temp)}°C). This poses a serious health risk. Immediate attention is recommended."

        # fallback
        return f"Conditions in {location} show {reason_text}. Currently stable but should be monitored."

# -------------------------------------------------------
# Module-level pattern analysis (used by run_demo_full.py)
# -------------------------------------------------------
def _analyze_patterns_impl(results: list) -> dict:
    """Compute risk distribution summary from a list of result dicts."""
    try:
        total = len(results)
        high = sum(1 for r in results if isinstance(r, dict) and r.get("risk_level") == "HIGH")
        medium = sum(1 for r in results if isinstance(r, dict) and r.get("risk_level") == "MEDIUM")
        low = sum(1 for r in results if isinstance(r, dict) and r.get("risk_level") == "LOW")

        if high >= 5:
            pattern_type = "CLUSTER_ANOMALY"
            severity = "INCREASING"
        elif high >= 2:
            pattern_type = "REPEATED_ANOMALY"
            severity = "STABLE"
        elif high == 1:
            pattern_type = "ISOLATED_EVENT"
            severity = "LOW"
        else:
            pattern_type = "NO_PATTERN"
            severity = "NONE"

        return {
            "pattern_id": "pattern_auto",
            "count": total,
            "type": "risk_distribution",
            "pattern_type": pattern_type,
            "severity_trend": severity,
            "summary": f"HIGH: {high}, MEDIUM: {medium}, LOW: {low}",
        }

    except Exception as e:
        return {
            "pattern_id": "error",
            "count": 0,
            "type": "error",
            "pattern_type": "NO_PATTERN",
            "severity_trend": "NONE",
            "summary": str(e),
        }


def analyze_patterns(results: list) -> dict:
    """Standalone function for use in run_demo_full.py and /run route."""
    return _analyze_patterns_impl(results)
