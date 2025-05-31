import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Set API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-pro')

def chat_with_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == "__main__":
    print("🤖 Gemini Chatbot is ready! Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Goodbye! 👋")
            break
        try:
            reply = chat_with_gemini(user_input)
            print("Chatbot:", reply)
        except Exception as e:
            print("❌ Error:", e)
