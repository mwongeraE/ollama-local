# backend.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat"  # Replace if needed

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    response = requests.post(
        DEEPSEEK_API_URL,
        json={"message": user_message},
        headers={"Authorization": "Bearer YOUR_API_KEY"}
    )
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)