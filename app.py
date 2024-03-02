import os
import streamlit as st
import openai

# Retrieve the OpenAI API key and Assistant ID from environment variables directly
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

if not OPENAI_API_KEY or not ASSISTANT_ID:
    raise ValueError("API key or Assistant ID not found. Please set OPENAI_API_KEY and ASSISTANT_ID environment variables.")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Streamlit app setup
st.title("ChatGPT Clone with Assistant ID")

# Initialize session state for message history if it doesn't already exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.container():
        st.write(f"{message['role'].title()}: {message['content']}")

# User input
user_input = st.text_input("Enter your message:", key="user_input")

# Send button
send_button = st.button("Send")

if send_button and user_input:
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Prepare messages for OpenAI Chat Completion
    messages = [{"role": "user", "content": msg["content"]} for msg in st.session_state.messages if msg["role"] == "user"]
    
    # Call OpenAI API with Assistant ID (assuming GPT-3.5-turbo for example)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        assistant_id=ASSISTANT_ID
    )
    
    # Append assistant's response to chat history
    if response.choices:
        st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message["content"]})

# This line helps display the chat in a more conversational format
st.experimental_rerun()
