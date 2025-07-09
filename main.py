import sys, os
sys.path.append(os.path.abspath('.')) 

import streamlit as st
from streamlit_option_menu import option_menu

# Import các hàm cần thiết
from src.core.session_manager import initialize_session_state
from src.core.auth import sign_out, get_current_user
from src.ui.auth_page import render_auth_page
from src.ui.homepage import render_homepage
from src.ui.inspection_page import render_inspection_page
from src.ui.manager_panel import render_manager_panel_page
from src.ui.super_admin_panel import render_super_admin_panel_page

def render_main_app():
    """Vẽ giao diện chính sau khi người dùng đã đăng nhập."""
    with st.sidebar:
        st.success(f"Xin chào, {st.session_state.username}!")
        st.write(f"Vai trò: **{st.session_state.role}**")

        # Xây dựng menu động dựa trên vai trò
        options = ["Trang chủ", "Danh sách Báo cáo"]
        icons = ["house", "card-list"]

        if st.session_state.role in ['manager', 'super_admin']:
            options.append("Quản lý (Manager)")
            icons.append("person-check")

        if st.session_state.role == 'super_admin':
            options.append("Super Admin Panel")
            icons.append("gem")

        # Nếu chưa có biến lưu lựa chọn, khởi tạo là None (không chọn mục nào)
        if "selected_page" not in st.session_state:
            st.session_state.selected_page = None

        # Xác định default_index cho option_menu
        if st.session_state.selected_page in options:
            default_idx = options.index(st.session_state.selected_page)
        else:
            # Nếu không hợp lệ, đặt default_index là None để không chọn mục nào
            default_idx = None

        selected_page = option_menu(
            menu_title="Điều hướng",
            options=options,
            icons=icons,
            menu_icon="cast",
            default_index=default_idx,
        )

        # Cập nhật lại session
        st.session_state.selected_page = selected_page

        st.markdown("---")
        if st.button("Đăng xuất / Logout"):
            sign_out()
            for key in ['user', 'username', 'role', 'current_report_id', 'inspection_data', 'selected_page']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    # --- HIỂN THỊ GIAO DIỆN THEO selected_page ---
    if st.session_state.selected_page == "Trang chủ":
        render_homepage()
    elif st.session_state.selected_page == "Danh sách Báo cáo":
        render_inspection_page()
    elif st.session_state.selected_page == "Quản lý (Manager)":
        if st.session_state.role in ['manager', 'super_admin']:
            render_manager_panel_page()
        else:
            st.error("Bạn không có quyền truy cập trang này!")
    elif st.session_state.selected_page == "Super Admin Panel":
        if st.session_state.role == 'super_admin':
            render_super_admin_panel_page()
        else:
            st.error("Bạn không có quyền truy cập trang này!")
    else:
        # Khi không có mục nào được chọn, hoặc mới đăng nhập
        st.info("Vui lòng chọn mục trong menu để bắt đầu.")

# --- BỘ ĐIỀU PHỐI CHÍNH ---
def main():
    st.set_page_config(page_title="Eurofins Inspection", layout="wide")
    
    # Khởi tạo session state
    initialize_session_state()

    # Kiểm tra xem người dùng đã đăng nhập chưa
    # Sử dụng 'user' thay vì 'logged_in' để phù hợp với Supabase auth
    if not st.session_state.get('user'):
        render_auth_page()
    else:
        render_main_app()

if __name__ == "__main__":
    main()
