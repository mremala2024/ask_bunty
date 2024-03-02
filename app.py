import streamlit as st
import random
from langchain.llms import OpenAI

# Assuming the OPENAI_API_KEY is securely set up in Streamlit's secrets or through another secure method
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

llm = OpenAI(openai_api_key=OPENAI_API_KEY)

st.title("Ask Bunty About the Monty Hall Game")

# Initialize or update the session state for storing messages and game state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.game_state = "init"

# Function to handle user messages and generate responses
def handle_message(user_input):
    if st.session_state.game_state == "init":
        st.session_state.messages.append({"role": "Bunty", "content": "Hello, I'm Bunty! Do you want to play the Monty Hall game? (Yes/No)"})
        st.session_state.game_state = "waiting_for_game_start"
    elif user_input.strip().lower() == "yes" and st.session_state.game_state == "waiting_for_game_start":
        st.session_state.messages.append({"role": "Bunty", "content": "Great! Choose a door: 1, 2, or 3."})
        st.session_state.game_state = "choosing_door"
    elif user_input.strip().isdigit() and st.session_state.game_state == "choosing_door":
        chosen_door = int(user_input)
        car_door = random.randint(1, 3)
        goat_door = next(door for door in [1, 2, 3] if door != chosen_door and door != car_door)
        st.session_state.messages.append({"role": "Bunty", "content": f"Door {goat_door} has a goat behind it. Do you want to switch your choice? (Yes/No)"})
        st.session_state['chosen_door'] = chosen_door
        st.session_state['goat_door'] = goat_door
        st.session_state['car_door'] = car_door
        st.session_state.game_state = "offered_to_switch"
    elif user_input.strip().lower() in ["yes", "no"] and st.session_state.game_state == "offered_to_switch":
        if user_input.strip().lower() == "yes":
            st.session_state['chosen_door'] = next(door for door in [1, 2, 3] if door != st.session_state['chosen_door'] and door != st.session_state['goat_door'])
        if st.session_state['chosen_door'] == st.session_state['car_door']:
            st.session_state.messages.append({"role": "Bunty", "content": "Congratulations! You've won the car!"})
        else:
            st.session_state.messages.append({"role": "Bunty", "content": "Sorry, you've found a goat. Better luck next time!"})
        st.session_state.messages.append({"role": "Bunty", "content": "The key strategy is to always switch, which statistically gives you a 2/3 chance of winning."})
        st.session_state.game_state = "game_over"
    else:
        # For non-game related questions or if game state doesn't match any known condition,
        # use OpenAI to generate a response.
        response = llm.predict(user_input)
        st.session_state.messages.append({"role": "Bunty", "content": response})

# Display existing messages with floating chat style
for message in st.session_state.messages:
    if message["role"] == "user":
        st.text_area("You:", value=message["content"], height=50, key=f"user_{st.session_state.messages.index(message)}", disabled=True)
    else:
        st.text_area("Bunty:", value=message["content"], height=50, key=f"assistant_{st.session_state.messages.index(message)}", disabled=True)

# User input
user_input = st.text_input("Enter your message", "")

# When the user submits a message
if st.button("Send") and user_input:
    # Handle the user message
    handle_message(user_input)

    # Clear the input box after sending the message
    st.experimental
