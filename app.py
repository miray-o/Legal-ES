from flask import Flask, request, jsonify, render_template
from prolog_engine import handle_chat_message, reset_court

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    user_text = request.json.get('message')
    
    if user_text.lower() in ['reset', 'restart', 'clear']:
        reply = reset_court()
    else:
        # Send text to the engine and get the string response back
        reply = handle_chat_message(user_text)
        
    return jsonify({"reply": reply})