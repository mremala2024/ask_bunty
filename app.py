import streamlit as st
from langchain.llms import OpenAI
import random

# Assuming OPENAI_API_KEY is set in Streamlit secrets for security reasons
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "")

if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY in your Streamlit secrets.")
    st.stop()

llm = OpenAI(openai_api_key=OPENAI_API_KEY)

st.title("Ask Bunty")

# Initialize or update the session state for storing messages and game state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "Bunty", "content": "Hello, I'm Bunty! Do you want to play the Monty Hall game? (Yes/No)"}]
    st.session_state.game_state = "waiting_for_game_start"

def handle_game_logic(user_input):
    user_input = user_input.strip().lower()
    game_response = ""

    if user_input == "yes" and st.session_state.game_state == "waiting_for_game_start":
        game_response = "Great! Choose a door: 1, 2, or 3."
        st.session_state.game_state = "choosing_door"
    elif user_input in ["1", "2", "3"] and st.session_state.game_state == "choosing_door":
        chosen_door = int(user_input)
        car_door = random.randint(1, 3)
        goat_door = next(door for door in [1, 2, 3] if door != chosen_door and door != car_door)
        game_response = f"Door {goat_door} has a goat behind it. Do you want to switch your choice? (Yes/No)"
        st.session_state.game_state = "offered_to_switch"
        # Store game details for further logic
        st.session_state.update({"chosen_door": chosen_door, "car_door": car_door, "goat_door": goat_door})
    elif user_input in ["yes", "no"] and st.session_state.game_state == "offered_to_switch":
        final_choice = st.session_state.chosen_door if user_input == "no" else 6 - st.session_state.chosen_door - st.session_state.goat_door
        game_response = "Congratulations! You've won the car!" if final_choice == st.session_state.car_door else "Sorry, you've found a goat. Better luck next time!"
        st.session_state.game_state = "game_over"
    else:
        # Handle as non-game related query if the game state doesn't match or after game over
        response = llm.predict(user_input)
        game_response = response

    return game_response

# User submits a message
user_input = st.text_input("Enter your message:", "")
if user_input:
    # Append user message to the conversation
    st.session_state.messages.append({"role": "You", "content": user_input})

    # Handle the message based on the current game state or forward to OpenAI
    bunty_response = handle_game_logic(user_input)
    st.session_state.messages.append({"role": "Bunty", "content": bunty_response})

# Display the conversation
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    st.text_area(f"{role}:", value=content, height=100, key=f"{role}_{st.session_state.messages.index(message)}", disabled=True)
