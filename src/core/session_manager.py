import streamlit as st
from .auth import get_current_user

def initialize_session_state():
    """
    Khởi tạo session state cho ứng dụng
    """
    # Khởi tạo các biến session state cần thiết
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'current_report_id' not in st.session_state:
        st.session_state.current_report_id = None
    if 'inspection_data' not in st.session_state:
        st.session_state.inspection_data = {}
    
    # Kiểm tra trạng thái đăng nhập hiện tại
    if not st.session_state.user:
        current_user = get_current_user()
        if current_user:
            st.session_state.user = current_user
            # Có thể lấy thêm thông tin username và role từ database nếu cần

def clear_session_state():
    """
    Xóa tất cả session state khi đăng xuất
    """
    keys_to_clear = ['user', 'username', 'role', 'current_report_id', 'inspection_data']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def is_user_logged_in():
    """
    Kiểm tra xem người dùng đã đăng nhập chưa
    
    Returns:
        bool: True nếu đã đăng nhập, False nếu chưa
    """
    return st.session_state.get('user') is not None

def get_user_role():
    """
    Lấy vai trò của người dùng hiện tại
    
    Returns:
        str: Vai trò của người dùng hoặc None nếu chưa đăng nhập
    """
    return st.session_state.get('role')

def has_permission(required_role):
    """
    Kiểm tra xem người dùng có quyền truy cập không
    
    Args:
        required_role (str): Vai trò cần thiết ('user', 'manager', 'super_admin')
        
    Returns:
        bool: True nếu có quyền, False nếu không
    """
    if not is_user_logged_in():
        return False
    
    user_role = get_user_role()
    
    # Định nghĩa thứ tự quyền hạn
    role_hierarchy = {
        'user': 1,
        'manager': 2,
        'super_admin': 3
    }
    
    if user_role not in role_hierarchy or required_role not in role_hierarchy:
        return False
    
    return role_hierarchy[user_role] >= role_hierarchy[required_role]

def require_auth(func):
    """
    Decorator để yêu cầu người dùng đăng nhập
    """
    def wrapper(*args, **kwargs):
        if not is_user_logged_in():
            st.error("Bạn cần đăng nhập để truy cập trang này!")
            st.stop()
        return func(*args, **kwargs)
    return wrapper

def require_role(required_role):
    """
    Decorator để yêu cầu vai trò cụ thể
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not has_permission(required_role):
                st.error(f"Bạn không có quyền truy cập! Cần vai trò: {required_role}")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    return decorator
