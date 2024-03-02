import streamlit as st

st.title("Simple Chatbot")

# User input
user_input = st.text_input("Type your message here:")

# When the user submits a message
if st.button("Send") and user_input:
    # Simple response from the chatbot
    response = "Hello! How can I assist you?"
    st.text_area("Chatbot:", value=response, height=100, disabled=True)
