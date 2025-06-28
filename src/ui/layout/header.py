import streamlit as st

def create_header():
    """Create the main application header"""
    st.markdown("""
    <div style="background-color: #005587; padding: 15px; display: flex; align-items: center; color: white; margin-bottom: 20px;">
        <h1 style="margin: 0; font-size: 24px;">Eurofins Inspection System</h1>
    </div>
    """, unsafe_allow_html=True)

def create_title():
    """Create the inspection report title"""
    st.markdown("""
    <div style="background-color: #78BE20; padding: 15px; color: white; border-radius: 5px; margin-bottom: 20px;">
        <h2 style="margin: 0; font-size: 20px;">BÁO CÁO GIÁM ĐỊNH / INSPECTION REPORT</h2>
    </div>
    """, unsafe_allow_html=True)
