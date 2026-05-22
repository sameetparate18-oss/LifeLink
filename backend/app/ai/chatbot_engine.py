def generate_ai_response(

    symptoms,
    disease,
    confidence,
    emergency

):

    symptom_text = ", ".join(symptoms)

    response = f"""

Based on your symptoms like {symptom_text},

the possible condition may be {disease}.

Prediction confidence is {confidence}%.

Emergency Level: {emergency['severity']}.

{emergency['message']}.

Please consult a healthcare professional for proper diagnosis.

"""

    return response