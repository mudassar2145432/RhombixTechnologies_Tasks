from flask import Flask, jsonify, request, render_template
from transformers import pipeline
import random
import json

app = Flask(__name__)

# Load intents
with open('intents.json') as file:
    intents = json.load(file)

# Dynamically extract all intent tags
labels = [intent['tag'] for intent in intents['intents']]

# Zero-shot classifier
classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1")

def get_response(user_input):
    user_input = user_input.lower()
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in user_input:
                return random.choice(intent['responses'])
    return "I'm not sure I understood that. Could you rephrase or ask in a different way?"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['GET'])
def get_bot_response():
    user_input = request.args.get('msg')
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
