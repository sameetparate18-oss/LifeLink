import json
import os
import logging
from typing import Dict, List, Any
from difflib import SequenceMatcher


# ================= LOGGING =================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("lifelink.ai.predictor")


# ================= LOAD DATABASE =================
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "disease_info.json")

try:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        disease_database = json.load(f)
    logger.info("✅ Disease database loaded successfully")

except Exception as e:
    logger.error(f"❌ DB load failed: {str(e)}")
    disease_database = {"diseases": {}}


# ================= MEDICAL KNOWLEDGE LAYER =================
MEDICAL_SYNONYMS = {
    "fever": ["pyrexia", "high temperature", "hot body"],
    "cough": ["dry cough", "wet cough"],
    "breathing difficulty": ["shortness of breath", "dyspnea", "asthma-like"],
    "chest pain": ["heart pain", "angina", "tight chest"],
    "fatigue": ["weakness", "tiredness", "exhaustion"],
    "vomiting": ["nausea", "throwing up"],
    "headache": ["migraine", "head pain"],
    "swelling": ["inflammation", "edema"]
}


# ================= UTILITIES =================
def normalize(text: str) -> str:
    return text.strip().lower()


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def expand(symptoms: List[str]) -> List[str]:
    expanded = []

    for s in symptoms:
        s = normalize(s)
        expanded.append(s)

        for key, vals in MEDICAL_SYNONYMS.items():
            if s == key or s in vals:
                expanded.append(key)
                expanded.extend(vals)

    return list(set(expanded))


# ================= CORE AI ENGINE =================
def predict_disease(symptoms: List[str]) -> Dict[str, Any]:

    try:

        if not symptoms:
            return {
                "prediction": "No Symptoms Provided",
                "confidence": "0%",
                "severity": "unknown",
                "description": "Please enter symptoms",
                "precautions": []
            }

        # expand medical intelligence
        input_symptoms = expand(symptoms)

        diseases = disease_database.get("diseases", {})

        if not diseases:
            return {
                "prediction": "Database Missing",
                "confidence": "0%",
                "severity": "unknown",
                "description": "No disease data available",
                "precautions": []
            }

        best_match = None
        best_score = 0
        best_matches = []

        # ================= SCORING ENGINE =================
        for _, disease in diseases.items():

            disease_symptoms = disease.get("symptoms", [])

            score = 0
            matches = []

            for s in disease_symptoms:

                name = normalize(s.get("name", ""))
                weight = s.get("weight", 1)

                for inp in input_symptoms:

                    # EXACT OR FUZZY MATCH
                    if inp in name or name in inp:
                        score += weight
                        matches.append(name)

                    elif similarity(inp, name) > 0.82:
                        score += weight * 0.8
                        matches.append(name)

            # normalize score
            if score > best_score:
                best_score = score
                best_match = disease
                best_matches = matches

        # ================= NO MATCH =================
        if not best_match:
            return {
                "prediction": "Unknown Condition",
                "confidence": "0%",
                "severity": "low",
                "description": "No strong disease match found.",
                "precautions": [
                    "Consult doctor",
                    "Monitor symptoms",
                    "Avoid self-medication"
                ]
            }

        # ================= CONFIDENCE ENGINE =================
        total_weight = sum(
            s.get("weight", 1)
            for s in best_match.get("symptoms", [])
        )

        base_confidence = (best_score / max(total_weight, 1)) * 100
        confidence = min(round(base_confidence, 2), 99.9)

        # ================= SEVERITY ENGINE =================
        severity = best_match.get("severity_level", "medium")

        emergency = best_match.get("emergency", False)

        if emergency and confidence > 60:
            severity = "CRITICAL"

        elif confidence > 80:
            severity = "HIGH"

        elif confidence > 50:
            severity = "MEDIUM"

        else:
            severity = "LOW"

        # ================= PRIORITY BOOST =================
        priority_score = best_match.get("ai_priority_score", 0)
        final_risk_score = round((confidence * 0.7) + (priority_score * 0.3), 2)

        logger.info(f"Predicted: {best_match.get('name')}")

        # ================= FINAL RESPONSE =================
        return {
            "prediction": best_match.get("name", "Unknown"),
            "confidence": f"{confidence}%",
            "severity": severity,
            "risk_score": final_risk_score,
            "description": best_match.get("description", ""),
            "matched_symptoms": best_matches,
            "recommended_tests": best_match.get("recommended_tests", []),
            "precautions": best_match.get("precautions", []),
            "recommended_medications": best_match.get("recommended_medications", []),
            "specialists": best_match.get("recommended_specialists", []),
            "emergency": emergency,
            "emergency_actions": best_match.get("emergency_actions", []),
            "survival_rate": best_match.get("survival_rate", "Unknown"),
            "recovery_days": best_match.get("estimated_recovery_days", "Unknown")
        }

    except Exception as e:

        logger.error(f"Prediction error: {str(e)}")

        return {
            "prediction": "System Error",
            "confidence": "0%",
            "severity": "unknown",
            "description": str(e),
            "precautions": []
        }


# ================= HEALTH CHECK =================
def predictor_health_check():

    return {
        "status": "ACTIVE",
        "database_loaded": bool(disease_database.get("diseases")),
        "total_diseases": len(disease_database.get("diseases", {}))
    }