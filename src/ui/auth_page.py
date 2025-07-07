# src/ui/auth_page.py (MODERN DARK THEME LOGIN/SIGNUP)

import streamlit as st
import time
from src.core.auth import sign_in, sign_up

def render_auth_page():
    """Renders the modern dark-themed login and sign-up page."""

    # --- CSS TÙY CHỈNH ---
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Reset và thiết lập toàn bộ trang */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a202c 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Nền của toàn bộ trang */
    [data-testid="stAppViewContainer"] > .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a202c 100%);
        padding: 0;
    }

    /* Ẩn header và footer mặc định */
    [data-testid="stHeader"], 
    [data-testid="stToolbar"],
    footer {
        display: none;
    }
    
    /* Container chính */
    .auth-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 20px;
        position: relative;
    }

    /* Hiệu ứng background */
    .auth-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 20%, rgba(74, 222, 128, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(96, 165, 250, 0.1) 0%, transparent 50%);
        pointer-events: none;
    }

    /* Form container */
    .auth-form {
        width: 100%;
        max-width: 420px;
        padding: 3rem 2.5rem;
        background: rgba(31, 41, 55, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(55, 65, 81, 0.5);
        box-shadow: 
            0 25px 50px -12px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(255, 255, 255, 0.05);
        position: relative;
        z-index: 1;
    }

    /* Tiêu đề */
    .auth-form h2 {
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 28px;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #FFFFFF 0%, #E5E7EB 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .auth-subtitle {
        color: #9CA3AF;
        font-size: 14px;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Styling cho các label */
    .stTextInput label {
        color: #E5E7EB !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Styling cho các input */
    .stTextInput input, .stTextInput textarea {
        background-color: rgba(17, 24, 39, 0.8) !important;
        color: #F9FAFB !important;
        border: 1.5px solid rgba(55, 65, 81, 0.6) !important;
        border-radius: 12px !important;
        padding: 0.875rem 1rem !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stTextInput textarea:focus {
        border-color: #4ADE80 !important;
        box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.1) !important;
        outline: none !important;
    }
    
    /* Nút bấm chính */
    .stButton > button {
        width: 100% !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #4ADE80 0%, #22C55E 100%) !important;
        color: #111827 !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        border: none !important;
        padding: 0.875rem 0 !important;
        margin-top: 1.5rem !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        box-shadow: 0 4px 15px rgba(74, 222, 128, 0.3) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(74, 222, 128, 0.4) !important;
    }
    
    /* Nút chuyển đổi phụ */
    .switch-btn {
        background: transparent !important;
        border: 1.5px solid rgba(96, 165, 250, 0.6) !important;
        color: #60A5FA !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }
    
    .switch-btn:hover {
        background: rgba(96, 165, 250, 0.1) !important;
        border-color: #60A5FA !important;
        transform: translateY(-1px) !important;
    }
    
    /* Link phụ */
    .sub-link {
        text-align: left;
        margin-top: 1.5rem;
    }
    
    .sub-link a {
        color: #60A5FA;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s ease;
    }
    
    .sub-link a:hover {
        color: #93C5FD;
    }
    
    .sub-link p {
        color: #9CA3AF;
        font-size: 14px;
        margin: 0;
    }

    /* Đường kẻ 'or continue with' */
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        color: #6B7280;
        margin: 2rem 0;
        font-size: 14px;
        font-weight: 400;
    }
    .divider::before, .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid rgba(55, 65, 81, 0.6);
    }
    .divider:not(:empty)::before {
        margin-right: 1rem;
    }
    .divider:not(:empty)::after {
        margin-left: 1rem;
    }

    /* Hiệu ứng loading */
    .loading-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(31, 41, 55, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 20px;
        z-index: 10;
    }

    /* Responsive */
    @media (max-width: 480px) {
        .auth-form {
            padding: 2rem 1.5rem;
            margin: 1rem;
        }
        
        .auth-form h2 {
            font-size: 24px;
        }
    }

    /* Ẩn các thành phần Streamlit không cần thiết */
    .stDeployButton {
        display: none;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(31, 41, 55, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(55, 65, 81, 0.8);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(75, 85, 99, 0.9);
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
                st.markdown("<h2>Welcome Back</h2>", unsafe_allow_html=True)
                st.markdown('<p class="auth-subtitle">Sign in to your account to continue</p>', unsafe_allow_html=True)
                
                with st.form("login_form_dark"):
                    email = st.text_input("Email address", key="login_email", placeholder="Enter your email")
                    password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
                    submitted = st.form_submit_button("Sign In")

                    if submitted:
                        # SỬA Ở ĐÂY: Dùng hàm sign_in
                        user, username, role = sign_in(email, password)
                        if user:
                            st.session_state.user = user
                            st.session_state.username = username
                            st.session_state.role = role
                            st.success("🎉 Đăng nhập thành công!")
                            time.sleep(1)
                            st.switch_page("pages/1_🏠_Homepage.py") 
                        else:
                            st.error(f"❌ Đăng nhập thất bại: {role}") 
                
                # Sử dụng cột để đặt nút chuyển đổi bên cạnh link
                col1, col2 = st.columns([2.5, 1])
                with col1:
                    st.markdown('<div class="sub-link"><p>Don\'t have an account? <a href="#">Create one</a></p></div>', unsafe_allow_html=True)
                with col2:
                    if st.button("Sign Up", key="switch_to_signup_btn"):
                        st.session_state.auth_form_choice = 'Sign Up'
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

        # --- Form Đăng ký ---
        elif st.session_state.auth_form_choice == 'Sign Up':
            with st.container():
                st.markdown('<div class="auth-form">', unsafe_allow_html=True)
                st.markdown("<h2>Create Account</h2>", unsafe_allow_html=True)
                st.markdown('<p class="auth-subtitle">Join us today and get started</p>', unsafe_allow_html=True)
                
                with st.form("signup_form_dark"):
                    email = st.text_input("Email address", key="signup_email", placeholder="Enter your email")
                    username = st.text_input("Username", key="signup_username", placeholder="Choose a username")
                    password = st.text_input("Password", type="password", key="signup_password", placeholder="Create a strong password")
                    submitted = st.form_submit_button("Create Account")

                    if submitted:
                        # SỬA Ở ĐÂY: Dùng hàm sign_up
                        success, message = sign_up(email, password, username)
                        if success:
                            st.success(f"🎉 {message}")
                            st.session_state.auth_form_choice = 'Sign In' 
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(f"❌ Đăng ký thất bại: {message}")
                
                col1, col2 = st.columns([2.5, 1])
                with col1:
                    st.markdown('<div class="sub-link"><p>Already have an account? <a href="#">Sign in</a></p></div>', unsafe_allow_html=True)
                with col2:
                    if st.button("Sign In", key="switch_to_signin_btn"):
                        st.session_state.auth_form_choice = 'Sign In'
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
