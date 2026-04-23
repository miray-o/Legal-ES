from flask import Flask, request, jsonify, render_template
from prolog_engine import handle_chat_message, reset_court
import os

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
@app.route('/')
def index():
    return render_template('index.html')
def ask():
    user_text = request.json.get('message')
    
    if user_text.lower() in ['reset', 'restart', 'clear']:
        reply = reset_court()
    else:
        # Send text to the engine and get the string response back
        reply = handle_chat_message(user_text)
        
    return jsonify({"reply": reply})

if __name__ == '__main__':
    # Use the port assigned by the platform, or default to 5000 for local dev
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)