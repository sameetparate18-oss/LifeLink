import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ================= LOAD MEDICAL DATABASE =================
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "disease_info.json")

try:
    with open(DB_PATH, "r", encoding="utf-8") as f:
        DISEASE_DB = json.load(f)
except:
    DISEASE_DB = {"diseases": {}}


# ================= SAFETY SYSTEM PROMPT =================
SYSTEM_PROMPT = """
You are LifeLink AI Medical Assistant.

You are NOT a doctor.
You are a clinical decision support system.

Rules:
- Never give final diagnosis
- Always mention uncertainty
- Prioritize life-threatening conditions
- If emergency symptoms appear → warn immediately
- Be structured and clear

OUTPUT FORMAT:

1. Possible Conditions
2. Reasoning (medical explanation)
3. Risk Level (Low / Medium / High / Critical)
4. Recommended Actions
5. Emergency Warning (if needed)
"""


# ================= DATABASE CONTEXT BUILDER =================
def build_medical_context(symptoms_text: str):

    diseases = DISEASE_DB.get("diseases", {})

    context = []

    for d in diseases.values():
        context.append({
            "name": d.get("name"),
            "severity": d.get("severity_level"),
            "symptoms": [s["name"] for s in d.get("symptoms", [])],
            "emergency": d.get("emergency", False),
            "description": d.get("description", "")
        })

    return {
        "user_symptoms": symptoms_text,
        "medical_database": context[:10]  # keep small for token safety
    }


# ================= EMERGENCY DETECTOR =================
def detect_emergency(text: str) -> bool:

    danger_keywords = [
        "chest pain",
        "unable to breathe",
        "unconscious",
        "severe bleeding",
        "heart pain",
        "stroke",
        "paralysis"
    ]

    text = text.lower()

    return any(word in text for word in danger_keywords)


# ================= MAIN AI ENGINE =================
def doctor_ai_predict(symptoms_text: str):

    try:

        emergency_flag = detect_emergency(symptoms_text)

        medical_context = build_medical_context(symptoms_text)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"""
Patient Symptoms:
{symptoms_text}

Medical Database Reference:
{json.dumps(medical_context, indent=2)}
"""
                }
            ],
            temperature=0.3
        )

        ai_response = response.choices[0].message.content

        return {
            "success": True,
            "ai_response": ai_response,
            "emergency_flag": emergency_flag,
            "system": "LifeLink Medical AI v5.0"
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "ai_response": "AI service unavailable"
        }