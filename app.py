import streamlit as st
import random
from openai.openai_object import OpenAIObject
import openai

# Load your OpenAI API key from Streamlit's secrets or environment variables
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY
# Custom CSS to inject specified font styles
st.markdown("""
<style>
    html, body, [class*="css"] {
    font-family: 'Comic Sans MS', 'Comic Sans', cursive !important;
    }
</style>
""", unsafe_allow_html=True)
if 'user_stage' not in st.session_state:
    st.session_state.user_stage = 0
    st.session_state.messages = [{"sender": "Bunty", "text": "Hello, I'm Bunty! Do you want to play the Monty Hall game? (yes/no)"}]
