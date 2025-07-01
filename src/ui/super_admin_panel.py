import streamlit as st
import pandas as pd
from src.core.auth import get_users, save_users
import hashlib

def render_super_admin_panel_page():
    """Renders the super admin panel with modern UI design."""
    
    # Advanced CSS styling for Super Admin Panel
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .super-admin-header {
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 50%, #4a5568 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 24px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .super-admin-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 200, 255, 0.3) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .super-admin-header h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 20px rgba(0,0,0,0.5);
        position: relative;
        z-index: 2;
        background: linear-gradient(135deg, #fff 0%, #f7fafc 50%, #e2e8f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .super-admin-header .crown-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        position: relative;
        z-index: 2;
        animation: crownGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes crownGlow {
        0% { 
            filter: drop-shadow(0 0 10px #ffd700) drop-shadow(0 0 20px #ffd700);
            transform: rotate(-5deg);
        }
        100% { 
            filter: drop-shadow(0 0 20px #ffd700) drop-shadow(0 0 40px #ffd700);
            transform: rotate(5deg);
        }
    }
    
    .super-admin-header .subtitle {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.2rem;
        margin-top: 1rem;
        font-weight: 500;
        position: relative;
        z-index: 2;
    }
    
    .admin-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 2.5rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .admin-main-section {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .admin-main-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #ffd700 0%, #ffed4e 25%, #ff6b6b 50%, #4ecdc4 75%, #45b7d1 100%);
    }
    
    .section-title {
        color: #1a202c;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        margin: 0 0 2rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .section-icon {
        font-size: 2.5rem;
        padding: 0.75rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        animation: iconPulse 4s ease-in-out infinite;
    }
    
    @keyframes iconPulse {
        0%, 100% { transform: scale(1) rotate(0deg); }
        50% { transform: scale(1.05) rotate(2deg); }
    }
    
    .users-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0 3rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        transition: all 0.6s ease;
        transform: scale(0);
    }
    
    .stat-card:hover::before {
        transform: scale(1);
    }
    
    .stat-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
    }
    
    .stat-number {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    
    .stat-label {
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 600;
        position: relative;
        z-index: 1;
    }
    
    .stat-icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
    }
    
    .users-table {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .actions-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        margin-top: 3rem;
    }
    
    .action-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .action-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
    }
    
    .action-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }
    
    .edit-card::before {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .delete-card::before {
        background: linear-gradient(90deg, #ff6b6b 0%, #ee5a52 100%);
    }
    
    .action-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        color: #1a202c;
        font-weight: 700;
        font-size: 1.3rem;
    }
    
    .action-icon {
        font-size: 1.8rem;
        margin-right: 1rem;
        padding: 0.5rem;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .edit-icon {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        box-shadow: 0 4px 20px rgba(79, 172, 254, 0.3);
    }
    
    .delete-icon {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        box-shadow: 0 4px 20px rgba(255, 107, 107, 0.3);
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        display: block;
        color: #4a5568;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }
    
    .danger-zone {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(255, 107, 107, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .danger-zone::before {
        content: '⚠️';
        position: absolute;
        top: 1rem;
        right: 1rem;
        font-size: 2rem;
        opacity: 0.3;
        animation: warningBlink 2s ease-in-out infinite;
    }
    
    @keyframes warningBlink {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 0.7; }
    }
    
    .danger-zone h4 {
        margin: 0 0 0.5rem 0;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .danger-zone p {
        margin: 0;
        opacity: 0.9;
        font-size: 0.95rem;
    }
    
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3);
        display: flex;
        align-items: center;
        animation: successSlide 0.5s ease-out;
    }
    
    @keyframes successSlide {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .success-icon {
        margin-right: 1rem;
        font-size: 1.5rem;
    }
    
    /* Custom Streamlit component styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3) !important;
        font-size: 1rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stSelectbox > div > div {
        border-radius: 12px !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        transition: all 0.3s ease !important;
        background: rgba(255, 255, 255, 0.8) !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .stDataFrame {
        border-radius: 20px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Role badge styling */
    .role-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .role-user { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; }
    .role-admin { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; }
    .role-manager { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; }
    .role-super-admin { background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%); color: #1a202c; }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .actions-grid {
            grid-template-columns: 1fr;
        }
        
        .users-stats {
            grid-template-columns: 1fr;
        }
        
        .super-admin-header h1 {
            font-size: 2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Super Admin Header
    st.markdown("""
    <div class="super-admin-header">
        <div class="crown-icon">👑</div>
        <h1>Supreme Administrator</h1>
        <div class="subtitle">Hệ thống quản lý cấp cao nhất - Toàn quyền kiểm soát</div>
    </div>
    """, unsafe_allow_html=True)

    # Main content grid
    st.markdown('<div class="admin-grid">', unsafe_allow_html=True)
    
    # Main section
    st.markdown("""
    <div class="admin-main-section">
        <h2 class="section-title">
            <div class="section-icon">👥</div>
            Quản lý Toàn bộ Tài khoản
        </h2>
    """, unsafe_allow_html=True)
    
    # Get users data
    users_data = get_users()
    
    if not users_data:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #6b7280;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">👤</div>
            <p style="font-size: 1.2rem;">Không có tài khoản nào trong hệ thống</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # User statistics
        role_counts = {}
        for user_data in users_data.values():
            role = user_data.get('role', 'user')
            role_counts[role] = role_counts.get(role, 0) + 1
        
        total_users = len(users_data)
        user_count = role_counts.get('user', 0)
        admin_count = role_counts.get('admin', 0)
        manager_count = role_counts.get('manager', 0)
        super_admin_count = role_counts.get('super_admin', 0)
        
        st.markdown(f"""
        <div class="users-stats">
            <div class="stat-card">
                <div class="stat-number">{total_users}</div>
                <div class="stat-label"><span class="stat-icon">👥</span>Tổng Tài khoản</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{user_count}</div>
                <div class="stat-label"><span class="stat-icon">👤</span>Người dùng</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{admin_count}</div>
                <div class="stat-label"><span class="stat-icon">⚡</span>Quản trị viên</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{manager_count}</div>
                <div class="stat-label"><span class="stat-icon">👨‍💼</span>Quản lý</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{super_admin_count}</div>
                <div class="stat-label"><span class="stat-icon">👑</span>Super Admin</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Users table
        df_users = pd.DataFrame([{"Username": u, "Role": d.get('role')} for u, d in users_data.items()])
        st.markdown('<div class="users-table">', unsafe_allow_html=True)
        st.dataframe(df_users, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Action cards
        st.markdown('<div class="actions-grid">', unsafe_allow_html=True)
        
        # Edit Account Card
        st.markdown("""
        <div class="action-card edit-card">
            <div class="action-header">
                <div class="action-icon edit-icon">⚙️</div>
                <span>Chỉnh sửa Tài khoản</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        st.markdown('<label class="form-label">👤 Chọn tài khoản để chỉnh sửa</label>', unsafe_allow_html=True)
        selected_user = st.selectbox(
            "", 
            options=list(users_data.keys()),
            key="edit_user_select",
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if selected_user:
            current_role = users_data[selected_user].get('role', 'user')
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<label class="form-label">🎯 Vai trò hiện tại</label>', unsafe_allow_html=True)
            st.markdown(f'<div class="role-badge role-{current_role.replace("_", "-")}">{current_role}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<label class="form-label">🔄 Chọn vai trò mới</label>', unsafe_allow_html=True)
            new_role = st.selectbox(
                "", 
                ["user", "admin", "manager", "super_admin"],
                index=["user", "admin", "manager", "super_admin"].index(current_role),
                key="new_role_select",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            if current_role != new_role:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); color: white; padding: 1rem; border-radius: 12px; margin: 1rem 0;">
                    <strong>⚠️ Thay đổi vai trò:</strong> {current_role} → {new_role}
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("🔄 Cập nhật vai trò", key="update_role_btn", use_container_width=True):
                users_data[selected_user]['role'] = new_role
                save_users(users_data)
                st.markdown(f"""
                <div class="success-message">
                    <span class="success-icon">✅</span>
                    <span>Đã cập nhật vai trò cho '<strong>{selected_user}</strong>' thành <strong>{new_role}</strong></span>
                </div>
                """, unsafe_allow_html=True)
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Delete Account Card
        st.markdown("""
        <div class="action-card delete-card">
            <div class="action-header">
                <div class="action-icon delete-icon">🗑️</div>
                <span>Xóa Tài khoản</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="danger-zone">
            <h4>⚠️ Vùng Nguy Hiểm</h4>
            <p>Hành động xóa tài khoản không thể hoàn tác. Hãy cân nhắc kỹ trước khi thực hiện.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Get users that can be deleted (exclude current user)
        options_to_delete = [u for u in users_data.keys() if u != st.session_state.get('username')]

        if not options_to_delete:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #6b7280;">
                <p>Không có tài khoản nào có thể xóa</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="form-group">', unsafe_allow_html=True)
            st.markdown('<label class="form-label">👤 Chọn tài khoản để xóa</label>', unsafe_allow_html=True)
            user_to_delete = st.selectbox(
                "Chọn tài khoản để xóa", 
                options=options_to_delete,
                key="delete_user_select",
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
    
            if user_to_delete:
                user_role = users_data[user_to_delete].get('role', 'user')
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
                    <strong>🗑️ Xác nhận xóa:</strong><br>
                    Tài khoản: <strong>{user_to_delete}</strong><br>
                    Vai trò: <strong>{user_role}</strong>
                </div>
                """, unsafe_allow_html=True)
        
                # Thêm checkbox xác nhận
                st.markdown("---")
                confirm_delete = st.checkbox(
                    f"✅ Tôi hiểu rằng việc xóa tài khoản '{user_to_delete}' không thể hoàn tác",
                    key="confirm_delete_checkbox"
                )

                # Thêm text input để xác nhận tên tài khoản
                if confirm_delete:
                    st.markdown("""
                    <div style="background: #fef3c7; border: 1px solid #f59e0b; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                        <strong>⚠️ Xác nhận cuối cùng:</strong><br>
                        Để xác nhận xóa, vui lòng nhập chính xác tên tài khoản bên dưới:
                    </div>
                    """, unsafe_allow_html=True)
            
                    confirmation_input = st.text_input(
                        f"Nhập '{user_to_delete}' để xác nhận:",
                        key="delete_confirmation_input",
                        placeholder=f"Nhập: {user_to_delete}"
                    )
            
                    # Chỉ hiển thị nút xóa khi đã xác nhận đầy đủ
                    if confirmation_input == user_to_delete:
                        st.markdown("""
                        <div style="background: #fee2e2; border: 1px solid #ef4444; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                            <strong>🚨 CẢNH BÁO:</strong> Bạn sắp xóa vĩnh viễn tài khoản này!
                        </div>
                        """, unsafe_allow_html=True)
                
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("🚫 HỦY BỎ", key="cancel_delete_btn", use_container_width=True):
                                # Reset tất cả các trạng thái xác nhận
                                st.session_state.confirm_delete_checkbox = False
                                st.session_state.delete_confirmation_input = ""
                                st.rerun()
                
                        with col2:
                            if st.button("💥 XÁC NHẬN XÓA", key="delete_user_btn", use_container_width=True, type="primary"):
                                # Thực hiện xóa
                                deleted_user = user_to_delete
                                del users_data[user_to_delete]
                                save_users(users_data)
                        
                                # Reset các trạng thái
                                st.session_state.confirm_delete_checkbox = False
                                st.session_state.delete_confirmation_input = ""
                        
                                st.markdown(f"""
                                <div class="success-message">
                                    <span class="success-icon">✅</span>
                                    <span>Đã xóa tài khoản '<strong>{deleted_user}</strong>' khỏi hệ thống</span>
                                </div>
                                """, unsafe_allow_html=True)
                        
                                # Delay một chút để hiển thị thông báo trước khi rerun
                                import time
                                time.sleep(1)
                                st.rerun()
            
                    elif confirmation_input and confirmation_input != user_to_delete:
                        st.markdown("""
                        <div style="background: #fef2f2; border: 1px solid #ef4444; padding: 0.5rem; border-radius: 6px; color: #dc2626;">
                            ❌ Tên tài khoản không khớp. Vui lòng nhập chính xác.
                        </div>
                        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
