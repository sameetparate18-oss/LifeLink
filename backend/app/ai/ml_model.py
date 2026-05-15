from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
import os

# ---------------- DATASET ----------------

data = {
    "fever": [1, 1, 0, 0],
    "cough": [1, 0, 1, 0],
    "headache": [1, 1, 0, 1],
    "disease": ["Flu", "Flu", "Cold", "Migraine"]
}

df = pd.DataFrame(data)

# ---------------- TRAIN ----------------

X = df.drop("disease", axis=1)
y = df["disease"]

model = RandomForestClassifier()

model.fit(X, y)

# ---------------- SAVE MODEL ----------------

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "symptom_model.pkl"
)

joblib.dump(model, MODEL_PATH)

print("Model trained successfully!")