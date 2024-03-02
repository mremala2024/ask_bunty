import streamlit as st
import random

# Assuming OPENAI_API_KEY is set in Streamlit's secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Setup LangChain OpenAI with API key
from langchain.llms import OpenAI
llm = OpenAI(openai_api_key=OPENAI_API_KEY)

# Page setup
st.title("Monty Hall Game with Bunty")

# Instructions
if 'stage' not in st.session_state:
    st.session_state['stage'] = 0
    st.session_state['chosen_door'] = None
    st.session_state['car_door'] = random.randint(1, 3)
    st.session_state['revealed_door'] = None
    st.session_state['messages'] = ["Hi! I'm Bunty. Do you want to play the Monty Hall Game? (yes/no)"]

# Display messages
for message in st.session_state['messages']:
    st.write(message)

# User input
user_input = st.text_input("Your response:", key="user_response")

# Process input
if user_input:
    if st.session_state['stage'] == 0:
        if user_input.lower() == 'yes':
            st.session_state['messages'].append("Great! Choose a door (1, 2, or 3):")
            st.session_state['stage'] = 1
        else:
            st.session_state['messages'].append("Maybe next time!")
    elif st.session_state['stage'] == 1:
        if user_input in ['1', '2', '3']:
            chosen_door = int(user_input)
            st.session_state['chosen_door'] = chosen_door
            # Reveal a door that does not have a car and was not chosen
            doors = [1, 2, 3]
            doors.remove(chosen_door)
            if st.session_state['car_door'] in doors:
                doors.remove(st.session_state['car_door'])
            revealed_door = random.choice(doors)
            st.session_state['revealed_door'] = revealed_door
            st.session_state['messages'].append(f"Door {revealed_door} has a goat. Do you want to switch your choice? (yes/no)")
            st.session_state['stage'] = 2
        else:
            st.session_state['messages'].append("Please choose a valid door (1, 2, or 3):")
    elif st.session_state['stage'] == 2:
        if user_input.lower() == 'yes':
            # Switch choice
            doors = [1, 2, 3]
            doors.remove(st.session_state['chosen_door'])
            doors.remove(st.session_state['revealed_door'])
            final_choice = doors[0]
        else:
            final_choice = st.session_state['chosen_door']
        if final_choice == st.session_state['car_door']:
            st.session_state['messages'].append("You won the car!")
        else:
            st.session_state['messages'].append("It's a goat. Better luck next time!")
        st.session_state['messages'].append("Game over. Thanks for playing!")
        st.session_state['stage'] = 3  # End game
    # Clear input
    st.session_state['user_response'] = ''
    st.experimental_rerun()

