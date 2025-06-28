import streamlit as st
from src.core.auth import check_login, register_user

def render_auth_page():
    st.title("Hệ thống Giám định Eurofins")
    st.subheader("Vui lòng đăng nhập hoặc đăng ký để tiếp tục")

    login_tab, signup_tab = st.tabs(["🔐 Đăng nhập (Login)", "✍️ Đăng ký (Sign Up)"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Tên đăng nhập / Username")
            password = st.text_input("Mật khẩu / Password", type="password")
            submitted = st.form_submit_button("Đăng nhập")

            if submitted:
                role = check_login(username, password)
                if role:
                    st.success(f"Đăng nhập thành công với vai trò: {role}")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = role
                    st.rerun()
                else:
                    st.error("Tên đăng nhập hoặc mật khẩu không chính xác.")

    with signup_tab:
        with st.form("signup_form"):
            new_username = st.text_input("Tên đăng nhập mới / New Username")
            new_password = st.text_input("Mật khẩu mới / New Password", type="password")
            confirm_password = st.text_input("Xác nhận mật khẩu / Confirm Password", type="password")
            signup_submitted = st.form_submit_button("Đăng ký")

            if signup_submitted:
                if new_password != confirm_password:
                    st.error("Mật khẩu xác nhận không khớp.")
                else:
                    success, message = register_user(new_username, new_password)
                    if success:
                        st.success(message + " Bây giờ bạn có thể đăng nhập.")
                    else:
                        st.error(message)