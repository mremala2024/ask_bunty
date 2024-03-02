import streamlit as st
import os
import openai

# Load the OpenAI API key from an environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Function to generate responses using OpenAI's API
def generate_response_with_openai(user_message):
    response = openai.Completion.create(
      engine="text-davinci-003",  # You might want to update the engine if necessary
      prompt=user_message,
      temperature=0.7,
      max_tokens=150,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      stop=["\n"]
    )
    return response.choices[0].text.strip()

# Main Streamlit app
def main():
    st.title("Ask Bunty")

    # Initialize or update the session state for storing messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.text_area("You:", value=message["content"], height=100, key=f"user_{message['content']}", disabled=True)
        else:
            st.text_area("Bunty:", value=message["content"], height=100, key=f"assistant_{message['content']}", disabled=True)

    # User input
    user_input = st.text_input("Enter your message", "")

    # When the user submits a message
    if st.button("Send") and user_input:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Call OpenAI API to generate and display response
        if OPENAI_API_KEY:  # Ensure API key is available
            response = generate_response_with_openai(user_input)
            st.session_state.messages.append({"role": "Bunty", "content": response})
        else:
            st.error("OpenAI API key not set. Please check your environment variables.")

        # Clear the input box after sending the message by rerunning the app
        st.experimental_rerun()

if __name__ == "__main__":
    main()
