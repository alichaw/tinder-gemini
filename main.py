# main.py

import os
from dotenv import load_dotenv
from data_processing import upload_and_prepare_context
from tinder_api import TinderAPI
import google.generativeai as genai
import datetime

def configure_gemini_api(api_key):
    """Configure the Gemini API."""
    genai.configure(api_key=api_key)

def generate_chat_response(query, context, uploaded_files, chat=None):
    """Generate a chat response using Gemini API."""
    if chat is None:
        # Start a new chat session
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(
            history=[
                {"role": "user", "parts": [f"Use the following context to respond as if chatting on Tinder just chinese: {context}."]},
                {"role": "user", "parts": [f"The following files are uploaded: {', '.join(uploaded_files)}."]}
            ]
        )

    # Send the query message
    response = chat.send_message(query, stream=True)
    generated_text = ""
    for chunk in response:
        generated_text += chunk.text
    return generated_text, chat


def main():
    # Load environment variables
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    TINDER_API_TOKEN = os.getenv("TINDER_API_TOKEN")

    # Configure APIs
    configure_gemini_api(GEMINI_API_KEY)
    tinder_api = TinderAPI(TINDER_API_TOKEN)

    # Load and upload data
    context_folder = "data"
    context, uploaded_files = upload_and_prepare_context(context_folder)

    # Fetch Tinder profile
    profile = tinder_api.profile()
    user_id = profile['data']['user']['_id']
    print(f"My Profile: {profile['data']['user']['name']}\n")

    # Fetch matches
    matches = tinder_api.matches(limit=10)
    print(f"Found {len(matches)} matches.\n")

    # Process each match
    chat_instance = None
    for match in matches:
        match_id = match["id"]
        person_name = match["person"]["name"]
        print(f"Chatting with {person_name}...")

        # Get messages from the match
        messages = tinder_api.get_messages(match_id)
        new_messages = []
        for message in reversed(messages):
            if message["from"] != user_id:
                new_messages.append(message["message"])
                break

        if new_messages:
            user_query = new_messages[0]
            print(f"Latest message from {person_name}: {user_query}")

            # Generate response using Gemini API
            response_text, chat_instance = generate_chat_response(user_query, context, uploaded_files, chat=chat_instance)
            print(f"Generated Response: {response_text}")

            # Send the response back on Tinder
            tinder_api.send_message(match_id, response_text)
            print(f"Message sent to {person_name}.\n")
        else:
            print(f"No new messages from {person_name}.\n")

if __name__ == "__main__":
    main()
