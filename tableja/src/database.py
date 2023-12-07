
from typing import Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from postgre import insert_restaurant
from openai import OpenAI
import json
from dotenv import load_dotenv, dotenv_values
import os
load_dotenv()
dotenv_values(".env")

client = QdrantClient("localhost", port=6333)
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
                },
                vector=embedding,
            ),
        ],
    )
    insert_restaurant(id, name)


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
