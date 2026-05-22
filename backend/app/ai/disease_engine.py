from app.ai.symptom_processor import extract_symptoms

from app.ai.predictor import predict_disease

from app.ai.emergency_detector import detect_emergency

from app.ai.chatbot_engine import generate_ai_response

# ================= MAIN ENGINE =================

def process_disease_prediction(user_input):

    # STEP 1 — EXTRACT SYMPTOMS

    symptoms = extract_symptoms(user_input)

    # STEP 2 — PREDICT DISEASE

    prediction = predict_disease(symptoms)

    # STEP 3 — DETECT EMERGENCY

    emergency = detect_emergency(symptoms)

    # STEP 4 — GENERATE AI RESPONSE

    ai_response = generate_ai_response(

        symptoms,

        prediction["disease"],

        prediction["confidence"],

        emergency

    )

    # STEP 5 — FINAL RESPONSE

    return {

        "symptoms_detected": symptoms,

        "predicted_disease": prediction["disease"],

        "confidence": prediction["confidence"],

        "severity": emergency["severity"],

        "ai_response": ai_response

    }
