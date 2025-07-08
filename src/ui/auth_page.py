import streamlit as st
import sys, os
import time

# Thêm đường dẫn vào sys.path để import từ thư mục src
sys.path.append(os.path.abspath('.'))

# Import các hàm cần thiết
from src.core.auth import sign_in, sign_up, sign_out, reset_password

# Cấu hình trang - chỉ cần làm một lần ở đây
st.set_page_config(page_title="Eurofins System", layout="wide")

def render_auth_page():
    """Renders the modern centered login and sign-up page with optimized layout."""

    # Initialize session state
    if 'auth_form_choice' not in st.session_state:
        st.session_state.auth_form_choice = 'Sign In'
    if 'auth_message' not in st.session_state:
        st.session_state.auth_message = ('', '')

    # --- CUSTOM CSS ---
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {{
        margin: 0 !important;
        padding: 0 !important;
        height: 100vh !important;
        overflow: hidden !important;
    }}

    .stApp {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        margin: 0 !important;
        padding: 0 !important;
        height: 100vh !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: 0 !important;
        padding: 0 !important;
        height: 100vh !important;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0 !important;
        margin: 0 !important;
        height: 100vh !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    [data-testid="stHeader"], 
    [data-testid="stToolbar"],
    footer,
    .stDeployButton,
    [data-testid="stDecoration"] {{
        display: none !important;
    }}

    /* Hide default streamlit spacing */
    .block-container {{
        padding: 0 !important;
        margin: 0 !important;
        max-width: none !important;
        height: 100vh !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    /* Remove any top spacing */
    .element-container {{
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* Remove gap between elements */
    .stVerticalBlock {{
        gap: 0 !important;
    }}

    .auth-container {{
        width: 100%;
        max-width: 420px;
        padding: 0 20px;
        position: relative;
    }}

    .auth-container::before {{
        content: '';
        position: absolute;
        top: -50px;
        left: -50px;
        right: -50px;
        bottom: -50px;
        background: 
            radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 40% 70%, rgba(139, 92, 246, 0.15) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }}

    .brand-logo {{
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
    }}

    .brand-logo .logo-icon {{
        width: 80px;
        height: 80px;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        border-radius: 50%;
        margin: 0 auto 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        animation: logoFloat 3s ease-in-out infinite;
    }}

    @keyframes logoFloat {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}

    .brand-logo .brand-name {{
        color: white;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }}

    .brand-logo .brand-tagline {{
        color: rgba(255, 255, 255, 0.8);
        font-size: 14px;
        margin: 0.5rem 0 0;
        font-weight: 400;
    }}

    .auth-form {{
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 25px 50px -12px rgba(0, 0, 0, 0.25),
            0 0 0 1px rgba(255, 255, 255, 0.1);
        padding: 2.5rem;
        position: relative;
        z-index: 1;
        animation: formSlideIn 0.8s ease-out;
    }}

    @keyframes formSlideIn {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .auth-form h2 {{
        color: #1F2937;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 28px;
        text-align: center;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    .auth-subtitle {{
        color: #6B7280;
        font-size: 14px;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 400;
    }}

    .stTextInput label {{
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        margin-bottom: 0.5rem !important;
    }}

    .stTextInput input, .stTextInput textarea {{
        background-color: rgba(255, 255, 255, 0.8) !important;
        color: #1F2937 !important;
        border: 1.5px solid rgba(209, 213, 219, 0.8) !important;
        border-radius: 12px !important;
        padding: 0.875rem 1rem !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        transition: all 0.3s ease !important;
    }}

    .stTextInput input:focus, .stTextInput textarea:focus {{
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        outline: none !important;
        background-color: rgba(255, 255, 255, 0.95) !important;
        transform: translateY(-2px) !important;
    }}

    .stButton > button {{
        width: 100% !important;
        border-radius: 12px !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        border: none !important;
        padding: 0.875rem 0 !important;
        margin-top: 1.5rem !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }}

    .stButton > button:hover {{
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }}

    .switch-link {{
        text-align: center;
        margin-top: 1.5rem;
        color: #6B7280;
        font-size: 14px;
    }}

    .link-button {{
        background: none;
        border: none;
        color: #667eea;
        text-decoration: none;
        font-weight: 500;
        cursor: pointer;
        padding: 0;
        font: inherit;
        transition: color 0.3s ease;
        display: inline;
    }}

    .link-button:hover {{
        color: #5a67d8;
        text-decoration: underline;
    }}

    .forgot-password {{
        text-align: right;
        margin-top: -10px;
        margin-bottom: 15px;
        font-size: 14px;
    }}

    .auth-message {{
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 14px;
        text-align: center;
        animation: messageSlide 0.5s ease-out;
    }}

    @keyframes messageSlide {{
        from {{
            opacity: 0;
            transform: translateY(-10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .success-message {{
        background-color: #f0fff4;
        color: #2f855a;
        border: 1px solid #c6f6d5;
    }}

    .error-message {{
        background-color: #fff5f5;
        color: #c53030;
        border: 1px solid #fed7d7;
    }}

    .floating-shapes {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    }}

    .shape {{
        position: absolute;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        animation: floatShapes 20s linear infinite;
    }}

    .shape:nth-child(1) {{
        width: 100px;
        height: 100px;
        left: 10%;
        animation-delay: 0s;
    }}

    .shape:nth-child(2) {{
        width: 150px;
        height: 150px;
        right: 10%;
        animation-delay: -7s;
    }}

    .shape:nth-child(3) {{
        width: 80px;
        height: 80px;
        left: 70%;
        animation-delay: -14s;
    }}

    @keyframes floatShapes {{
        0% {{
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }}
        10% {{
            opacity: 1;
        }}
        90% {{
            opacity: 1;
        }}
        100% {{
            transform: translateY(-100px) rotate(360deg);
            opacity: 0;
        }}
    }}

    @media (max-width: 480px) {{
        .auth-container {{
            padding: 0 15px;
        }}
        
        .auth-form {{
            padding: 2rem 1.5rem;
        }}
        
        .auth-form h2 {{
            font-size: 24px;
        }}

        .brand-logo .logo-icon {{
            width: 60px;
            height: 60px;
            font-size: 24px;
        }}

        .brand-logo .brand-name {{
            font-size: 20px;
        }}
    }}

    ::-webkit-scrollbar {{
        width: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: rgba(255, 255, 255, 0.1);
    }}

    ::-webkit-scrollbar-thumb {{
        background: rgba(102, 126, 234, 0.3);
        border-radius: 4px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(102, 126, 234, 0.5);
    }}

    /* Hide the form switch buttons */
    [data-testid="stButton"] button[kind="secondary"] {{
        display: none !important;
    }}

    </style>
    """, unsafe_allow_html=True)

    # Floating background shapes
    st.markdown("""
    <div class="floating-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    """, unsafe_allow_html=True)

    # --- PAGE LAYOUT ---
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)

    # Brand Logo Section
    st.markdown("""
    <div class="brand-logo">
        <div class="logo-icon">🔬</div>
        <h1 class="brand-name">Eurofins System</h1>
        <p class="brand-tagline">Advanced Fruit Quality Analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # Display auth messages if they exist
    if st.session_state.auth_message[0]:
        msg_type, msg_content = st.session_state.auth_message
        st.markdown(
            f'<div class="auth-message {msg_type}-message">{msg_content}</div>',
            unsafe_allow_html=True
        )
        # Clear message after display
        st.session_state.auth_message = ('', '')

    # --- SIGN IN FORM ---
    if st.session_state.auth_form_choice == 'Sign In':
        with st.form("login_form_dark"):
            st.markdown('<div class="auth-form">', unsafe_allow_html=True)
            st.markdown("<h2>Welcome Back</h2>", unsafe_allow_html=True)
            st.markdown('<p class="auth-subtitle">Sign in to your account to continue</p>', unsafe_allow_html=True)
            
            email = st.text_input("Email address", key="login_email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
            
            # Forgot password link
            st.markdown(
                '<div class="forgot-password">'
                '<button class="link-button" type="button" onclick="handleForgotPassword()">Forgot password?</button>'
                '</div>',
                unsafe_allow_html=True
            )
            
            submitted = st.form_submit_button("Sign In")
            
            if submitted:
                if email and password:
                    user, username, role = sign_in(email, password)
                    if user:
                        st.session_state.user = user
                        st.session_state.username = username
                        st.session_state.role = role
                        st.session_state.auth_message = ('success', "🎉 Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.session_state.auth_message = ('error', f"❌ Login failed: {role}")
                        st.rerun()
                else:
                    st.session_state.auth_message = ('error', "❌ Please fill in all fields")
                    st.rerun()
            
            # Switch to sign up
            st.markdown(
                '<div class="switch-link">'
                '<p>Don\'t have an account? <button class="link-button" type="button" onclick="handleSignUp()">Create one</button></p>'
                '</div>',
                unsafe_allow_html=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)

    # --- SIGN UP FORM ---
    elif st.session_state.auth_form_choice == 'Sign Up':
        with st.form("signup_form_dark"):
            st.markdown('<div class="auth-form">', unsafe_allow_html=True)
            st.markdown("<h2>Create Account</h2>", unsafe_allow_html=True)
            st.markdown('<p class="auth-subtitle">Join us today and get started</p>', unsafe_allow_html=True)
            
            email = st.text_input("Email address", key="signup_email", placeholder="Enter your email")
            username = st.text_input("Username", key="signup_username", placeholder="Choose a username")
            password = st.text_input("Password", type="password", key="signup_password", placeholder="Create a strong password")
            
            submitted = st.form_submit_button("Create Account")
            
            if submitted:
                if email and username and password:
                    success, message = sign_up(email, password, username)
                    if success:
                        st.session_state.auth_message = ('success', f"🎉 {message}")
                        st.session_state.auth_form_choice = 'Sign In'
                        st.rerun()
                    else:
                        st.session_state.auth_message = ('error', f"❌ Registration failed: {message}")
                        st.rerun()
                else:
                    st.session_state.auth_message = ('error', "❌ Please fill in all fields")
                    st.rerun()
            
            # Switch to sign in
            st.markdown(
                '<div class="switch-link">'
                '<p>Already have an account? <button class="link-button" type="button" onclick="handleSignIn()">Sign in</button></p>'
                '</div>',
                unsafe_allow_html=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)

    # --- FORGOT PASSWORD FORM ---
    elif st.session_state.auth_form_choice == 'Forgot Password':
        with st.form("forgot_password_form"):
            st.markdown('<div class="auth-form">', unsafe_allow_html=True)
            st.markdown("<h2>Reset Password</h2>", unsafe_allow_html=True)
            st.markdown('<p class="auth-subtitle">Enter your email to reset your password</p>', unsafe_allow_html=True)
            
            email = st.text_input("Email address", key="reset_email", placeholder="Enter your email")
            
            submitted = st.form_submit_button("Send Reset Instructions")
            if submitted:
                if email:
                    success, message = reset_password(email)
                    if success:
                        st.session_state.auth_message = ('success', f"📩 {message}")
                    else:
                        st.session_state.auth_message = ('error', f"❌ {message}")
                    st.session_state.auth_form_choice = 'Sign In'
                    st.rerun()
                else:
                    st.session_state.auth_message = ('error', "❌ Please enter your email address")
                    st.rerun()
            
            # Back to sign in
            st.markdown(
                '<div class="switch-link">'
                '<button class="link-button" type="button" onclick="handleSignIn()">Back to Sign In</button>'
                '</div>',
                unsafe_allow_html=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # --- JAVASCRIPT FOR FORM SWITCHING ---
    st.markdown("""
    <script>
    function handleSignUp() {
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: {auth_form_choice: 'Sign Up'}
        }, '*');
    }

    function handleSignIn() {
        window.parent.postMessage({
            type: 'streamlit:setComponentValue', 
            value: {auth_form_choice: 'Sign In'}
        }, '*');
    }

    function handleForgotPassword() {
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: {auth_form_choice: 'Forgot Password'}
        }, '*');
    }
    </script>
    """, unsafe_allow_html=True)

    # Handle form switching through session state (hidden buttons)
    if st.button("Switch to Sign Up", key="switch_signup", help="Switch forms"):
        st.session_state.auth_form_choice = 'Sign Up'
        st.rerun()

    if st.button("Switch to Sign In", key="switch_signin", help="Switch forms"):
        st.session_state.auth_form_choice = 'Sign In'
        st.rerun()

    if st.button("Switch to Forgot Password", key="switch_forgot", help="Switch forms"):
        st.session_state.auth_form_choice = 'Forgot Password'
        st.rerun()


def render_homepage():
    """Render the homepage when user is logged in"""
    st.title("🏠 Eurofins System - Dashboard")
    st.write("Welcome to the Eurofins System Dashboard!")
    
    # You can add more homepage content here
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Samples", "1,234", "12%")
    
    with col2:
        st.metric("Pending Analysis", "56", "-2%")
    
    with col3:
        st.metric("Completed Tests", "892", "8%")
    
    st.info("This is a placeholder for your homepage content. You can customize this section based on your needs.")


# --- QUẢN LÝ SESSION STATE ---
# Đảm bảo các key cần thiết tồn tại trong session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'auth_form_choice' not in st.session_state:
    st.session_state.auth_form_choice = 'Sign In'

# --- LOGIC ĐIỀU HƯỚNG CHÍNH (CONTROLLER) ---
if st.session_state.user:
    # Nếu đã đăng nhập, hiển thị sidebar và trang chủ
    with st.sidebar:
        st.success(f"Xin chào, {st.session_state.username}!")
        st.write(f"Vai trò: `{st.session_state.role}`")
        if st.button("Đăng xuất", use_container_width=True):
            sign_out()
            # Xóa các thông tin người dùng khỏi session và chạy lại
            del st.session_state.user
            del st.session_state.username
            del st.session_state.role
            st.rerun()
    
    # Gọi hàm render trang chủ
    render_homepage()
else:
    # Nếu chưa đăng nhập, hiển thị trang đăng nhập/đăng ký
    render_auth_page()
