import os
import google.generativeai as genai

# Configure
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Personalities
USER_STYLE = "Role: Warm health assistant. Tone: Caring, emoji-rich. Style: Plain text, no markdown."
DOCTOR_STYLE = "Role: Clinical analyst. Tone: Objective, professional. Style: Markdown tables, clinical terms."

def generate_ai_insight(vitals: dict, role: str = "user") -> str:
    try:
        # Use 1.5-flash for speed/reliability
        model = genai.GenerativeModel("gemini-2.5-flash")

        personality = DOCTOR_STYLE if role == "doctor" else USER_STYLE

        prompt = f"""
        {personality}
        
        Vitals Data:
        - Heart Rate: {vitals.get('heart_rate')} bpm
        - Oxygen (SpO2): {vitals.get('spo2')}%
        - Temperature: {vitals.get('temperature')}°C
        
        Provide a concise analysis for the {role}.
        """

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"AI Error: {e}")
        return "Insight currently unavailable. Please check back shortly."