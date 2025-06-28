import streamlit as st

def create_styled_header(title, style_class="eurofins-blue"):
    """Create a styled header with Eurofins branding"""
    return st.markdown(f'<div class="{style_class}"><h3>{title}</h3></div>', unsafe_allow_html=True)

def create_bilingual_label(vietnamese, english):
    """Create a bilingual label for Vietnamese and English"""
    return st.markdown(f'<div class="bilingual-label">{vietnamese} / {english}</div>', unsafe_allow_html=True)
