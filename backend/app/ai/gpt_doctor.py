from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are a medical AI assistant.

Rules:
- Do NOT claim to be a real doctor
- Give safe educational advice only
- Suggest consulting a doctor for serious symptoms
- Provide possible conditions, not final diagnosis
"""

def gpt_medical_chat(message: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ]
    )

    return response.choices[0].message.content