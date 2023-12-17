from anyio import sleep
from openai import OpenAI
from dotenv import load_dotenv, dotenv_values
from database import get_most_similar_vector_id
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_openai_response(prompt):
    """
    This function sends a prompt to the OpenAI API and returns the response.
    """
    try:
        response = client.completions.create(
          model="text-davinci-003",
          prompt=prompt,
          max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def chat_flow():
  print("Welcome to the Restaurant Finder Chatbot!")
  user_input = ""

  query = ""
  # Example of a conversation flow
  while True:
    # Asking about cuisine preference
    user_input = str(input("What are your location preferences?"))
    response = get_openai_response(f"Based on {user_input}, extract the location.")
    query = "Restaurant address: " + response

    # Getting location preference
    user_input = str(input("What is your preferred restaurant price range from 1 to 3?"))
    response = get_openai_response(f"Based {user_input}, extract the price range from 1 to 3. YOU CAN ONLY CHOOSE FROM 1 TO 3. 1 would be the cheapest and 3 would be the most expensive.")
    query += "Price level: " + response

    # Getting price preference
    user_input = str(input("What is your preferred restaurant cuisine?"))
    response = get_openai_response(f"Based on {user_input}, extract the cuisine.")
    query += "Restaurant cuisine: " + response

    # Additional requirements
    user_input = str(input("Do you have any additional requirements?"))
    response = get_openai_response(f"Based on {user_input}, extract the additional requirements.")
    query += "About: " + response


    print(query)

    id = get_most_similar_vector_id(query)
    print(id)

    break

# def ask_question(prompt):
#     response = client.chat.completions.create(model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly."},
#         {"role": "user", "content": prompt}
#     ])
#     return response.choices[0]

# restaurant_cuisine = ask_question("What is the restaurant's cuisine?")

# print(restaurant_cuisine)


# assistant = client.beta.assistants.create(
#   instructions="You are a restaurant information assistant. You need to ask the user questions to collect all the necessary information about the users needs. After collecting all the necessary information you will call the getEmbedding function to get the embedding of the user's input.",
#   model="gpt-4-1106-preview",
#   tools=[{
#       "type": "function",
#     "function": {
#       "name": "getEmbedding",
#       "description": "Get the embedding of the user's input",
#       "parameters": {
#         "type": "object",
#         "properties": {

#         },
#         "required": []
#       }
#     }
#   }]
# )

# def get_most_similar_vector_id(query: str):
#     # Generate the embedding for the query
#     query_embedding = client.embeddings.create(model="text-embedding-ada-002", input=[query]).data[0].embedding


#     search_results = client.search(
#         collection_name="restaurants",
#         query_vector=query_embedding,
#         with_vectors=False,
#         with_payload=True,
#     )

#     # Extract the ID of the most similar vector
#     most_similar_vector_id = search_results[0] 
#     json_results = [result for result in most_similar_vector_id]
#     json_object = json.dumps(json_results, indent=4)
#     json_object = json.loads(json_object)
#     return json_object



chat_flow()