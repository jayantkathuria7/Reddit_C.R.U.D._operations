import os
import logging
from dotenv import load_dotenv
from io import StringIO
import streamlit as st

# Set up logging
logger = logging.getLogger(__name__)

# Function to load environment variables from uploaded file
def load_credentials_from_file(uploaded_file):
    if uploaded_file is not None:
        try:
            # Read the content of the uploaded file
            content = uploaded_file.getvalue().decode("utf-8")

            # Debugging: Show the content of the .env file
            # st.text(content)  # This will display the content for debugging

            # Use StringIO to simulate a file for dotenv
            env_data = StringIO(content)
            load_dotenv(stream=env_data)

            # Check if environment variables are loaded correctly
            # logger.info(f"REDDIT_CLIENT_ID: {os.getenv('REDDIT_CLIENT_ID')}")
            # logger.info(f"REDDIT_CLIENT_SECRET: {os.getenv('REDDIT_CLIENT_SECRET')}")
            # logger.info(f"REDDIT_USER_AGENT: {os.getenv('REDDIT_USER_AGENT')}")
            # logger.info(f"REDDIT_USERNAME1: {os.getenv('REDDIT_USERNAME')}")
            # logger.info(f"REDDIT_PASSWORD: {os.getenv('REDDIT_PASSWORD')}")

            logger.info("Credentials loaded successfully from uploaded file.")
            return True
        except Exception as e:
            logger.error(f"Failed to load credentials from file: {e}")
            st.error("Failed to load credentials. Please upload a valid .env file.")
            return False
    else:
        st.error("No file uploaded. Please upload your credentials.env file.")
        return False
