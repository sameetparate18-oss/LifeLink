import os
import joblib

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "symptom_model.pkl"
)

model = joblib.load(MODEL_PATH)

def predict_disease(symptoms):

    prediction = model.predict([symptoms])

    return prediction[0]