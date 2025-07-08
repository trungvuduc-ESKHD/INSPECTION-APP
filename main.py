import streamlit as st
from src.core.auth import sign_in, sign_up
from src.core.supabase_client import supabase
from src.ui.auth_page import render_auth_page

st.set_page_config(page_title="Login - Eurofins", layout="centered")

# --- QUẢN LÝ SESSION ---
if 'user' not in st.session_state:
    st.session_state.user = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None

# Nếu đã đăng nhập, tự động chuyển trang
if st.session_state.user:
    st.switch_page("pages/1_🏠_Homepage.py")

# --- GIAO DIỆN ---
st.title("Hệ thống Giám định Eurofins")
login_tab, signup_tab = st.tabs(["🔐 Đăng nhập", "✍️ Đăng ký"])

with login_tab:
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        if st.form_submit_button("Đăng nhập"):
            user, username, role = sign_in(email, password)
            if user:
                st.session_state.user = user
                st.session_state.username = username
                st.session_state.role = role
                st.switch_page("pages/1_🏠_Homepage.py")
            else:
                st.error(f"Đăng nhập thất bại: {role}") # role sẽ chứa thông báo lỗi

with signup_tab:
    with st.form("signup_form"):
        email = st.text_input("Email")
        username = st.text_input("Tên hiển thị (Username)")
        password = st.text_input("Mật khẩu (ít nhất 6 ký tự)", type="password")
        if st.form_submit_button("Đăng ký"):
            success, message = sign_up(email, password, username)
            if success:
                st.success(message)
            else:
                st.error(f"Đăng ký thất bại: {message}")
