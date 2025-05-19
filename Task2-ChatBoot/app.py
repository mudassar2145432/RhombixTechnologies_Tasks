from flask import Flask, jsonify, request, render_template
from transformers import pipeline
import random
import json
import boto3  # Needed to interact with Amazon Lex

app = Flask(__name__)

# Load intents
with open('intents.json') as file:
    intents = json.load(file)

# Dynamically extract all intent tags
labels = [intent['tag'] for intent in intents['intents']]

# Zero-shot classifier
classifier = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1")

# Initialize the Lex V2 client
client = boto3.client('lexv2-runtime', region_name='us-east-1')  # Change region if different

def get_lex_response(user_input):
    response = client.recognize_text(
        botId='EPA2HDLAI4',                 # Your Lex V2 bot ID
        botAliasId='TSTALIASID',           # Replace with your actual bot alias ID
        localeId='en_US',                  
        sessionId='user123',               
        text=user_input
    )
    if 'messages' in response and response['messages']:
        return response['messages'][0]['content']
    else:
        return "I'm not sure how to respond to that."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['GET'])
def get_bot_response():
    user_input = request.args.get('msg')
    response = get_lex_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
