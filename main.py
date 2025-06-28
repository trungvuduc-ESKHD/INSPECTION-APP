import sys, os
sys.path.append(os.path.abspath('.')) 

import streamlit as st
from streamlit_option_menu import option_menu

# Import các hàm cần thiết
from src.core.session_manager import initialize_session_state
from src.core.auth import init_user_db
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
        
        if st.session_state.role == 'manager':
            options.append("Quản lý (Manager)")
            icons.append("person-check")
        if st.session_state.role == 'super_admin':
            # Super Admin có tất cả quyền của Manager
            if "Quản lý (Manager)" not in options:
                options.append("Quản lý (Manager)")
                icons.append("person-check")
            # và thêm quyền của riêng mình
            options.append("Super Admin Panel")
            icons.append("gem")
            
        selected_page = option_menu(
            menu_title="Điều hướng",
            options=options,
            icons=icons,
            menu_icon="cast",
            default_index=0,
        )
        
        st.markdown("---")
        if st.button("Đăng xuất / Logout"):
            for key in ['logged_in', 'username', 'role', 'current_report_id', 'inspection_data']:
                if key in st.session_state: del st.session_state[key]
            st.rerun()

    # --- HIỂN THỊ TRANG TƯƠNG ỨNG VỚI LỰA CHỌN TRÊN MENU ---
    if selected_page == "Trang chủ":
        render_homepage()
        
    elif selected_page == "Danh sách Báo cáo":
        # Hàm này bây giờ sẽ là trang giám định chính
        render_inspection_page()
        
    elif selected_page == "Quản lý (Manager)":
        render_manager_panel_page()
        
    elif selected_page == "Super Admin Panel":
        render_super_admin_panel_page()

# --- BỘ ĐIỀU PHỐI CHÍNH ---
def main():
    st.set_page_config(page_title="Eurofins Inspection", layout="wide")
    
    init_user_db()
    initialize_session_state()

    if not st.session_state.get('logged_in'):
        render_auth_page()
    else:
        render_main_app()

if __name__ == "__main__":
    main()