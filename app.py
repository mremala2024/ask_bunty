import streamlit as st
import os
from langchain.llms import OpenAI

# Function to simulate responses based on user input
def simulate_response(user_message):
    # Example logic to simulate a response based on the user_message
    # This should be replaced with your logic to generate responses
    if "play" in user_message.lower():
        return "Great! Let's play the Monty Hall game! Here's how it works..."
    elif user_message.isdigit() and int(user_message) in [1, 2, 3]:
        return "You've chosen a door. Now, I will reveal a door with a goat..."
    elif "switch" in user_message.lower() or "stick" in user_message.lower():
        return "Let's see if you won the prize!"
    else:
        return "Would you like to play a game or learn about probability?"

# Main Streamlit app
def main():
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

        # Simulate and display response
        response = simulate_response(user_input)  # This line simulates generating a response
        st.session_state.messages.append({"role": "Bunty", "content": response})

        # Clear the input box after sending the message
        st.experimental_rerun()

if __name__ == "__main__":
    main()
