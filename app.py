import streamlit as st
import os
from langchain.llms import OpenAI

# Assuming OPENAI_API_KEY is set as an environment variable for security reasons
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

llm = OpenAI(openai_api_key=OPENAI_API_KEY)

st.title("Ask Bunty")

# Initialize or update the session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.text_area("You:", value=message["content"], height=100, key=f"user_{st.session_state.messages.index(message)}", disabled=True)
    else:
        st.text_area("Bunty:", value=message["content"], height=100, key=f"assistant_{st.session_state.messages.index(message)}", disabled=True)

# User input
user_input = st.text_input("Enter your message", "")

# When the user submits a message
if st.button("Send") and user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate and display response
    response = llm.predict(user_input)
    st.session_state.messages.append({"role": "Bunty", "content": response})

    # Clear the input box after sending the message
    st.experimental_rerun()
