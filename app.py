




import requests
from flask import Flask, request, jsonify
from gemini_service import ask_gemini
import os
from dotenv import load_dotenv
from flask_cors import CORS

# ✅ Load environment variables
load_dotenv()

AISENSY_API_KEY = os.getenv("AISENSY_API_KEY")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

app = Flask(__name__)
CORS(app)

# ✅ Context Memory
context_memory = []


@app.route("/ask", methods=["POST"])
def ask():
    """Accept a JSON payload with {'question': 'user_question'} and return AI reply."""
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Call Gemini service
    answer = ask_gemini(question, context_memory[-10:])
    context_memory.append({"user": question, "ai": answer})
    if len(context_memory) > 10:
        context_memory.pop(0)

    return jsonify({"response": answer})


@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    """Accept a JSON payload {'phone': '...', 'message': '...'}."""
    payload = request.get_json()
    try:
        message = payload.get("message", "")
        phone = payload.get("phone", "")

        if not message or not phone:
            return jsonify({"error": "Missing phone or message"}), 400

        # Get AI reply
        answer = ask_gemini(message, context_memory[-10:])
        context_memory.append({"user": message, "ai": answer})
        if len(context_memory) > 10:
            context_memory.pop(0)

        # Here you can send this reply to WhatsApp or any external service
        print("Sample WhatsApp message to:", phone)
        print("Message:", answer)

        return jsonify({
            "status": "success",
            "sent_to": phone,
            "question": message,
            "bot_reply": answer
        })

        # If you want to send to Aisensy or any external service, you can
        # un-comment this block and use it:
        """
        response = requests.post(
            "https://backend.aisensy.com/campaign/t1/api",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {AISENSY_API_KEY}"
            },
            json={"phone": phone, "message": answer}
        )
        response.raise_for_status()
        return jsonify({"status": "sent", "message_id": response.json()}), 200
        """
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/context", methods=["GET"])
def get_context():
    """Return the conversation context."""
    return jsonify({"context": context_memory})


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
