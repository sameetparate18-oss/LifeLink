from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "LifeLink backend is running 🚀"}