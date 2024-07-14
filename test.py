import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()
api = os.getenv('gemini_api_key')
genai.configure(api_key = api)
model = genai.GenerativeModel(model_name="gemini-pro")
user = input("Enter your query here:")
response = model.generate_content(user)
print(response.text)