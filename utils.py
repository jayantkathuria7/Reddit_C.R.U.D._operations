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

            # Use StringIO to simulate a file for dotenv
            env_data = StringIO(content)
            load_dotenv(stream=env_data)

            logger.info("Credentials loaded successfully from uploaded file.")
            return True
        except Exception as e:
            logger.error(f"Failed to load credentials from file: {e}")
            st.error("Failed to load credentials. Please upload a valid .env file.")
            return False
    else:
        st.error("No file uploaded. Please upload your credentials.env file.")
        return False
