from flask import Flask, request, jsonify, send_from_directory
import os
import ollama

app = Flask(__name__)

# Store chat history (for simplicity, use a database in production)
chat_history = []

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    response = ollama.chat(
        model="deepseek-r1:70b",
        messages=[{"role": "user", "content": user_message}]
    )
    
    print(f"User: {user_message}")
    print(f"Bot: {response['message']['content']}")
    return jsonify({"reply": response["message"]["content"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)