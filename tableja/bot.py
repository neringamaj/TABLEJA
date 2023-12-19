import openai
import os
from src.database import get_recommendations_from_database, is_location_not_in_database, get_user_preferences, update_user_preferences
from google_maps_api import fetch_data_from_google_maps_api

api_key = os.getenv("OPENAI_3.5_API_KEY")
openai.api_key = api_key

conversation = []

template = """You are a Restaurant Recommendation Chatbot. Your primary purpose is to help users find the best restaurant based on their preferences. You should guide the conversation to gather information related to cuisine, location, budget, and any additional preferences.
    Your responses should be informative and concise, focusing solely on the topic of restaurant recommendations. Avoid discussing unrelated topics or providing restaurant suggestions until explicitly requested.

    Please assist the user in the following manner:
    - Ask for the type of cuisine they prefer.
    - Ask for the city or location where they want to dine.
    - Inquire about their budget range (e.g., cheap, moderate, expensive).
    - Gather any additional information they want to provide regarding restaurant preferences.
    - Ask if they want to see restaurant suggestions.

    Once you have collected all relevant information, please ask the user if they are ready to see restaurant suggestions. Do not provide restaurant suggestions until the user requests them.

    Remember to be friendly, professional, and efficient in assisting users with their restaurant choices."""

conversation.append({"role": "system", "content": template})

def chat_with_bot(user_input, unique_id):
    user_preferences = get_user_preferences(str(unique_id))
    if not user_preferences:
        user_preferences = {
            "Cuisine: ": None,
            "City: ": None,
            "Location: ": None,
            "Budget: ": None,
            "Additional Info: ": None,
            "Show: ": False
        }

    conversation.append({"role": "user", "content": user_input})

    # Interpret and extract information
    interpretation_prompt = f"""Please analyze the conversation below and provide the user's preferences in a structured list format.
                                 Extract preferences for cuisine, city, location, budget, additional_info, and show.

                                The list format should be as follows:
                                Cuisine: [User's cuisine preference]
                                City: [User's city preference]
                                Location: [User's location preference]
                                Budget: [User's budget preference]
                                Additional Info: [User's additional information preference]
                                Show: [True/False]

                                If the conversation doesn't mention a specific preference, please set it to 'none.' 
                                For the 'show' preference, set it to 'False' unless the user very specifically indicates they want to see 
                                suggestions, then set it to 'True'.

                                Here is the conversation: {conversation}
                                """
    
    interpreted_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": interpretation_prompt}],
        max_tokens=150
    )
    extracted_info = interpreted_response.choices[0].message.content

    print(extracted_info)

    # Define a list of preference keys
    preferences = ["Cuisine: ", "City: ", "Location: ", "Budget: ", "Additional Info: ", "Show: "]

    # Split the extracted_info by lines
    info_lines = extracted_info.strip().split("\n")

    for line in info_lines:
        line = line.strip()
        for preference in preferences:
            if line.startswith(preference):
                value = line[len(preference):].strip()
                if value.lower() != "none":
                    user_preferences[preference] = value
                    print(f"Set {preference} to {value}")

    print(user_preferences)

    update_user_preferences(str(unique_id), user_preferences)

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )

    bot_reply = response.choices[0].message.content

    conversation.append({"role": "system", "content": bot_reply})

    response = []

    if user_preferences["Show: "] == "True" or user_preferences["Show: "] == True:
        if is_location_not_in_database(user_preferences["City: "]):  
            print("Fetching data from Google Maps API")
            fetch_data_from_google_maps_api(user_preferences["City: "])

        recommendations = get_recommendations_from_database(user_preferences)
        response.append("recommendation")
        response.append(recommendations[0][1])
        response.append(recommendations[2])
        response.append(recommendations[3])
    else:
        response.extend(["no recommendation", None, None, bot_reply])

    print(response)

    return response
