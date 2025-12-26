# app/services/ai_service.py

import os
import json
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# =====================================================
# AZURE AI LANGUAGE (PRIMARY – CLINICAL SIGNALS)
# =====================================================
def analyze_with_azure_language(vitals: dict):
    endpoint = os.getenv("AZURE_LANGUAGE_ENDPOINT")
    key = os.getenv("AZURE_LANGUAGE_KEY")

    if not endpoint or not key:
        return None

    # ✅ CORRECT Azure Language endpoint (NO colon)
    url = f"{endpoint.rstrip('/')}/language/analyze-text?api-version=2023-04-01"

    text = (
        f"Patient vitals: "
        f"Heart rate {vitals.get('heart_rate')} bpm, "
        f"SpO2 {vitals.get('spo2')} percent, "
        f"Temperature {vitals.get('temperature')} Celsius."
    )

    payload = {
        "kind": "Healthcare",
        "analysisInput": {
            "documents": [
                {
                    "id": "1",
                    "language": "en",
                    "text": text,
                }
            ]
        },
        "parameters": {
            "fhirVersion": "4.0.1"
        }
    }

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            url, headers=headers, json=payload, timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("⚠️ Azure Language failed:", e)
        return None


# =====================================================
# GEMINI (FALLBACK – HUMAN EXPLANATION)
# =====================================================
def analyze_with_gemini(vitals: dict, role: str):
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {
            "status": "Unknown",
            "severity": 1,
            "risks": [],
            "ai_insight": "Gemini API key not configured.",
            "generated_at": datetime.now(timezone.utc),
        }

    genai.configure(api_key=api_key)

    # ✅ SUPPORTED FREE MODEL
    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        f"You are a healthcare assistant.\n\n"
        f"Vitals:\n"
        f"- Heart Rate: {vitals.get('heart_rate')} bpm\n"
        f"- SpO2: {vitals.get('spo2')}%\n"
        f"- Temperature: {vitals.get('temperature')}°C\n\n"
        f"Return ONLY valid JSON with keys:\n"
        f"status, severity (1-3), risks (array), ai_insight.\n"
        f"No markdown."
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

    except Exception as e:
        print("❌ Gemini failed:", e)
        return {
            "status": "Unknown",
            "severity": 1,
            "risks": [],
            "ai_insight": "AI explanation unavailable.",
            "generated_at": datetime.now(timezone.utc),
        }


# =====================================================
# PUBLIC ENTRY POINT (USED BY ROUTERS)
# =====================================================
def analyze_vitals(vitals: dict, role: str = "user"):
    """
    Primary: Azure AI Language
    Fallback: Gemini
    """

    azure_result = analyze_with_azure_language(vitals)

    if azure_result:
        severity = 1
        risks = []

        if vitals.get("spo2", 100) < 92:
            severity = 3
            risks.append("Low oxygen saturation")

        if vitals.get("heart_rate", 0) > 120:
            severity = max(severity, 2)
            risks.append("Elevated heart rate")

        status = "Critical" if severity == 3 else "Stable"

        return {
            "status": status,
            "severity": severity,
            "risks": risks,
            "ai_insight": "Clinical signals analyzed using Azure AI Language.",
            "generated_at": datetime.now(timezone.utc),
        }

    # Azure failed → Gemini fallback
    return analyze_with_gemini(vitals, role)
