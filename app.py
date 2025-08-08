from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS
import ollama  # For local LLM (replace if using API)

app = Flask(__name__)

# ===== CORS SETUP =====
# Option 1: Allow all origins (for development)
CORS(app)  # Basic global CORS

# Option 2: Restrict to specific origins (recommended for production)
# CORS(app, resources={
#     r"/chat": {"origins": ["http://localhost:5000", "http://your-frontend-domain.com"]}
# })

# ===== CHAT HISTORY =====
chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST", "OPTIONS"])  # Handle OPTIONS for preflight
def chat():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()  # Handle preflight
    
    user_message = request.json.get("message")
    
    # Local LLM (Ollama)
    response = ollama.chat(
        model="deepseek-llm",  # Replace with your model
        messages=[{"role": "user", "content": user_message}]
    )
    ai_response = response["message"]["content"]
    
    print(f"User: {user_message}")
    print(f"AI: {ai_response}")

    # Save to history
    chat_history.append({"user": user_message, "ai": ai_response})
    return _corsify_response(jsonify({"reply": ai_response}))

# ===== CORS HELPER FUNCTIONS =====
def _build_cors_preflight_response():
    response = jsonify({"status": "preflight"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

def _corsify_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)