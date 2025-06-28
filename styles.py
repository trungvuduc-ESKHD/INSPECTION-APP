import streamlit as st

def load_css():
    st.markdown("""
    <style>
        .eurofins-blue {
            background-color: #005587;
            padding: 10px;
            color: white;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .eurofins-green {
            background-color: #78BE20;
            padding: 10px;
            color: white;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .bilingual-label {
            font-weight: bold;
        }
        
        /* Make the tabs larger and more prominent */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1px;
            background-color: white;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            font-size: 16px;
            font-weight: 500;
            background-color: #f1f3f4;
            padding: 10px 20px;
            border-radius: 5px 5px 0 0;
        }
        .stTabs [aria-selected="true"] {
            background-color: #005587;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

def create_header():
    st.markdown("""
    <div style="background-color: #005587; padding: 15px; display: flex; align-items: center; color: white; margin-bottom: 20px;">
        <h1 style="margin: 0; font-size: 24px;">Eurofins Inspection System</h1>
    </div>
    """, unsafe_allow_html=True)

def create_title():
    st.markdown("""
    <div style="background-color: #78BE20; padding: 15px; color: white; border-radius: 5px; margin-bottom: 20px;">
        <h2 style="margin: 0; font-size: 20px;">BÁO CÁO GIÁM ĐỊNH / INSPECTION REPORT</h2>
    </div>
    """, unsafe_allow_html=True)