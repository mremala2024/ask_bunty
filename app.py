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

# Define custom responses based on the provided messages
custom_responses = {
    "hi": "Hello there! Welcome to the chat! Are you interested in playing a fun game to test your decision-making skills? It's called the Monty Hall game! Would you like to give it a try?",
    "yes": "Great! Let's play the Monty Hall game! Here's how it works:\n\nImagine there are three doors. Behind one of the doors, there's a fantastic prize, like a new toy! Behind the other two doors, there are goats.\n\nFirst, you choose one of the three doors...",
    # Add more custom responses as needed
}

# User input
user_input = st.text_input("Enter your message", "")

# When the user submits a message
if st.button("Send") and user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Check if the user input matches any custom response
    response = None
    for key, value in custom_responses.items():
        if key.lower() in user_input.lower():
            response = value
            break
    
    # If no custom response is found, use llm to generate a response
    if response is None:
        response_data = llm.predict(prompt=user_input, max_tokens=150)
        if response_data and 'choices' in response_data and len(response_data['choices']) > 0:
            response = response_data['choices'][0]['text'].strip()
        else:
            response = "I'm sorry, I couldn't generate a response. Please try again."
    
    # Append the response to the session state for display
    st.session_state.messages.append({"role": "Bunty", "content": response})

    # Clear the input box after sending the message
    st.experimental_rerun()
