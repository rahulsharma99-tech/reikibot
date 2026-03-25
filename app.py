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

# Memory (shared for now - simple version)
messages = [
    {
        "role": "system",
        "content": "You are a chatbot for a Reikigyan website reikigyan.in. Answer about courses, benefits, pricing, and contact details in short."
    }
]

# Chat function (clean)


def chat(user_message):
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        max_tokens=100
    )

    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    return reply

# API endpoint


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


# Run server
if __name__ == "__main__":
    # app.run(debug=True)   #default code
    app.run(host="0.0.0.0", port=5000)  # changed for render
