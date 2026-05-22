import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier

# ================= LOAD DATASET =================

df = pd.read_csv(
    "app/ai/dataset.csv"
)

# ================= FEATURES =================

X = df.drop(
    "disease",
    axis=1
)

# ================= TARGET =================

y = df["disease"]

# ================= MODEL =================

model = RandomForestClassifier(
    n_estimators=100
)

# ================= TRAIN =================

model.fit(X, y)

# ================= SAVE MODEL =================

joblib.dump(

    model,

    "app/ai/disease_model.pkl"

)

print("✅ Model Trained Successfully")