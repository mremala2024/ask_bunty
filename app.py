import streamlit as st
import os

# Assuming OPENAI_API_KEY is set as an environment variable for security reasons
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Placeholder for the OpenAI class (adapt according to your actual implementation)
class OpenAI:
    def __init__(self, openai_api_key):
        self.api_key = openai_api_key
    
    def predict(self, prompt):
        # Your logic to call the OpenAI API and return the response
        return "Let's have fun learning!"

llm = OpenAI(openai_api_key=OPENAI_API_KEY)

st.title("Ask Bunty")

# Initialize or update the session state for storing messages and check if the greeting has been done
if "messages" not in st.session_state:
    st.session_state.messages = []
    greeting_message = "Hi there, friend! Ready to play a fun game and learn something cool? Or do you want to try the Monty Hall game? It's really fun!"
    st.session_state.messages.append({"role": "Bunty", "content": greeting_message})

# Display existing messages
for message in st.session_state.messages:
    role = "You:" if message["role"] == "user" else "Bunty:"
    st.text_area(role, value=message["content"], height=100, key=f"{message['role']}_{st.session_state.messages.index(message)}", disabled=True)

# User input
user_input = st.text_input("Enter your message", "")

# When the user submits a message
if st.button("Send") and user_input:
    # Append user message to the conversation
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Simple logic to handle a response about the Monty Hall game
    # You can expand this with more conditions or integrate with llm.predict for dynamic responses
    if "monty hall" in user_input.lower():
        response = "Great choice! In the Monty Hall game, you get to pick one of three doors. Behind one door is a car, and behind the others, goats. Pick a door, and I'll show you what happens next!"
    else:
        # Use llm.predict or another method to generate a response for other inputs
        response = llm.predict(user_input)

    # Append Bunty's response to the conversation
    st.session_state.messages.append({"role": "Bunty", "content": response})

    # Clear the input box after sending the message
    st.experimental_rerun()
