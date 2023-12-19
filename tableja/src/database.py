from typing import Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI
import json 
from dotenv import load_dotenv, dotenv_values
import os
from qdrant_client.http.models import Batch
import numpy as np
from qdrant_client.conversions.common_types import Filter


load_dotenv()
dotenv_values(".env")

client = QdrantClient("https://71b6c4a9-4a80-4ebb-8e75-eeeac394b2b3.us-east4-0.gcp.cloud.qdrant.io", api_key=os.getenv("QDRANT_API"))
client_openAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def upload_restaurant(embedding, id, name, address, rating, description, cuisine, priceRange):
    client.upsert(
        collection_name="restaurants",
        points=[
            models.PointStruct(
                id=id,
                payload={
                    "name": name,
                    "address": address,
                    "rating": rating,
                    "description": description,
                    "cuisine": cuisine,
                    "priceRange": priceRange,
                    "show": False,
                },
                vector=embedding,
            ),
        ],
    )

def get_most_similar_vector_id(query: str) -> json:
    # Generate the embedding for the query
    query_embedding = client_openAI.embeddings.create(model="text-embedding-ada-002", input=[query]).data[0].embedding


    search_results = client.search(
        collection_name="restaurants",
        query_vector=query_embedding,
        with_vectors=False,
        with_payload=True,
    )

    # Extract the ID of the most similar vector
    most_similar_vector_id = search_results[0] 
    json_results = [result for result in most_similar_vector_id]
    json_object = json.dumps(json_results, indent=4)
    json_object = json.loads(json_object)
    return json_object

def get_recommendations_from_database(user_preferences: dict) -> json:
    query = json.dumps(user_preferences)

    query_embedding = client_openAI.embeddings.create(
        model="text-embedding-ada-002", 
        input=[query]
    ).data[0].embedding

    search_results = client.search(
        collection_name="restaurants",
        query_vector=query_embedding,
        with_vectors=False,
        with_payload=True,
    )

    most_similar_vector_id = search_results[0] 
    json_results = [result for result in most_similar_vector_id]
    json_object = json.dumps(json_results, indent=4)
    json_object = json.loads(json_object)
    return json_object

""" 
    filtered_results = []
    for result in search_results:
        payload = result["payload"]
        if all(item in payload.items() for item in user_preferences.items()):
            filtered_results.append(payload)

    return filtered_results """

def is_location_not_in_database(city_name: str) -> bool:
   """ # Construct a filter with a generic dictionary structure
    city_filter = {
        "must": [
            {
                "key": "address",  # Specifying the key
                "match": {  # Assuming the match condition should be a dictionary
                    "MatchText": {  # Assuming a MatchText type is expected
                        "keyword": city_name  # The city name to match
                    }
                }
            }
        ]
    }

    # Perform the search query
    try:
        result = client.search(
            collection_name="restaurants",
            query_vector=[],  # Empty vector for non-vector-based search
            query_filter=city_filter,
            limit=10,
            with_payload=False  # Assuming we don't need to retrieve the payload
        )

        # Check if any matching results were found
        return len(result) == 0

    except Exception as e:
        print(f"An error occurred: {e}")
        return False """
   return False

users_collection = client.get_collection('users')

def update_user_preferences(user_id, preferences):
    try:
        preferences_payload = {key: {"type": "keyword", "value": value} for key, value in preferences.items()}
        dummy_vector = np.zeros(1536).tolist()

        response = client.upsert(
        collection_name="users",
        points=[
            models.PointStruct(
                id=user_id,
                payload=preferences_payload,
                vector=dummy_vector,
            ),
        ],
    )

        print("Upsert response:", response)  # Log the response
    except Exception as e:
        print(f"Error during upsert: {e}")


def get_user_preferences(user_id):
    """
    Fetch user preferences from the Qdrant database.
    """
    try:
        # Retrieve user preferences using Qdrant
        retrieved_data = client.retrieve(
            collection_name='users',  # Replace with your collection name
            ids=[user_id],
            with_payload=True
        )

        if retrieved_data:
            user_preferences = {key: value['value'] for key, value in retrieved_data[0].payload.items()}
            return user_preferences
        else:
            return None
    except Exception as e:
        print(f"Error fetching user preferences: {e}")
        return None




