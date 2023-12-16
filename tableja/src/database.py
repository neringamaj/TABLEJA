from typing import Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI
import json
from dotenv import load_dotenv, dotenv_values
import os
load_dotenv()
dotenv_values(".env")

client = QdrantClient("https://71b6c4a9-4a80-4ebb-8e75-eeeac394b2b3.us-east4-0.gcp.cloud.qdrant.io", api_key="QDRANT_API")
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
