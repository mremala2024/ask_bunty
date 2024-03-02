import streamlit as st
import os
import openai

# Ensure the openai package is installed: pip install openai

# Load the OpenAI API key from an environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the API key is not found and display an error message
if OPENAI_API_KEY is None:
    st.error("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Configure the OpenAI library with your API key
openai.api_key = OPENAI_API_KEY

class OpenAI:
    @staticmethod
    def predict(prompt):
        # Make a call to the OpenAI API using the provided prompt
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",  # Or use "gpt-3.5-turbo" or another appropriate engine
                prompt=prompt,
                temperature=0.7,
                max_tokens=150,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            # Return the text of the first choice in the response
            return response.choices[0].text.strip()
        except Exception as e:
            return f"An error occurred: {str(e)}"

# The rest of your Streamlit app setup goes here...
