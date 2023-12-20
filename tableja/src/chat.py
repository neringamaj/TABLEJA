from openai import OpenAI
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_question(prompt):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  {"role": "system", "content": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."},
                                                  {"role": "user",
                                                      "content": prompt}
                                              ])
    return response.choices[0]


restaurant_cuisine = ask_question("What is the restaurant's cuisine?")

print(restaurant_cuisine)


assistant = client.beta.assistants.create(
    instructions="You are a restaurant information assistant. You need to ask the user questions to collect all the necessary information about the users needs. After collecting all the necessary information you will call the getEmbedding function to get the embedding of the user's input.",
    model="gpt-4-1106-preview",
    tools=[{
        "type": "function",
        "function": {
          "name": "getEmbedding",
          "description": "Get the embedding of the user's input",
          "parameters": {
              "type": "object",
              "properties": {

              },
              "required": []
          }
        }
    }],
    max_tokens=2000,
)


def get_most_similar_vector_id(query: str) -> json:
    # Generate the embedding for the query
    query_embedding = client.embeddings.create(
        model="text-embedding-ada-002", input=[query]).data[0].embedding

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
