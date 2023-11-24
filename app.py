from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

def get_random_restaurants(count, category="restaurant"):
    base_url = "https://source.unsplash.com/random/?"
    return [{"id": i, "name": f"{category.title()} #{i}", "image": f"{base_url}/{category}/{i}"} for i in range(1, count + 1)]

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    suggestions = get_random_restaurants(12, "restaurant")
    visited = get_random_restaurants(6, "visited")
    return jsonify({"suggestions": suggestions, "visited": visited})

@app.route('/api/chatbot', methods=['POST'])
def chatbot_response():
    user_message = request.json.get('message', '')
    # Here you would integrate with a real chatbot service to process the message
    # For now, we'll just echo the message back
    bot_response = f"I received your message: {user_message}"
    return jsonify({"reply": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
