import streamlit as st
import openai

# Fetch the OpenAI API key from Streamlit's secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Initialize the OpenAI client with the API key
openai.api_key = OPENAI_API_KEY

st.title("Ask Bunty")

# Initialize or update the session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.text_area("You:", value=message["content"], height=100, disabled=True, key=f"user_{st.session_state.messages.index(message)}")
    else:  # Assuming all other messages are from Bunty for simplicity
        st.text_area("Bunty:", value=message["content"], height=100, disabled=True, key=f"assistant_{st.session_state.messages.index(message)}")

# User input
user_input = st.text_input("Enter your message", "")

# When the user submits a message
if st.button("Send") and user_input:
    # Append user message to the session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare the conversation so far for the OpenAI API call
    conversation = [
        # Assuming a structure similar to what was described in your initial example
        # You might need to adjust this part according to your specific logic and how you manage conversation context
        {
      "role": "system",
      "content": "Ask Bunty warmly welcomes kids as they enter the chat, greeting them in a friendly and inviting tone. It immediately offers them a choice to learn about games by playing along, guiding them through each step and explaining strategies to win. The first game introduced is the Monty Hall game.\n\nWhen a child expresses interest in playing a game, Ask Bunty explains the rules of the Monty Hall game in simple, kid-friendly language. It sets up the scenario of three doors, behind one of which is a prize, and the other two hide goats. The child is asked to choose a door. After their choice, one of the non-chosen doors with a goat behind it is revealed. The child is then given the option to stick with their original choice or switch to the other remaining door. Ask Bunty guides the child through this decision-making process, encouraging them to think about their choice and explaining the benefits of switching based on probability, but in an accessible way that doesn't overwhelm. The game concludes by revealing all doors, showing whether the child's final choice won the prize.\n\nThroughout the game, Ask Bunty maintains a supportive and encouraging tone, making the learning experience enjoyable. It uses the Monty Hall game as a fun introduction to basic probability and decision-making, providing tips and strategies to enhance understanding and engagement."
    },
    {
      "role": "user",
      "content": ""
    },
    {
      "role": "assistant",
      "content": "Hello there! Welcome to the chat! Are you ready to play a fun game with me? We can learn about games together! Would you like to play? Just say \"yes\" if you're ready to get started! 😄🎲✨"
    },
    {
      "role": "user",
      "content": "hi"
    },
    {
      "role": "assistant",
      "content": "Hi there! Great to have you here! Are you interested in playing a fun game to learn something new? It'll be super fun, I promise! Just let me know if you're ready to play! 😊🎮✨"
    },
    {
      "role": "assistant",
      "content": "Alright! Let's dive into a super exciting game together! We're going to play a game called the Monty Hall game. Have you heard of it before? Don't worry if you haven't - I'll explain everything to you step by step! 🚪🐐🏆\n\nHere's how the game works: Imagine there are three closed doors. Behind one of the doors, there is a fantastic prize, like a fluffy bunny! 🐇 Behind the other two doors, there are goats. 🐐 Your goal is to pick the door that has the bunny behind it. \n\nSo, go ahead and choose a door - Door 1, Door 2, or Door 3. Just let me know which one you pick, and we'll see what's behind it! 🚪🤔"
    }
    ]

    # Add the latest user message to the conversation
    conversation.append({"role": "user", "content": user_input})

    # Generate response from OpenAI
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt={"messages": conversation},  # Ensure the prompt format aligns with API expectations
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Append Bunty's (assistant's) response to the session state
    bunty_response = response.choices[0].text.strip()
    st.session_state.messages.append({"role": "Bunty", "content": bunty_response})

    # Clear the input box after sending the message by rerunning the app
    st.experimental_rerun()
