import streamlit as st
import pandas as pd
from src.core.auth import get_users, save_users
import hashlib

def render_super_admin_panel_page():
    st.title("👔 Administrator Panel")
    st.warning("Đây là khu vực nguy hiểm⚠️")

    st.header("Quản lý toàn bộ tài khoản")
    users_data = get_users()
    df_users = pd.DataFrame([{"Username": u, "Role": d.get('role')} for u, d in users_data.items()])
    st.dataframe(df_users, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("⚙️ Chỉnh sửa tài khoản"):
            selected_user = st.selectbox("Chọn tài khoản", options=list(users_data.keys()))
            if selected_user:
                current_role = users_data[selected_user].get('role', 'user')
                new_role = st.selectbox("Vai trò mới", ["user", "admin", "manager", "super_admin"],
                                        index=["user", "admin", "manager", "super_admin"].index(current_role))
                if st.button("Cập nhật vai trò"):
                    users_data[selected_user]['role'] = new_role
                    save_users(users_data)
                    st.success(f"Đã cập nhật vai trò cho '{selected_user}'."); st.rerun()

    with col2:
        with st.expander("🗑️ Xóa tài khoản"):
            options_to_delete = [u for u in users_data.keys() if u != st.session_state.username]
            user_to_delete = st.selectbox("Chọn tài khoản để xóa", options=options_to_delete)
            if st.button("XÁC NHẬN XÓA TÀI KHOẢN", type="primary"):
                if user_to_delete:
                    del users_data[user_to_delete]
                    save_users(users_data)
                    st.success(f"Đã xóa tài khoản '{user_to_delete}'."); st.rerun()
