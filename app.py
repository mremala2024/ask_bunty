import streamlit as st
import os
import random

# Assuming OPENAI_API_KEY is set as an environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Initialize LangChain's OpenAI with the API key
llm = OpenAI(openai_api_key=OPENAI_API_KEY)

st.title("Ask Bunty About the Monty Hall Game")

# Styling for chat messages
st.markdown("""
<style>
.streamlit-text-area, .streamlit-input {
    border: 2px solid #4CAF50;
    border-radius: 20px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Initialize or update session state
if "stage" not in st.session_state:
    st.session_state.stage = "greeting"
    st.session_state.messages = []

# Function to handle game logic
def monty_hall_game(user_input):
    if st.session_state.stage == "greeting":
        st.session_state.messages.append({"role": "Bunty", "content": "Hello! Do you want to play the Monty Hall game? (Yes/No)"})
        st.session_state.stage = "ask_play"
    elif st.session_state.stage == "ask_play":
        if user_input.lower() == "yes":
            st.session_state.messages.append({"role": "Bunty", "content": "Great! Choose a door: 1, 2, or 3."})
            st.session_state.stage = "choose_door"
        else:
            st.session_state.messages.append({"role": "Bunty", "content": "Maybe next time! Have a nice day."})
            st.session_state.stage = "end"
    elif st.session_state.stage == "choose_door":
        chosen_door = int(user_input) if user_input.isdigit() and int(user_input) in [1, 2, 3] else None
        if chosen_door:
            doors = [1, 2, 3]
            prize_door = random.choice(doors)
            doors.remove(chosen_door)
            if chosen_door != prize_door:
                doors.remove(prize_door)
            revealed_door = random.choice(doors)
            st.session_state.revealed_door = revealed_door
            st.session_state.chosen_door = chosen_door
            st.session_state.prize_door = prize_door
            st.session_state.messages.append({"role": "Bunty", "content": f"Door {revealed_door} has a goat. Do you want to switch your choice? (Yes/No)"})
            st.session_state.stage = "switch_choice"
        else:
            st.session_state.messages.append({"role": "Bunty", "content": "Please choose a valid door: 1, 2, or 3."})
    elif st.session_state.stage == "switch_choice":
        if user_input.lower() == "yes":
            final_choice = 6 - st.session_state.chosen_door - st.session_state.revealed_door
        else:
            final_choice = st.session_state.chosen_door
        if final_choice == st.session_state.prize_door:
            st.session_state.messages.append({"role": "Bunty", "content": "Congratulations! You've won the car!"})
        else:
            st.session_state.messages.append({"role": "Bunty", "content": "Sorry, you've found a goat. Better luck next time!"})
        st.session_state.messages.append({"role": "Bunty", "content": "The strategy is to always switch, statistically giving you a 2/3 chance of winning."})
        st.session_state.stage = "end"

# Display existing messages
for message in st.session_state.messages:
    st.text_area(label=message["role"] + ":", value=message["content"], height=75, disabled=True, key=f"{message['role']}_{st.session_state.messages.index(message)}")

# User input
user_input = st.text_input("Enter your message", "", key="user_input")

# When the user submits a message
if user_input and st.session_state.stage != "end
