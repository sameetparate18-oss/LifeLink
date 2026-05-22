# ================= CRITICAL SYMPTOMS =================

critical_symptoms = [

    "chest pain",
    "breathing problem",
    "shortness of breath"

]

high_symptoms = [

    "high fever",
    "vomiting",
    "dizziness"

]

# ================= DETECTOR =================

def detect_emergency(symptoms):

    for symptom in symptoms:

        if symptom in critical_symptoms:

            return {

                "severity": "Critical",

                "message": "Immediate medical attention required"

            }

    for symptom in symptoms:

        if symptom in high_symptoms:

            return {

                "severity": "High",

                "message": "Consult doctor soon"

            }

    return {

        "severity": "Normal",

        "message": "Condition appears stable"

    }