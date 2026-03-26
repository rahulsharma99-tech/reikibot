import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Strong system prompt (prevents wrong answers)
SYSTEM_PROMPT = """
You are a chatbot for the website reikigyan.in.

Rules:
- Answer ONLY about Reiki courses, benefits, pricing, and general info
- Do NOT make up phone numbers, email, or address
- If user asks contact details, say: "Please visit the official website reikigyan.in"
- If you don't know something, say: "Please check the official website"
- Keep answers short and clear
"""

# Chat function (no shared memory)


def chat(user_message):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        max_tokens=120
    )

    return response.choices[0].message.content


# Chat API
@app.route("/chat", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        reply = chat(user_message)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Home route (for uptime check)
@app.route("/", methods=["GET"])
def home():
    return "Chatbot is running"


# Run server (Replit / hosting ready)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
