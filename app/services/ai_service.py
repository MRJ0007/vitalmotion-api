from datetime import datetime
from app.services.azure_language_service import analyze_health_text
from app.services.gemini_service import generate_ai_insight


def analyze_vitals(vitals: dict) -> dict:
    hr = vitals.get("heart_rate")
    spo2 = vitals.get("spo2")
    temp = vitals.get("temperature")

    status = "normal"
    risks = []

    if hr is not None and (hr < 50 or hr > 120):
        status = "warning"
        risks.append("Abnormal heart rate detected")

    if spo2 is not None and spo2 < 94:
        status = "critical"
        risks.append("Low oxygen saturation")

    if temp is not None and temp > 38:
        if status != "critical":
            status = "warning"
        risks.append("Elevated body temperature")

    severity_map = {
        "normal": 0,
        "warning": 2,
        "critical": 3,
    }

    # ---- AZURE AI (MICROSOFT AI SERVICE) ----
    vitals_text = (
        f"Heart rate {hr}, "
        f"oxygen saturation {spo2}, "
        f"temperature {temp}"
    )

    try:
        azure_ai_text = analyze_health_text(vitals_text)
    except Exception as e:
        print("❌ Azure AI error:", e)
        azure_ai_text = "Azure AI analysis unavailable."

    # ---- GEMINI AI ----
    try:
        gemini_text = generate_ai_insight(vitals)
    except Exception as e:
        print("❌ Gemini AI error:", e)
        gemini_text = "AI insight unavailable."

    return {
        "status": status,
        "severity": severity_map[status],
        "risks": risks,
        "ai_insight": f"{azure_ai_text} {gemini_text}",
        "generated_at": datetime.utcnow(),
    }
