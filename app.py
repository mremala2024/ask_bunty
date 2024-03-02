import streamlit as st
import random
from langchain.llms import OpenAI

# Assuming OPENAI_API_KEY is set in Streamlit's secrets for security reasons
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

llm = OpenAI(openai_api_key=OPENAI_API_KEY)

st.title("Ask Bunty")

# Initialize or update the session state for storing messages, game state, and game details
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    st.session_state["game_state"] = "init"
    st.session_state["chosen_door"] = None
    st.session_state["goat_door"] = None
    st.session_state["car_door"] = None

# Function to handle user messages and game logic
def handle_message(user_input):
    user_input = user_input.strip().lower()
    game_response = ""

    if st.session_state.game_state == "init":
        game_response = "Hello, I'm Bunty! Do you want to play the Monty Hall game? (Yes/No)"
        st.session_state.game_state = "waiting_for_game_start"

    elif user_input == "yes" and st.session_state.game_state == "waiting_for_game_start":
        game_response = "Great! Choose a door: 1, 2, or 3."
        st.session_state.game_state = "choosing_door"

    elif user_input in ["1", "2", "3"] and st.session_state.game_state == "choosing_door":
        chosen_door = int(user_input)
        car_door = random.randint(1, 3)
        goat_door = next(door for door in [1, 2, 3] if door != chosen_door and door != car_door)
        game_response = f"Door {goat_door} has a goat behind it. Do you want to switch your choice? (Yes/No)"
        st.session_state.update({"chosen_door": chosen_door, "goat_door": goat_door, "car_door": car_door, "game_state": "offered_to_switch"})

    elif user_input in ["yes", "no"] and st.session_state.game_state == "offered_to_switch":
        if user_input == "yes":
            chosen_door = next(door for door in [1, 2, 3] if door not in [st.session_state["chosen_door"], st.session_state["goat_door"]])
        else:
            chosen_door = st.session_state["chosen_door"]
        game_response = "Congratulations! You've won the car!" if chosen_door == st.session_state["car_door"] else "Sorry, you've found a goat. Better luck next time!"
        game_response += " The key strategy is to always switch, which statistically gives you a 2/3 chance of winning."
        st.session_state.game_state = "game_over"

    if game_response:
        st.session_state.messages.append({"role": "Bunty", "content": game_response})
    else:
        # If the input doesn't match expected game responses, treat it as a general query
        response = llm.predict(user_input)
        st.session_state.messages.append({"role": "Bunty", "content": response})

# Display existing messages
for message in st.session_state.messages:
    st.text_area("", value=message["content"], height=100, key=f"{message['role']}_{st.session_state.messages.index(message)}", disabled=True)

# User input and Send button
user_input = st.text_input("Enter your message", key="user_input")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    handle_message(user_input)
    st.session_state.user_input = ""  # Attempt to clear the input box, might not clear due to Streamlit's behavior
    st.experimental_rerun()
