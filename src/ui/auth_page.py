import streamlit as st
import time
from src.core.auth import sign_in, sign_up

def render_auth_page():
    """Renders the modern dark-themed login and sign-up page with enhanced functionality."""
    
    # Initialize session state
    if 'auth_form_choice' not in st.session_state:
        st.session_state.auth_form_choice = 'Sign In'
    if 'auth_message' not in st.session_state:
        st.session_state.auth_message = ('', '')
    
    # --- CUSTOM CSS ---
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }}

    [data-testid="stHeader"], 
    [data-testid="stToolbar"],
    footer {{
        display: none;
    }}
    
    .auth-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 20px;
        position: relative;
    }}

    .auth-container::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 40% 70%, rgba(139, 92, 246, 0.15) 0%, transparent 50%);
        pointer-events: none;
    }}

    .auth-form {{
        width: 100%;
        max-width: 420px;
        padding: 3rem 2.5rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 25px 50px -12px rgba(0, 0, 0, 0.25),
            0 0 0 1px rgba(255, 255, 255, 0.1);
        position: relative;
        z-index: 1;
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
    
    .switch-btn {{
        background: transparent !important;
        border: 1.5px solid rgba(102, 126, 234, 0.6) !important;
        color: #667eea !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
    }}
    
    .switch-btn:hover {{
        background: rgba(102, 126, 234, 0.1) !important;
        border-color: #667eea !important;
        transform: translateY(-1px) !important;
    }}
    
    .sub-link {{
        text-align: left;
        margin-top: 1.5rem;
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
    
    .divider {{
        display: flex;
        align-items: center;
        text-align: center;
        color: #9CA3AF;
        margin: 2rem 0;
        font-size: 14px;
        font-weight: 400;
    }}
    .divider::before, .divider::after {{
        content: '';
        flex: 1;
        border-bottom: 1px solid rgba(209, 213, 219, 0.6);
    }}
    .divider:not(:empty)::before {{
        margin-right: 1rem;
    }}
    .divider:not(:empty)::after {{
        margin-left: 1rem;
    }}

    .loading-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 24px;
        z-index: 10;
    }}

    .forgot-password {{
        text-align: right;
        margin-top: -15px;
        margin-bottom: 20px;
        font-size: 14px;
    }}

    .auth-message {{
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 14px;
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

    @media (max-width: 480px) {{
        .auth-form {{
            padding: 2rem 1.5rem;
            margin: 1rem;
        }}
        
        .auth-form h2 {{
            font-size: 24px;
        }}
    }}

    .stDeployButton {{
        display: none;
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
    
    </style>
    """, unsafe_allow_html=True)
    
    # --- PAGE LAYOUT ---
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Use single centered column for better mobile responsiveness
    with st.container():
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
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
                        '<button class="link-button" type="button">Forgot password?</button>'
                        '</div>',
                        unsafe_allow_html=True
                    )
                    
                    submitted = st.form_submit_button("Sign In")
                    
                    if submitted:
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
                    
                    # Switch to sign up
                    st.markdown(
                        '<div class="sub-link">'
                        '<p>Don\'t have an account? <button class="link-button" type="button">Create one</button></p>'
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
                        success, message = sign_up(email, password, username)
                        if success:
                            st.session_state.auth_message = ('success', f"🎉 {message}")
                            st.session_state.auth_form_choice = 'Sign In'
                            st.rerun()
                        else:
                            st.session_state.auth_message = ('error', f"❌ Registration failed: {message}")
                            st.rerun()
                    
                    # Switch to sign in
                    st.markdown(
                        '<div class="sub-link">'
                        '<p>Already have an account? <button class="link-button" type="button">Sign in</button></p>'
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
                        # In a real app, you would send a password reset email here
                        st.session_state.auth_message = ('success', "📩 Password reset instructions sent to your email")
                        st.session_state.auth_form_choice = 'Sign In'
                        st.rerun()
                    
                    # Back to sign in
                    st.markdown(
                        '<div class="sub-link">'
                        '<button class="link-button" type="button">Back to Sign In</button>'
                        '</div>',
                        unsafe_allow_html=True
                    )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- JAVASCRIPT FOR BUTTON HANDLING ---
    st.markdown("""
    <script>
    // Handle link button clicks
    document.addEventListener('click', function(event) {
        // Create Account button
        if (event.target.textContent === 'Create one') {
            window.streamlitSessionState.set({auth_form_choice: 'Sign Up'}, 'update');
        }
        // Sign In button
        else if (event.target.textContent === 'Sign in') {
            window.streamlitSessionState.set({auth_form_choice: 'Sign In'}, 'update');
        }
        // Forgot Password button
        else if (event.target.textContent === 'Forgot password?') {
            window.streamlitSessionState.set({auth_form_choice: 'Forgot Password'}, 'update');
        }
        // Back to Sign In button
        else if (event.target.textContent === 'Back to Sign In') {
            window.streamlitSessionState.set({auth_form_choice: 'Sign In'}, 'update');
        }
    });
    </script>
    """, unsafe_allow_html=True)

# Run the auth page
render_auth_page()
