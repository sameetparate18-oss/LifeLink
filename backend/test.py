from google import genai

client = genai.Client(
    api_key="AIzaSyBXiH3YYulP5ZhZxLqK4cdb6W5i87iPcgc"
)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Hello"
)

print(response.text)