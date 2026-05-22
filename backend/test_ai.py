from app.ai.disease_engine import process_disease_prediction

result = process_disease_prediction(
    "I have fever cough headache and weakness"
)

print(result)