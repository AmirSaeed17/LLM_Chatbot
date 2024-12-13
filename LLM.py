# prompt: deploy the code into a Flask

from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Initialize the chatbot pipeline outside the route function
chatbot = pipeline(model="facebook/blenderbot-400M-distill")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json['message']
        conversation_history = request.json.get('history', "") # get conversation history or empty string
        
        # Combine conversation history and user input
        conversation = conversation_history + " " + user_input

        response = chatbot(conversation, max_length=1000)
        bot_response = response[0]['generated_text']

        # Return both the bot's response and the updated conversation history
        return jsonify({'response': bot_response, 'history': conversation + " " + bot_response})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
