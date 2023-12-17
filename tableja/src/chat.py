from anyio import sleep
from openai import OpenAI
from dotenv import load_dotenv, dotenv_values
from src.database import get_most_similar_vector_id
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
        response = get_openai_response(
            f"USER INPUT LANGUAGE: LITHUANIAN. RESPONSE LANGUAGE: ENGLISH. This is restaurant reservation chatbot user input. User defined location where he would like to eat: {user_input}. Extract the location as accurate as possible including city, district or part of the city, key landmark or exact address. Do not include country name. Do not include any additional information. Do not use commas.")
        query = "Restaurant address: " + response
        print(response)
        # Getting location preference
        user_input = str(
            input("What is your preferred restaurant price range from 1 to 3?"))
        response = get_openai_response(
            f"USER INPUT LANGUAGE: LITHUANIAN. RESPONSE LANGUAGE: ENGLISH. User defined price preference: {user_input}. Return the following number according to user price input: 1 - cheap, budget friendly, 2 - medium, 3 - expensive, luxury. Only choose one of the three options and return just a number.")
        query += "Price level: " + response
        print(response)
        # Getting price preference
        user_input = str(input("What is your preferred restaurant cuisine?"))
        response = get_openai_response(
            f"User input language: LITHUANIAN. RESPONSE LANGUAGE: ENGLISH. Based on user prefered cuisine: {user_input}, return 2 keywords that define this cuisine. First of them must be name of cuisine and second one must be most popular dish of this cuisine.")
        query += "Restaurant cuisine: " + response
        print(response)
        # Additional requirements
        user_input = str(input("Do you have any additional requirements?"))
        response = get_openai_response(
            f"User input language: LITHUANIAN. RESPONSE LANGUAGE: ENGLISH. User defined additional requirements: {user_input}. If user expressed some additional requirements, extract 1 keyword from it. If not, return empty string.")
        query += "About: " + response

        print(response)

        id = get_most_similar_vector_id(query)
        print(id)

        break


# chat_flow()


def get_data_flow(data):
    query = ""

    response = get_openai_response(
        f"USER INPUT LANGUAGE: LITHUANIAN. RESPONSE LANGUAGE: ENGLISH. This is restaurant reservation chatbot user input. User defined location where he would like to eat: {data[1]}. Extract the location as accurate as possible including city, district or part of the city, key landmark or exact address. Do not include country name. Do not include any additional information. Do not use commas.")
    query += "Restaurant address: " + response
    print(response)
    response = get_openai_response(
        f"USER INPUT LANGUAGE: LITHUANIAN. RESPONSE LANGUAGE: ENGLISH. User defined price preference: {data[2]}. Return the following number according to user price input: 1 - cheap, budget friendly, 2 - medium, 3 - expensive, luxury. Only choose one of the three options and return just a number.")
    query += "Price level: " + response
    print(response)
    response = get_openai_response(
        f"User input language: LITHUANIAN. RESPONSE LANGUAGE: ENGLISH. Based on user prefered cuisine: {data[3]}, return 2 keywords that define this cuisine. First of them must be name of cuisine and second one must be most popular dish of this cuisine. Do not include any other information")
    query += "Restaurant cuisine: " + response
    print(response)
    # response = get_openai_response(
    #     f"User input language: LITHUANIAN. RESPONSE LANGUAGE: ENGLISH. User defined additional requirements: {data[4]}. If user expressed some additional requirements, extract 1 keyword from it. If not, return empty string.")
    # query += "About: " + response
    print(query)
    result = get_most_similar_vector_id(query)

    return result


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


# chat_flow()
