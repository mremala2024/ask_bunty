import streamlit as st
from langchain.llms import OpenAI

# Load the OpenAI API key, assuming it's set as an environment variable
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else None

if OPENAI_API_KEY is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY in your Streamlit secrets.")
    st.stop()

llm = OpenAI(openai_api_key=OPENAI_API_KEY)

st.title("Ask Bunty")

# Initialize or update the session state for storing messages and game state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.game_state = "init"

def handle_message(user_input):
    # Check the current state of the conversation/game and respond accordingly
    if st.session_state.game_state == "init":
        st.session_state.messages.append({"role": "Bunty", "content": "Hello, I'm Bunty! Do you want to play the Monty Hall game? (Yes/No)"})
        st.session_state.game_state = "waiting_for_game_start"
    elif user_input.strip().lower() == "yes" and st.session_state.game_state == "waiting_for_game_start":
        st.session_state.messages.append({"role": "Bunty", "content": "Great! Choose a door: 1, 2, or 3."})
        st.session_state.game_state = "choosing_door"
    # Insert additional game logic here
    else:
        # For non-game related questions or if game state doesn't match any known condition,
        # use OpenAI to generate a response.
        response = llm.predict(user_input)
        st.session_state.messages.append({"role": "Bunty", "content": response})

# Display existing messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.text_area("You:", value=message["content"], height=100, key=f"user_{st.session_state.messages.index(message)}", disabled=True)
    else:  # Bunty's messages
        st.text_area("Bunty:", value=message["content"], height=100, key=f"assistant_{st.session_state.messages.index(message)}", disabled=True)

# User input
user_input = st.text_input("Enter your message", "")

# When the user submits a message
if st.button("Send") and user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Handle the message based on game state or forward to OpenAI
    handle_message(user_input)

    # Clear the input box after sending the message
    st.experimental_rerun()
