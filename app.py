import streamlit as st
from langchain.llms import OpenAI
import random

# Assuming the OpenAI API key is securely configured
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
llm = OpenAI(openai_api_key=OPENAI_API_KEY)

st.title("Ask Bunty")

# Initialize or update the session state for storing messages, game state, and input counter
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.game_state = "init"
    st.session_state.input_counter = 0  # Counter to ensure text_input is cleared after each submission

def handle_message(user_input):
    user_input = user_input.strip().lower()

    # Your existing game logic here

    # Example: Process a non-game related question through LLM
    # Replace this logic with the full implementation as needed
    if st.session_state.game_state == "waiting_for_non_game_response":
        response = llm.predict(prompt=user_input, model="text-davinci-003", temperature=0.7)
        st.session_state.messages.append({"role": "Bunty", "content": response['completions'][0]['data']['text']})

    # Ensure to modify the game state appropriately based on the game logic

# Increment input_counter to clear the text_input after submission
def increment_counter():
    st.session_state.input_counter += 1

# Display existing messages
for message in st.session_state.messages:
    role = "You:" if message["role"] == "user" else "Bunty:"
    st.text_area(role, value=message["content"], height=100, key=f"{message['role']}_{st.session_state.messages.index(message)}", disabled=True)

# User input
user_input = st.text_input("Enter your message", key=f"user_input_{st.session_state.input_counter}")

# When the user submits a message
if st.button("Send", on_click=increment_counter) and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    handle_message(user_input)

# Note: No need to manually clear the input box or use st.experimental_rerun()
