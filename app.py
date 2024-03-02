import streamlit as st
from langchain.llms import OpenAI
import random

# Setup OpenAI API key from Streamlit secrets
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "")

if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY in your Streamlit secrets.")
    st.stop()

llm = OpenAI(openai_api_key=OPENAI_API_KEY)

st.title("Chat with Bunty")

# Initialize or update the session state for storing messages and game state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "Bunty", "content": "Hello, I'm Bunty! Say 'hi' to start."}]
    st.session_state["game_state"] = "user_greeting"
    st.session_state["chosen_door"] = None
    st.session_state["car_door"] = None
    st.session_state["revealed_goat_door"] = None

def add_message(role, content):
    """Add a message to the conversation."""
    st.session_state["messages"].append({"role": role, "content": content})

def handle_message(user_input):
    """Process user messages, including game logic and general queries."""
    user_input = user_input.strip().lower()

    if user_input and st.session_state["game_state"] == "user_greeting":
        add_message("You", user_input)
        if "hi" in user_input or "hello" in user_input:
            add_message("Bunty", "Do you want to play the Monty Hall game? (Yes/No)")
            st.session_state["game_state"] = "waiting_for_game_start"
        else:
            response = llm.predict(prompt=user_input, max_tokens=60, temperature=0.5)
            response_text = ' '.join(response.split()[:20])  # Limit to 20 words
            add_message("Bunty", response_text)
    elif st.session_state["game_state"] == "waiting_for_game_start" and user_input == "yes":
        add_message("You", user_input)
        add_message("Bunty", "Great! Choose a door: 1, 2, or 3.")
        st.session_state["game_state"] = "choosing_door"
        st.session_state["car_door"] = random.randint(1, 3)  # Randomly place the car
    elif st.session_state["game_state"] == "choosing_door" and user_input in ["1", "2", "3"]:
        user_choice = int(user_input)
        st.session_state["chosen_door"] = user_choice
        add_message("You", f"Door {user_choice}")
        
        # Reveal a goat door that was not chosen and does not have the car
        doors = [1, 2, 3]
        doors.remove(user_choice)
        if st.session_state["car_door"] in doors: doors.remove(st.session_state["car_door"])
        revealed_goat_door = doors[random.randint(0, len(doors) - 1)]
        st.session_state["revealed_goat_door"] = revealed_goat_door
        
        add_message("Bunty", f"Behind door {revealed_goat_door}, there is a goat. Do you want to switch your choice? (Yes/No)")
        st.session_state["game_state"] = "offered_to_switch"
    elif st.session_state["game_state"] == "offered_to_switch":
        add_message("You", user_input)
        if user_input == "yes":
            # Switch the user's choice to the remaining door
            remaining_doors = [1, 2, 3]
            remaining_doors.remove(st.session_state["chosen_door"])
            remaining_doors.remove(st.session_state["revealed_goat_door"])
            st.session_state["chosen_door"] = remaining_doors[0]
        
        # Reveal the outcome
        if st.session_state["chosen_door"] == st.session_state["car_door"]:
            add_message("Bunty", "You've won the car! Congratulations!")
        else:
            add_message("Bunty", "Sorry, there's a goat behind your door. Better luck next time!")
        st.session_state["game_state"] = "game_over"
        add_message("Bunty", "Do you want to play again? (Yes/No)")
    else:
        # Reset the game or handle post-game conversation
        if st.session_state["game_state"] == "game_over" and user_input == "yes":
            # Reset the game state to start a new game
            st.session_state["game_state"] = "waiting_for_game_start"
            st.session_state["chosen_door"] = None
            st.session_state["car_door"] = None
            st.session_state["revealed_goat_door"] = None
            add_message("Bunty", "Do you want to play the Monty Hall game? (Yes/No)")
        else:
            # Treat any other input as a general query
            response = llm.predict(prompt=user_input, max_tokens=60, temperature=0.5)
            response_text = ' '.join(response.split()[:20])  # Limit to 20 words
            add_message("Bunty", response_text)

# User input and message handling
user_input = st.text_input("Say something to Bunty:", key="new_message", on_change=handle_message, args=(st.session_state.get("new_message"),))

# Display the conversation
for message in st.session_state["messages"]:
    role = "You:" if message["role"] == "user" else "Bunty:"
    st.text_area(f"{role}", value=message["content"], height=75, disabled=True, key=f"{role}_{st.session_state['messages'].index(message)}")
