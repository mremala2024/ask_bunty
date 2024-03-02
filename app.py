import streamlit as st
import os
from langchain.llms import OpenAI

# Assuming OPENAI_API_KEY is set as an environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

llm = OpenAI(openai_api_key=OPENAI_API_KEY)

st.title("Ask Bunty About the Monty Hall Game")

# Styling for chat messages
st.markdown("""
<style>
.streamlit-text-area {
    border: 2px solid #4CAF50;
    border-radius: 20px;
}
.streamlit-input {
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Initialize or update the session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages in a more interactive and styled manner
for message in st.session_state.messages:
    st.text_area(label=message["role"] + ":", value=message["content"], height=75, disabled=True, key=f"{message['role']}_{st.session_state.messages.index(message)}")

# User input
user_input = st.text_input("Enter your message", "", key="user_input")

# When the user submits a message
if st.button("Send") and user_input:
    # Append user message to the session state
    st.session_state.messages.append({"role": "You", "content": user_input})

    # Concatenate all previous messages to maintain context
    conversation_context = "Let's discuss the Monty Hall game, a probability puzzle based on a game show scenario where you choose one of three doors, behind one of which is a car. The host, knowing what's behind the doors, opens another door revealing a goat. You then decide whether to stick with your initial choice or switch to the other unopened door. " + " ".join([msg["content"] for msg in st.session_state.messages if msg["role"] == "You"])

    # Generate and display response
    response = llm.predict(conversation_context)
    st.session_state.messages.append({"role": "Bunty", "content": response})

    # Clear the input box and rerun to update the chat
    st.experimental_rerun()
