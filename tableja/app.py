from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from src.database import get_most_similar_vector_id

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
    result = get_most_similar_vector_id(user_message)

    return jsonify({"reply": result[3]})

if __name__ == '__main__':
    app.run(debug=True)