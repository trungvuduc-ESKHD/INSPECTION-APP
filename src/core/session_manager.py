# src/core/session_manager.py (SIMPLIFIED)
import streamlit as st

def initialize_session_state():
    """Khởi tạo các biến session state cần thiết cho luồng làm việc."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'current_report_id' not in st.session_state:
        st.session_state.current_report_id = None
    if 'inspection_data' not in st.session_state:
        st.session_state.inspection_data = None