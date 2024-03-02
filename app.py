import streamlit as st
from langchain.llms import OpenAI

# Load the OpenAI API key, assuming it's set as an environment variable
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else None

if OPENAI_API_KEY is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY in your Streamlit secrets.")
    st.stop()

llm = OpenAI(openai_api_key=OPENAI_API_KEY)

st.title("Ask Bunty")

# Initialize or update the session state for storing messages and game state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.game_state = "init"

def handle_message(user_input):
    # Basic validation to ensure user_input is processable
    user_input = user_input.strip().lower()

    # Starting the game
    if st.session_state.game_state == "init":
        st.session_state.messages.append({"role": "Bunty", "content": "Hello, I'm Bunty! Do you want to play the Monty Hall game? (Yes/No)"})
        st.session_state.game_state = "waiting_for_game_start"

    # User agrees to play the game
    elif user_input == "yes" and st.session_state.game_state == "waiting_for_game_start":
        st.session_state.messages.append({"role": "Bunty", "content": "Great! Choose a door: 1, 2, or 3."})
        st.session_state.game_state = "choosing_door"

    # User chooses a door
    elif user_input in ["1", "2", "3"] and st.session_state.game_state == "choosing_door":
        chosen_door = int(user_input)
        st.session_state['chosen_door'] = chosen_door
        # Randomly decide which door has the car and reveal a goat door
        car_door = random.randint(1, 3)
        goat_door = next(door for door in [1, 2, 3] if door != chosen_door and door != car_door)
        st.session_state.messages.append({"role": "Bunty", "content": f"Door {goat_door} has a goat behind it. Do you want to switch your choice? (Yes/No)"})
        st.session_state['goat_door'] = goat_door
        st.session_state['car_door'] = car_door
        st.session_state.game_state = "offered_to_switch"

    # User decides whether to switch
    elif user_input in ["yes", "no"] and st.session_state.game_state == "offered_to_switch":
        if user_input == "yes":
            # Switch to the remaining door
            st.session_state['chosen_door'] = next(door for door in [1, 2, 3] if door not in [st.session_state['chosen_door'], st.session_state['goat_door']])
        # Reveal whether the user won or lost
        if st.session_state['chosen_door'] == st.session_state['car_door']:
            st.session_state.messages.append({"role": "Bunty", "content": "Congratulations! You've won the car!"})
        else:
            st.session_state.messages.append({"role": "Bunty", "content": "Sorry, you've found a goat. Better luck next time!"})
        st.session_state.messages.append({"role": "Bunty", "content": "The key strategy is to always switch, which statistically gives you a 2/3 chance of winning."})
        st.session_state.game_state = "game_over"

    # Handle non-game related queries or unrecognized inputs
    elif st.session_state.game_state not in ["init", "game_over"]:
        # If the input doesn't match expected game responses, treat it as a general query
        response = llm.predict(user_input)
        st.session_state.messages.append({"role": "Bunty", "content": response})
    else:
        # Reset the game or handle post-game conversation
        st.session_state.messages.append({"role": "Bunty", "content": "Do you want to play again or ask something else? (play/ask)"})
        st.session_state.game_state = "init"  # Reset game state for simplicity; adjust based on desired flow


# Display existing messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.text_area("You:", value=message["content"], height=100, key=f"user_{st.session_state.messages.index(message)}", disabled=True)
    else:  # Bunty's messages
        st.text_area("Bunty:", value=message["content"], height=100, key=f"assistant_{st.session_state.messages.index(message)}", disabled=True)

# User input
user_input = st.text_input("Enter your message", "")

# When the user submits a message
if st.button("Send") and user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Handle the message based on game state or forward to OpenAI
    handle_message(user_input)

    # Clear the input box after sending the message
    st.experimental_rerun()
