import streamlit as st
import os

# Placeholder for the OpenAI wrapper class
class OpenAI:
    def __init__(self, openai_api_key):
        self.api_key = openai_api_key
    
    # Placeholder for a method to send prompts to the OpenAI API and get a response
    def predict(self, prompt):
        # Integrate with OpenAI's API here, using the provided API key and prompt
        # This example simply echoes the prompt for demonstration purposes
        return f"Response to: {prompt}"

# Load the OpenAI API key from an environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the API key is not found and display an error message
if OPENAI_API_KEY is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Initialize the OpenAI wrapper with the API key
llm = OpenAI(openai_api_key=OPENAI_API_KEY)

# Set up the Streamlit UI
st.title("Ask Bunty")

# Initialize or update the session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Use custom CSS to style the chat for a friendlier and more engaging appearance
st.markdown("""
<style>
    .stTextArea>div>div>textarea {
        border-radius: 20px;
    }
    .stTextInput>div>div>input {
        border-radius: 20px;
    }
    .stButton>button {
        border-radius: 20px;
        border: 1px solid #4CAF50;
        color: white;
        background-color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Display existing messages
for message in st.session_state.messages:
    role = "You:" if message["role"] == "user" else "Bunty:"
    st.text_area(role, value=message["content"], height=100, key=f"{message['role']}_{st.session_state.messages.index(message)}", disabled=True)

# Input for user messages
user_input = st.text_input("Enter your message", "")

# When the user submits a message
if st.button("Send") and user_input:
    # Append user message to the conversation
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Enhanced prompt engineering for a kid-friendly tone and explanation of the Monty Hall problem
    prompt = f"Explain the Monty Hall problem in a simple, friendly, and engaging way suitable for kids. The user asked: '{user_input}'"
    response = llm.predict(prompt)  # Call the predict method with the enhanced prompt
    
    # Simple validation for response relevance (basic example)
    if "Monty Hall" in response or "door" in response:
        st.session_state.messages.append({"role": "Bunty", "content": response})
    else:
        # Fallback message in case the response is not relevant
        st.session_state.messages.append({"role": "Bunty", "content": "Hmm, I'm not sure about that. Let's try something else fun!"})

    # Clear the input box after sending the message
    st.experimental_rerun()
