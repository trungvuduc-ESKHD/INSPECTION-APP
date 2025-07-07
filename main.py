import streamlit as st
import sys, os

# Thêm đường dẫn vào sys.path để import từ thư mục src
sys.path.append(os.path.abspath('.'))

# Import các hàm render giao diện
from src.ui.auth_page import render_auth_page
from src.ui.homepage import render_homepage
from src.core.auth import sign_out

# Cấu hình trang - chỉ cần làm một lần ở đây
st.set_page_config(page_title="Eurofins System", layout="wide")

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
