import os
import streamlit as st
import openai

# Retrieve the OpenAI API key and Assistant ID from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

if not OPENAI_API_KEY or not ASSISTANT_ID:
    raise ValueError("API key or Assistant ID not found. Please set OPENAI_API_KEY and ASSISTANT_ID environment variables.")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Streamlit app
st.title("Ask Bunty")

# Initialize session state for message history
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
    messages = [{"role": "system", "content": "The following is a conversation with an AI assistant."},
                *st.session_state.messages]

    # Call OpenAI API with parameters aimed at improving response relevance
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,  # Adjust for more deterministic (lower) or creative (higher) responses
        max_tokens=150,
        assistant_id=ASSISTANT_ID
    )

    # Append assistant's response to chat history
    if response.choices:
        st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message["content"]})

    # Rerun the Streamlit app to update the conversation
    st.experimental_rerun()
