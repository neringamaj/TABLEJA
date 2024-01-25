from flask import Flask, jsonify, request
from flask_cors import CORS
from src.postgre import get_restaurant
from bot import chat_with_bot

app = Flask(__name__)
CORS(app)

@app.route('/api/chatbot', methods=['POST'])
def chatbot_response():
    user_message = request.json.get('message', '')
    id = request.json.get('userID', '')
    result = chat_with_bot(user_message, id)

    return jsonify({"marker": result[0], "reply": result[3], "id": result[1]})

@app.route('/api/restaurants/<string:restaurant_id>', methods=['GET'])
def get_restaurant_details(restaurant_id):
    try:
        restaurant_details = get_restaurant(restaurant_id)
        if restaurant_details:
            
            return jsonify({"id": restaurant_details[0], "name": restaurant_details[1], "url": restaurant_details[2]})
        else:

            return jsonify({"error": "Restaurant not found"}), 404
    except Exception as e:
        print(f"Error fetching restaurant details: {e}")

        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/recommended', methods=['GET'])
def get_recommended_restaurants():
    recommended_ids = ["03d8c12f-86db-41e8-83aa-b20843754caf", "0da4ecbb-1e84-41fa-b6b6-e24d0b33d33a", "11bff774-5d52-4da4-af72-c89510fd2588", "17939b52-a096-4245-9a34-0fde1fb6aec3", "33c337a4-1cfa-4500-809f-ab3ad582cf46"]

    recommended_restaurants = [get_restaurant(restaurant_id) for restaurant_id in recommended_ids]

    recommended_restaurants = [
        {"id": restaurant[0], "name": restaurant[1], "url": restaurant[2]}
        for restaurant in recommended_restaurants if restaurant is not None
    ]

    return jsonify(recommended_restaurants)

if __name__ == '__main__':
    app.run(debug=True)