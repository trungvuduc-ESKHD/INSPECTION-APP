# src/ui/auth_page.py (DARK THEME LOGIN/SIGNUP)

import streamlit as st
from src.core.auth import sign_in, sign_up

def render_auth_page():
    """Renders the dark-themed, modern login and sign-up page."""

    # --- CSS TÙY CHỈNH ---
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Nền của toàn bộ trang */
    [data-testid="stAppViewContainer"] > .main {
        background-color: #111827; /* Dark background */
    }

    /* Bỏ qua header mặc định của Streamlit */
    [data-testid="stHeader"] {
        background-color: transparent;
    }
    
    .auth-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100vh;
        padding: 20px;
    }

    .auth-form {
        width: 100%;
        max-width: 400px;
        padding: 2rem;
    }
    
    .auth-form h2 {
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 24px;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Các ô input */
    .stTextInput label {
        color: #9CA3AF; /* Light gray for labels */
        font-weight: 500;
    }
    
    .stTextInput input, .stTextInput textarea {
        background-color: #1F2937;
        color: #F9FAFB;
        border: 1px solid #374151;
        border-radius: 8px;
    }
    
    /* Nút bấm chính */
    .stButton > button {
        width: 100%;
        border-radius: 8px !important;
        background-color: #4ADE80 !important; /* Bright green */
        color: #111827 !important; /* Dark text */
        font-weight: 600 !important;
        border: none !important;
        padding: 0.75rem 0 !important;
        margin-top: 1rem;
    }
    
    /* Link phụ */
    .sub-link {
        text-align: center;
        margin-top: 1.5rem;
    }
    
    .sub-link a {
        color: #60A5FA;
        text-decoration: none;
        font-weight: 500;
    }
    
    .sub-link p {
        color: #9CA3AF;
    }

    /* Đường kẻ 'or continue with' */
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        color: #4B5563;
        margin: 1.5rem 0;
    }
    .divider::before, .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #374151;
    }
    .divider:not(:empty)::before {
        margin-right: .5em;
    }
    .divider:not(:empty)::after {
        margin-left: .5em;
    }
    
    </style>
    """, unsafe_allow_html=True)
    
    # --- BỐ CỤC GIAO DIỆN ---
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    _, center_col, _ = st.columns([1, 1.5, 1])

    with center_col:
        if 'auth_form_choice' not in st.session_state:
            st.session_state.auth_form_choice = 'Sign In'
        
        # --- Form Đăng nhập ---
        if st.session_state.auth_form_choice == 'Sign In':
            with st.container():
                st.markdown('<div class="auth-form">', unsafe_allow_html=True)
                st.markdown("<h2>Sign In to Your Account</h2>", unsafe_allow_html=True)
                
                with st.form("login_form_dark"):
                    email = st.text_input("Email address", key="login_email")
                    password = st.text_input("Password", type="password", key="login_password")
                    # st.checkbox("Remember me", key="login_remember") # Bỏ qua checkbox này cho đơn giản
                    submitted = st.form_submit_button("Sign In")

                    if submitted:
                        # SỬA Ở ĐÂY: Dùng hàm sign_in
                        user, username, role = sign_in(email, password)
                        if user:
                            st.session_state.user = user
                            st.session_state.username = username
                            st.session_state.role = role
                            # Không dùng st.rerun(), switch_page sẽ xử lý việc tải lại
                            st.switch_page("pages/1_🏠_Homepage.py") 
                        else:
                            # role sẽ chứa thông báo lỗi từ sign_in
                            st.error(f"Đăng nhập thất bại: {role}") 
                
                # Sử dụng cột để đặt nút chuyển đổi bên cạnh link
                col1, col2 = st.columns([2,1])
                with col1:
                    st.markdown('<div class="sub-link" style="text-align:left;"><p>Don\'t have an account? <a href="#">Sign up</a></p></div>', unsafe_allow_html=True)
                with col2:
                    if st.button("Sign Up", key="switch_to_signup_btn"):
                        st.session_state.auth_form_choice = 'Sign Up'
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

        # --- Form Đăng ký ---
        elif st.session_state.auth_form_choice == 'Sign Up':
            with st.container():
                st.markdown('<div class="auth-form">', unsafe_allow_html=True)
                st.markdown("<h2>Create a New Account</h2>", unsafe_allow_html=True)
                
                with st.form("signup_form_dark"):
                    email = st.text_input("Email address", key="signup_email")
                    username = st.text_input("Username", key="signup_username")
                    password = st.text_input("Password", type="password", key="signup_password")
                    submitted = st.form_submit_button("Sign Up")

                    if submitted:
                        # SỬA Ở ĐÂY: Dùng hàm sign_up
                        success, message = sign_up(email, password, username)
                        if success:
                            st.success(message)
                            st.session_state.auth_form_choice = 'Sign In' 
                            time.sleep(2) # Đợi 2 giây để người dùng đọc thông báo
                            st.rerun()
                        else:
                            st.error(f"Đăng ký thất bại: {message}")
                
                col1, col2 = st.columns([2,1])
                with col1:
                    st.markdown('<div class="sub-link" style="text-align:left;"><p>Already have an account? <a href="#">Sign in</a></p></div>', unsafe_allow_html=True)
                with col2:
                    if st.button("Sign In", key="switch_to_signin_btn"):
                        st.session_state.auth_form_choice = 'Sign In'
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
