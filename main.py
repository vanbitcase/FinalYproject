from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__, template_folder="../templates")

GROQ_API_KEY = "YOUR_GROQ_API_KEY"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["POST"])
def chat():
    user_message = request.form["message"]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        bot_response = data['choices'][0]['message']['content']

        return jsonify({"response": bot_response})
    
    except Exception as e:
        return jsonify({"response": "Error processing your request."})

if __name__ == "__main__":
    app.run(debug=True)
