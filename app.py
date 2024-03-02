import streamlit as st
import os
from langchain.llms import OpenAI

# Assuming OPENAI_API_KEY is set as an environment variable for security reasons
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

llm = OpenAI(openai_api_key=OPENAI_API_KEY)

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

# Predefined responses based on specific inputs
def get_predefined_response(message):
    predefined_responses = {
        "hi": "Hello there! Welcome to the chat! Are you interested in playing a fun game to test your decision-making skills? It's called the Monty Hall game! Would you like to give it a try?",
        "yes": "Great! Let's play the Monty Hall game! Here's how it works: Imagine there are three doors. Behind one of the doors, there's a fantastic prize, like a new toy! Behind the other two doors, there are goats. First, you choose one of the three doors. Then, I will reveal one of the other two doors that has a goat behind it. After seeing the goat behind one of the doors, you'll have the option to stick with your original choice or switch to the other remaining door. So, which door would you like to choose: Door 1, Door 2, or Door 3? Just let me know your pick!",
        "how to win in the game": "To increase your chances of winning the Monty Hall game, it's generally better to switch doors after one with a goat has been revealed. Here's why: When you initially choose a door, there's a 1/3 chance that you picked the door with the prize behind it. This means there's a 2/3 chance that the prize is behind one of the other two doors. When one of the other doors with a goat is revealed, the probability doesn't change for your initial choice (1/3 chance of being correct), but the combined probability for the other two doors increases to 2/3. So, by switching doors, you're more likely to win the prize. It might seem counterintuitive, but statistically, switching doors gives you a higher chance of winning in the long run. It's a fun way to learn about probability and decision-making! Would you like to play another round or learn more about games and strategies? Just let me know!"
    }
    # Return the predefined response if it exists, otherwise None
    return predefined_responses.get(message.lower())

# When the user submits a message
if st.button("Send") and user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Check for predefined response
    predefined_response = get_predefined_response(user_input)
    if predefined_response:
        response = predefined_response
    else:
        # Generate and display response using OpenAI API if no predefined response is found
        response = llm.predict(prompt=user_input, max_tokens=150)["choices"][0]["text"].strip()

    st.session_state.messages.append({"role": "Bunty", "content": response})

    # Clear the input box after sending the message
    st.experimental_rerun()
