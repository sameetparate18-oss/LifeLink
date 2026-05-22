import joblib
import pandas as pd

# ================= LOAD MODEL =================

model = joblib.load(
    "app/ai/disease_model.pkl"
)

# ================= ALL SYMPTOMS =================

all_symptoms = [

    "fever",
    "cough",
    "headache",
    "vomiting",
    "nausea",
    "fatigue",
    "weakness",
    "body pain",
    "sore throat",
    "cold",
    "dizziness",
    "diarrhea",
    "chest pain",
    "breathing problem",
    "shortness of breath",
    "stomach pain"

]

# ================= PREDICT FUNCTION =================

def predict_disease(symptoms):

    vector = {}

    for symptom in all_symptoms:

        if symptom in symptoms:
            vector[symptom] = 1
        else:
            vector[symptom] = 0

    # Convert to DataFrame
    input_data = pd.DataFrame([vector])

    # Prediction
    disease = model.predict(input_data)[0]

    # Confidence
    probability = max(
        model.predict_proba(input_data)[0]
    )

    return {

        "disease": disease,

       "confidence": float(
    round(probability * 100, 2)
)
    }