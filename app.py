import streamlit as st

# Function to simulate a response from the chatbot, adjust with actual OpenAI API call
def chatbot_response(user_input):
    # Placeholder response logic, replace with your actual API call
    if "monty hall" in user_input.lower():
        return "Alright, let's play the Monty Hall game! Imagine we have three doors: behind one door is a shiny car 🚗, and behind the others, friendly goats 🐐. Which door would you like to pick first?"
    elif "play" in user_input.lower():
        return "Great! Do you want to try the Monty Hall game? It's really fun!"
    else:
        return "I'm here to make learning fun. What would you like to do?"

st.title("Ask Bunty")

# Initialize or update the session state for storing messages and conversation state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.conversation_started = False

# Display existing messages
for message in st.session_state.messages:
    role = "You:" if message["role"] == "user" else "Bunty:"
    st.text_area(role, value=message["content"], height=100, key=f"{message['role']}_{st.session_state.messages.index(message)}", disabled=True)

# Start of conversation
if not st.session_state.conversation_started:
    st.session_state.messages.append({"role": "Bunty", "content": "Hi there, friend! Ready to play a fun game and learn something cool?\n\n1. Let's pick a door and see if you can win the car behind it.\n2. Do you want to try the Monty Hall game? It's really fun!"})
    st.session_state.conversation_started = True

# User input
user_input = st.text_input("Enter your message", "")

# When the user submits a message
if st.button("Send") and user_input:
    # Append user message to the conversation
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate and display response
    response = chatbot_response(user_input)
    st.session_state.messages.append({"role": "Bunty", "content": response})

    # Clear the input box after sending the message
    st.experimental_rerun()
