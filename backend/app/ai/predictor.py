import json
import os
import logging
from typing import Dict, List, Any


# =========================================================
# LOGGING CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(
    "lifelink.ai.predictor"
)


# =========================================================
# LOAD AI DISEASE DATABASE
# =========================================================

BASE_DIR = os.path.dirname(__file__)

DATA_PATH = os.path.join(
    BASE_DIR,
    "disease_info.json"
)

try:

    with open(DATA_PATH, "r", encoding="utf-8") as f:

        disease_database = json.load(f)

    logger.info(
        "✅ Disease database loaded successfully"
    )

except Exception as e:

    logger.error(
        f"❌ Failed to load disease database: {str(e)}"
    )

    disease_database = {
        "diseases": {}
    }


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text: str) -> str:

    return text.strip().lower()


# =========================================================
# AI DISEASE PREDICTION ENGINE
# =========================================================

def predict_disease(
    symptoms: List[str]
) -> Dict[str, Any]:

    """
    AI disease prediction engine using
    weighted symptom matching.
    """

    try:

        # =================================================
        # VALIDATE INPUT
        # =================================================

        if not symptoms:

            return {

                "prediction":
                    "No Symptoms Provided",

                "confidence":
                    "0%",

                "severity":
                    "unknown",

                "description":
                    "Please provide symptoms.",

                "precautions":
                    []
            }

        # =================================================
        # CLEAN INPUT
        # =================================================

        input_symptoms = [

            normalize_text(symptom)

            for symptom in symptoms
        ]

        diseases = disease_database.get(
            "diseases",
            {}
        )

        if not diseases:

            return {

                "prediction":
                    "Disease Database Missing",

                "confidence":
                    "0%",

                "severity":
                    "unknown",

                "description":
                    "No diseases found in database.",

                "precautions":
                    []
            }

        best_match = None

        highest_score = 0

        matched_symptoms = []

        # =================================================
        # CHECK EACH DISEASE
        # =================================================

        for disease_key, disease_data in diseases.items():

            score = 0

            current_matches = []

            disease_symptoms = disease_data.get(
                "symptoms",
                []
            )

            # =============================================
            # MATCH SYMPTOMS
            # =============================================

            for symptom_data in disease_symptoms:

                symptom_name = normalize_text(
                    symptom_data.get(
                        "name",
                        ""
                    )
                )

                weight = symptom_data.get(
                    "weight",
                    0
                )

                if symptom_name in input_symptoms:

                    score += weight

                    current_matches.append(
                        symptom_name
                    )

            # =============================================
            # SAVE BEST MATCH
            # =============================================

            if score > highest_score:

                highest_score = score

                best_match = disease_data

                matched_symptoms = current_matches

        # =================================================
        # NO MATCH FOUND
        # =================================================

        if best_match is None:

            return {

                "prediction":
                    "Unknown Disease",

                "confidence":
                    "0%",

                "severity":
                    "unknown",

                "description":
                    "No matching disease found.",

                "precautions": [
                    "Consult a doctor",
                    "Monitor symptoms",
                    "Stay hydrated"
                ]
            }

        # =================================================
        # AI CONFIDENCE CALCULATION
        # =================================================

        total_possible_weight = sum(

            symptom.get("weight", 0)

            for symptom in best_match.get(
                "symptoms",
                []
            )
        )

        confidence = round(

            (
                highest_score /
                max(total_possible_weight, 1)
            ) * 100,

            2
        )

        confidence = min(
            confidence,
            99.9
        )

        logger.info(
            f"✅ Disease predicted: "
            f"{best_match.get('name')}"
        )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        return {

            "prediction":
                best_match.get(
                    "name",
                    "Unknown"
                ),

            "confidence":
                f"{confidence}%",

            "severity":
                best_match.get(
                    "severity_level",
                    "medium"
                ),

            "description":
                best_match.get(
                    "description",
                    ""
                ),

            "matched_symptoms":
                matched_symptoms,

            "recommended_tests":
                best_match.get(
                    "recommended_tests",
                    []
                ),

            "precautions":
                best_match.get(
                    "precautions",
                    []
                ),

            "specialists":
                best_match.get(
                    "recommended_specialists",
                    []
                ),

            "recommended_medications":
                best_match.get(
                    "recommended_medications",
                    []
                ),

            "emergency":
                best_match.get(
                    "emergency",
                    False
                ),

            "emergency_actions":
                best_match.get(
                    "emergency_actions",
                    []
                ),

            "survival_rate":
                best_match.get(
                    "survival_rate",
                    "Unknown"
                ),

            "estimated_recovery_days":
                best_match.get(
                    "estimated_recovery_days",
                    "Unknown"
                ),

            "ai_priority_score":
                best_match.get(
                    "ai_priority_score",
                    0
                )
        }

    except Exception as e:

        logger.error(
            f"❌ Prediction failed: {str(e)}"
        )

        return {

            "prediction":
                "Prediction Error",

            "confidence":
                "0%",

            "severity":
                "unknown",

            "description":
                "AI prediction failed.",

            "precautions":
                [],

            "error":
                str(e)
        }


# =========================================================
# AI HEALTH CHECK
# =========================================================

def predictor_health_check():

    """
    AI predictor diagnostics.
    """

    return {

        "status":
            "ACTIVE",

        "database_loaded":
            bool(
                disease_database.get(
                    "diseases"
                )
            ),

        "total_diseases":
            len(
                disease_database.get(
                    "diseases",
                    {}
                )
            )
    }