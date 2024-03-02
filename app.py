import streamlit as st
import openai

# Assuming OPENAI_API_KEY is set as an environment variable for security reasons
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

if OPENAI_API_KEY is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY in your Streamlit secrets.")
    st.stop()

# Initialize OpenAI client with the API key
openai.api_key = OPENAI_API_KEY

st.title("Ask Bunty")

# Initialize or update the session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.text_area("You:", value=message["content"], height=100, key=f"user_{st.session_state.messages.index(message)}", disabled=True)
    else:  # Assuming all other messages are from Bunty for simplicity
        st.text_area("Bunty:", value=message["content"], height=100, key=f"assistant_{st.session_state.messages.index(message)}", disabled=True)

# User input
user_input = st.text_input("Enter your message", "")

# When the user submits a message
if st.button("Send") and user_input:
    # Append user message to the session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare the conversation so far for the OpenAI API call
    conversation = [
        {
            "role": "system",
            "content": "Ask Bunty warmly welcomes kids as they enter the chat, greeting them in a friendly and inviting tone..."
            # The content should include the initial system prompt and any other necessary context
        },
        *st.session_state.messages,  # Include all previous messages
        {"role": "user", "content": user_input}  # Include the latest user message
    ]

    # Generate response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Append Bunty's (assistant's) response to the session state
    bunty_response = response.choices[0].message["content"]
    st.session_state.messages.append({"role": "Bunty", "content": bunty_response})

    # Clear the input box after sending the message
    st.experimental_rerun()
