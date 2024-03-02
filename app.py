import streamlit as st
import random
from langchain.llms import OpenAI

# Assuming OPENAI_API_KEY is set in Streamlit's secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Initialize LangChain's OpenAI with the API key
llm = OpenAI(openai_api_key=OPENAI_API_KEY)

# Setup page
st.set_page_config(page_title="Monty Hall Game with OpenAI Integration", page_icon="🚪")

st.title("Talk to Bunty about anything!")

# Initialize session state if not already present
if 'stage' not in st.session_state:
    st.session_state.stage = "welcome"
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    st.text_area(label="", value=message, height=75, disabled=True)

# User input
user_input = st.text_input("Type your message here...", key="user_input")

def process_input(user_input):
    # If the stage is not within the Monty Hall game, use OpenAI to generate a response
    if st.session_state.stage not in ["choose_door", "reveal_goat", "final_decision"]:
        response = llm.predict(prompt=user_input)
        st.session_state.messages.append("Bunty: " + response)
    else:
        # Game logic (simplified for brevity)
        if st.session_state.stage == "welcome":
            if "yes" in user_input.lower():
                st.session_state.stage = "choose_door"
                st.session_state.messages.append("Bunty: Great! Choose a door: 1, 2, or 3.")
            else:
                st.session_state.messages.append("Bunty: Maybe next time! Feel free to ask me anything else.")
                st.session_state.stage = "chat"  # Move to chat mode outside the game
        # Add other Monty Hall game stages here...

# Process input on pressing Enter
if user_input:
    st.session_state.messages.append("You: " + user_input)
    process_input(user_input)
    st.session_state.user_input = ''  # Clear input field
    st.experimental_rerun()  # Rerun the app to refresh the state

# Note: Simplified for brevity. Implement Monty Hall game logic in process_input function.
