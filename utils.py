import os
import logging
import streamlit as st
from dotenv import load_dotenv
from io import StringIO

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load credentials from uploaded file
def load_credentials_from_file(uploaded_file):
    if uploaded_file is not None:
        try:
            content = uploaded_file.getvalue().decode("utf-8")
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
