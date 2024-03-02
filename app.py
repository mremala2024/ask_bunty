import streamlit as st
import os
from langchain.llms import OpenAI

# Function to inject custom CSS
def inject_custom_css():
    st.markdown("""
        <style>
        /* Style for the chat boxes */
        .stTextArea>div>div>textarea {
            border: 2px solid #4B0082; /* Purple borders */
            border-radius: 20px; /* Rounded corners */
            background-color: #F0E68C; /* Light yellow background */
        }
        /* Style for the user input box */
        .stTextInput>div>div>input {
            border-radius: 20px; /* Rounded corners for input box */
            border: 2px solid #FF6347; /* Tomato borders for input box */
        }
        /* Custom style for the send button (hidden in this case) */
        .stButton>button {
            display: none; /* Hide the send button */
        }
        </style>
    """, unsafe_allow_html=True)

# Inject the custom CSS
inject_custom_css()

# Initialize LangChain's OpenAI with the API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()
llm = OpenAI(openai_api_key=OPENAI_API_KEY)

# Application title
st.title("Ask Bunty")

# Initialize or update the session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.text_area("", value=message["content"], height=75, key=f"user_{st.session_state.messages.index(message)}", disabled=True)
    else:  # Bunty's messages
        st.text_area("", value=message["content"], height=75, key=f"assistant_{st.session_state.messages.index(message)}", disabled=True)

# User input with an arrow (simulated using placeholder text)
user_input = st.text_input("➡️ Enter your message", "", on_change=lambda: send_message(), key="user_input")

# Function to handle sending messages
def send_message():
    user_message = st.session_state.user_input
    if user_message:
        # Append user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_message})
        # Generate and append Bunty's response
        response = llm.predict(user_message)
        st.session_state.messages.append({"role": "Bunty", "content": response})
        # Clear the input box after sending the message
        st.session_state.user_input = ""
        st.experimental_rerun()

# Note: The actual send functionality is triggered by the on_change callback of the text_input
