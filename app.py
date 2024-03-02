import streamlit as st
from langchain.llms import OpenAI

# Retrieve the OpenAI API key from Streamlit's secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

llm = OpenAI(openai_api_key=OPENAI_API_KEY)

st.title("Ask Bunty About the Monty Hall Game")

# Custom CSS for styling the chat
st.markdown("""
<style>
.streamlit-text-area, .streamlit-input {
    border: 2px solid #4CAF50;
    border-radius: 20px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Initialize or update session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    st.text_area(label=message["role"] + ":", value=message["content"], height=75, disabled=True, key=f"{message['role']}_{st.session_state.messages.index(message)}")

# User input handling
user_input = st.text_input("Enter your message", "", key="user_input")

# Interactive chat logic here...
# The rest of your application logic follows
