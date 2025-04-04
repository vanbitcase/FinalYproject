from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")  # Use environment variable if available
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {GROQ_API_KEY}"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def send():
    user_message = request.form.get("message", "")

    if not user_message:
        return jsonify({"response": "Please enter a message."})

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        bot_response = data.get("choices", [{}])[0].get("message", {}).get("content", "Error getting response.")
    except requests.exceptions.RequestException as e:
        bot_response = f"API Error: {e}"
    except KeyError:
        bot_response = "Unexpected response format from API."
    print(bot_response)
    return jsonify({"response": bot_response})

# This is important for Vercel
app = app.wsgi_app

if __name__ == "__main__":
    app.run(debug=True)
