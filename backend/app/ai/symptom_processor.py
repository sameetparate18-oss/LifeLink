import re

# ================= MEDICAL SYMPTOMS =================

MEDICAL_SYMPTOMS = [

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

# ================= CLEAN TEXT =================

def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z\s]", "", text)

    return text

# ================= EXTRACT SYMPTOMS =================

def extract_symptoms(user_input):

    text = clean_text(user_input)

    found = []

    for symptom in MEDICAL_SYMPTOMS:

        if symptom in text:

            found.append(symptom)

    return found