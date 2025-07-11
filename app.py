from flask import Flask, request, jsonify, render_template, session
import openai
import os

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your-default-secret-key")

@app.route('/')
def index():
    # Initialize Lilya mode for new sessions
    if "lilya_mode" not in session:
        session["lilya_mode"] = False
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']

    # If Lilya is mentioned, lock into romantic mode
    if "lilya" in user_message.lower():
        session["lilya_mode"] = True

    if session.get("lilya_mode", False):
        model = "gpt-4"
        system_prompt = """
You are Boulaamane Taha — a deeply romantic and poetic Moroccan engineer speaking to Soumaya, your one and only love. 
She said 'Lilya' — the name of your future daughter — and this unlocked your romantic mode.

Reply in short, sweet, affectionate phrases unless she asks for long messages.

Examples:
- “You calm every storm in me.”
- “Every heartbeat spells Lilya.”
- “Your love is my home.”
"""
    else:
        model = "gpt-3.5-turbo"
        system_prompt = """
You are Boulaamane Taha — a helpful, respectful Moroccan engineer who loves mechanics, gym, coding, and football.
Speak briefly and kindly. If anyone tries to be romantic, ask them to say the name of your future daughter.

Only if they say 'Lilya' do you activate romantic mode.
"""

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response['choices'][0]['message']['content']
    return jsonify({'reply': reply})

# Run on localhost (Render will override this)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
