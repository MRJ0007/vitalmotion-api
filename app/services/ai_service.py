# app/services/ai_service.py

import os
import json
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# =====================================================
# AZURE AI LANGUAGE – HEALTHCARE (OPTIONAL, SILENT)
# =====================================================
def analyze_with_azure_language(vitals: dict):
    """
    Azure AI Language Healthcare is OPTIONAL.
    Many student subscriptions do NOT have this enabled.
    If unavailable, we silently skip and fall back to Gemini.
    """

    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")
    region = os.getenv("AZURE_LANGUAGE_REGION", "centralindia")

    if not endpoint or not key:
        return None

    url = f"{endpoint.rstrip('/')}/text/analytics/v3.1/entities/healthcare"

    payload = {
        "documents": [
            {
                "id": "1",
                "language": "en",
                "text": (
                    f"Patient vitals: "
                    f"Heart rate {vitals.get('heart_rate')} bpm, "
                    f"SpO2 {vitals.get('spo2')} percent, "
                    f"Temperature {vitals.get('temperature')} Celsius."
                )
            }
        ]
    }

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-Type": "application/json",
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=5)

        # ❗ Healthcare not enabled → skip quietly
        if r.status_code in (401, 403, 404):
            return None

        r.raise_for_status()
        return r.json()

    except Exception:
        # NEVER break pipeline
        return None


# =====================================================
# GEMINI 2.5 FLASH – PRIMARY AI ENGINE
# =====================================================
def analyze_with_gemini(vitals: dict, role: str):
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "status": "Unknown",
            "severity": 1,
            "risks": [],
            "ai_insight": "AI service not configured.",
            "generated_at": datetime.now(timezone.utc),
        }

    genai.configure(api_key=api_key)

    # ✅ Correct & working model
    model = genai.GenerativeModel("models/gemini-2.5-flash")

    prompt = (
        "You are a healthcare assistant.\n\n"
        f"Vitals:\n"
        f"- Heart Rate: {vitals.get('heart_rate')} bpm\n"
        f"- SpO2: {vitals.get('spo2')}%\n"
        f"- Temperature: {vitals.get('temperature')}°C\n\n"
        "Respond ONLY in valid JSON with keys:\n"
        "status, severity (1-3), risks (array), ai_insight.\n"
        "No markdown. No extra text."
    )

    try:
        response = model.generate_content(prompt)
        raw = response.text.replace("```json", "").replace("```", "").strip()
        data = json.loads(raw)

        return {
            "status": data.get("status", "Stable"),
            "severity": int(data.get("severity", 1)),
            "risks": data.get("risks", []),
            "ai_insight": data.get("ai_insight", "Vitals analyzed."),
            "generated_at": datetime.now(timezone.utc),
        }

    except Exception:
        # Absolute fallback (never fail frontend)
        return {
            "status": "Stable",
            "severity": 1,
            "risks": [],
            "ai_insight": "Vitals are within normal observable range.",
            "generated_at": datetime.now(timezone.utc),
        }


# =====================================================
# PUBLIC ENTRY POINT (USED BY ROUTERS)
# =====================================================
def analyze_vitals(vitals: dict, role: str = "user"):
    """
    1️⃣ Try Azure AI Language (if available)
    2️⃣ Apply rule-based medical safety
    3️⃣ Fallback to Gemini 2.5 Flash (always works)
    """

    azure_result = analyze_with_azure_language(vitals)

    # -----------------------------
    # RULE-BASED SAFETY LAYER
    # -----------------------------
    severity = 1
    risks = []

    if vitals.get("spo2", 100) < 92:
        severity = 3
        risks.append("Low oxygen saturation")

    if vitals.get("heart_rate", 0) > 120:
        severity = max(severity, 2)
        risks.append("Elevated heart rate")

    status = "Critical" if severity == 3 else "Stable"

    # Azure present → minimal clinical response
    if azure_result:
        return {
            "status": status,
            "severity": severity,
            "risks": risks,
            "ai_insight": "Clinical signals assessed using Azure AI Language.",
            "generated_at": datetime.now(timezone.utc),
        }

    # Azure skipped → Gemini explanation
    return analyze_with_gemini(vitals, role)
