from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from src.database import get_most_similar_vector_id
from src.postgre import get_restaurant

app = Flask(__name__)
CORS(app)

@app.route('/api/chatbot', methods=['POST'])
def chatbot_response():
    user_message = request.json.get('message', '')
    result = get_most_similar_vector_id(user_message)

    return jsonify({"reply": result[3], "id": result[0][1]})

@app.route('/api/restaurants/<string:restaurant_id>', methods=['GET'])
def get_restaurant_details(restaurant_id):
    try:
        restaurant_details = get_restaurant(restaurant_id)
        print(restaurant_details[2])
        print(jsonify(restaurant_details))
        if restaurant_details:
            return jsonify({"id": restaurant_details[0], "name": restaurant_details[1], "url": restaurant_details[2]})
        else:
            return jsonify({"error": "Restaurant not found"}), 404
    except Exception as e:
        print(f"Error fetching restaurant details: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)