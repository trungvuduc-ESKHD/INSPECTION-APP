import streamlit as st
from src.core.auth import check_login, register_user
# Import các hàm logic từ auth.py
from src.core.auth import sign_in, sign_up 

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
    
    _, center_col, _ = st.columns([1, 1.5, 1])

    with center_col:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        
        # Tiêu đề thay đổi tùy theo form
        if st.session_state.get('auth_form_choice', 'Sign In') == 'Sign In':
             st.markdown("<h2 class='auth-title'>Sign In to Your Account</h2>", unsafe_allow_html=True)
        else:
             st.markdown("<h2 class='auth-title'>Create a New Account</h2>", unsafe_allow_html=True)

        # Sử dụng form để tránh rerun không cần thiết
        if st.session_state.get('auth_form_choice', 'Sign In') == 'Sign In':
            with st.form("login_form_dark"):
                email = st.text_input("Email address", key="login_email")
                password = st.text_input("Password", type="password", key="login_password")
                submitted = st.form_submit_button("Sign In")

                if submitted:
                    user, username, role = sign_in(email, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.username = username
                        st.session_state.role = role
                        st.rerun()
                    else:
                        st.error(f"Đăng nhập thất bại: {role}")
            
            if st.button("Don't have an account? Sign up"):
                st.session_state.auth_form_choice = 'Sign Up'
                st.rerun()

        else: # Form Đăng ký
             with st.form("signup_form_dark"):
                email = st.text_input("Email address", key="signup_email")
                username = st.text_input("Username", key="signup_username")
                password = st.text_input("Password (min. 6 characters)", type="password", key="signup_password")
                submitted = st.form_submit_button("Create Account")

                if submitted:
                    success, message = sign_up(email, password, username)
                    if success:
                        st.success(message + " Bây giờ bạn có thể đăng nhập.")
                        st.success(message)
                        st.session_state.auth_form_choice = 'Sign In' # Tự động chuyển về tab đăng nhập
                        st.rerun()
                    else:
                        st.error(message)
                        st.error(f"Đăng ký thất bại: {message}")
            
             if st.button("Already have an account? Sign in"):
                st.session_state.auth_form_choice = 'Sign In'
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
