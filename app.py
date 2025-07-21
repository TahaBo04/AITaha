from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Set your API key cleanly — no proxies involved
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Please send JSON with a 'message' field."}), 400

        user_message = data["message"]

        response = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are Boulaamane Taha, helpful and romantic."},
                {"role": "user", "content": user_message}
            ]
        )

        return jsonify({"reply": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
