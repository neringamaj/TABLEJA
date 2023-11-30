from openai import OpenAI
from database import upload_restaurant
import uuid
from dotenv import load_dotenv, dotenv_values
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set up your OpenAI API credentials


def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

# Example usage
query = input("Restaurant description: ")

id = str(uuid.uuid4())
name = input("Restaurant name: ")
address = input("Restaurant address: ")
rating = input("Restaurant rating: ")
cuisine = input("Restaurant cuisine: ")
price = input("Restaurant price range: ")

query += " " + name + " " + address + " " + rating + " " + cuisine + " " + price


embedding = get_embedding(query)

upload_restaurant(embedding, id, name, address, rating, query, cuisine, price)