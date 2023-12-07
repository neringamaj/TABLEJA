import requests
import json
from src.database import upload_restaurant
from src.postgre import insert_restaurant
from openai import OpenAI
from uuid import uuid4
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
api_key=os.getenv("MAPS_API_KEY")

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding


def get_restaurants(api_key, location, radius):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        'location': location,
        'radius': radius,
        'type': 'restaurant',
        'key': api_key
    }
    res = requests.get(endpoint_url, params=params)
    results = []
    if res.status_code == 200:
        restaurants = res.json()['results']
        for restaurant in restaurants:
            place_id = restaurant.get("place_id")
            details = get_place_details(api_key, place_id) if place_id else {}
            if details:  # Include if details are available

                unique_id = uuid4()
                restaurant_info = {
                    'Name': restaurant.get('name'),
                    'Address': restaurant.get('vicinity'),
                    'Rating': restaurant.get('rating'),
                    'Price Level': restaurant.get('price_level'),
                    'Photo': get_photo_url(api_key, restaurant.get('photos', [{}])[0].get('photo_reference')) if restaurant.get('photos') else 'No photo available',
                    'Website': details.get('website', 'No website available'),
                    'About': details.get('about', 'No about section available'),
                    'Working Hours': details.get('working_hours', 'No working hours available'),
                    'Cuisine': details.get('cuisine', 'Cuisine not specified')
                }
                results.append(restaurant_info)
                query = f"Restaurant name: {restaurant_info['Name']}\nRestaurant address: {restaurant_info['Address']}\nRestaurant rating: {restaurant_info['Rating']}\nRestaurant price level: {restaurant_info['Price Level']}\n Restaurant cuisine: {restaurant_info['Cuisine']}\n Restaurant about: {restaurant_info['About']}\n"
                upload_restaurant(get_embedding(query), str(unique_id), restaurant_info['Name'], restaurant_info['Address'], restaurant_info['Rating'], restaurant_info['About'], restaurant_info['Cuisine'], restaurant_info['Price Level'])
                insert_restaurant(unique_id, restaurant_info['Name'], restaurant_info['Photo'])
    return results

def get_place_details(api_key, place_id):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
    fields = [
        'business_status', 'types', 'curbside_pickup', 'delivery', 'dine_in', 'opening_hours', 
        'reservable', 'serves_beer', 'serves_breakfast', 'serves_brunch', 'serves_dinner', 
        'serves_lunch', 'serves_vegetarian_food', 'serves_wine', 'takeout', 
        'wheelchair_accessible_entrance', 'website'
    ]
    params = {
        'place_id': place_id,
        'fields': ','.join(fields),
        'key': api_key
    }
    res = requests.get(endpoint_url, params=params)
    if res.status_code == 200:
        result = res.json().get('result', {})
        about_parts = []
        for field in fields[:-1]:  # Exclude 'website' field from this loop
            if result.get(field) is True:
                about_parts.append(field.replace('_', ' ').capitalize())

        working_hours = "Working Hours: Not available"
        if 'opening_hours' in result and 'weekday_text' in result['opening_hours']:
            working_hours = "Working Hours: " + ', '.join(result['opening_hours']['weekday_text'])

        types = result.get('types', [])
        cuisine_types = [t for t in types if 'restaurant' in t]
        return {
            'website': result.get('website', 'No website available'),
            'about': ' | '.join(about_parts),
            'working_hours': working_hours,
            'cuisine': ', '.join(cuisine_types) if cuisine_types else 'Cuisine not specified'
        }
    return None

def get_photo_url(api_key, photo_reference):
    if photo_reference:
        return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
    return 'No photo available'


location = '54.89701840237929, 23.92111125040317' 
radius = 1000  

restaurants = get_restaurants(api_key, location, radius)

with open('restaurants_info.txt', 'w', encoding='utf-8') as file:
    for restaurant in restaurants:
        for key, value in restaurant.items():
            file.write(f"{key}: {value}\n")
        file.write("\n----------------------\n")

print("Data written to restaurants_info.txt")

with open('restaurants_info.json', 'w', encoding='utf-8') as json_file:
    json.dump(restaurants, json_file, indent=4, ensure_ascii=False)

print("Data written to restaurants_info.json")