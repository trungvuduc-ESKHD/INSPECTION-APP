import streamlit as st

def load_css():
    """Load custom CSS styles for the application"""
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
