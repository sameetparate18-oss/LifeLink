import tkinter as tk
from tkinter import messagebox
import requests

# =========================
# WINDOW SETUP
# =========================
root = tk.Tk()
root.title("🩺 AI Disease Prediction System")
root.geometry("600x500")
root.configure(bg="#f5f7fa")

# =========================
# TITLE
# =========================
title = tk.Label(
    root,
    text="🩺 AI Disease Prediction",
    font=("Arial", 22, "bold"),
    bg="#f5f7fa",
    fg="#222"
)
title.pack(pady=20)

# =========================
# INSTRUCTION
# =========================
instruction = tk.Label(
    root,
    text="Describe your symptoms in plain English\nExample: I have fever, cough and body pain",
    font=("Arial", 12),
    bg="#f5f7fa",
    fg="#555"
)
instruction.pack(pady=10)

# =========================
# INPUT BOX
# =========================
symptom_entry = tk.Entry(
    root,
    width=60,
    font=("Arial", 14)
)
symptom_entry.pack(pady=15, ipady=8)

# =========================
# RESULT BOX
# =========================
result_box = tk.Text(
    root,
    height=15,
    width=70,
    font=("Arial", 11),
    bg="white"
)
result_box.pack(pady=20)

# =========================
# PREDICT FUNCTION
# =========================
def predict():

    symptoms = symptom_entry.get()

    if not symptoms.strip():
        messagebox.showerror("Error", "Please enter symptoms")
        return

    try:

        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json={
                "text": symptoms
            }
        )

        data = response.json()

        result_box.delete("1.0", tk.END)

        output = f"""
==============================
AI DISEASE PREDICTION RESULT
==============================

📝 Symptoms:
{data['input_symptoms']}

🦠 Predicted Disease:
{data['predicted_disease']}

📊 Confidence:
{data['confidence']}

⚠ Risk Level:
{data['risk_level']}

🚨 Emergency:
{data['emergency']}

👨‍⚕ Recommended Doctor:
{data['recommended_doctor']}

💡 Medical Advice:
{data['medical_advice']}

📈 All Probabilities:
"""

        for disease, prob in data["all_probabilities"].items():
            output += f"\n- {disease}: {prob}%"

        result_box.insert(tk.END, output)

    except Exception as e:
        messagebox.showerror("Server Error", str(e))

# =========================
# PREDICT BUTTON
# =========================
predict_btn = tk.Button(
    root,
    text="Predict Disease",
    font=("Arial", 14, "bold"),
    bg="#007bff",
    fg="white",
    padx=20,
    pady=10,
    command=predict
)
predict_btn.pack(pady=10)

# =========================
# RUN APP
# =========================
root.mainloop()