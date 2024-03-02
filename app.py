import streamlit as st
import random
import openai

# Assuming your OpenAI API key is stored in Streamlit's secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

# Custom CSS for comic-style font
st.markdown("""
<style>
    html, body, [class*="st-"] {
    font-family: 'Comic Neue', 'Comic Sans MS', cursive !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states
if 'stage' not in st.session_state:
    st.session_state.stage = "welcome"
    st.session_state.messages = []

# Function to display chat
def display_chat():
    for message in st.session_state.messages:
        if message["sender"] == "user":
            st.text_area("", value=message["text"], height=40, key=f"user_{st.session_state.messages.index(message)}", disabled=True)
        else:
            st.text_area("", value=message["text"], height=80, key=f"bunty_{st.session_state.messages.index(message)}", disabled=True)

# Function to handle Monty Hall game logic or general queries
def handle_query(query):
    if st.session_state.stage == "welcome":
        st.session_state.messages.append({"sender": "bunty", "text": "Hi! I'm Bunty. Do you want to play the Monty Hall Game? (yes/no)"})
        st.session_state.stage = "ask_play"
    # Add more conditions here for each stage of the Monty Hall game
    # For non-game related queries, use OpenAI's API to get responses
    else:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=query,
            temperature=0.5,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        st.session_state.messages.append({"sender": "bunty", "text": response.choices[0].text.strip()})

# User input
user_input = st.text_input("Say something to Bunty...", key="user_input")

# Process input
if user_input:
    st.session_state.messages.append({"sender": "user", "text": user_input})
    handle_query(user_input)
    st.session_state.user_input = ""  # Clear the input box after processing
    st.experimental_rerun()

display_chat()
