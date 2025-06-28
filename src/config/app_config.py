import streamlit as st

def setup_app_config():
    """Set up Streamlit page configuration"""
    st.set_page_config(
        page_title="Eurofins Inspection System",
        page_icon="📋",
        layout="wide",
        initial_sidebar_state="collapsed"
    )