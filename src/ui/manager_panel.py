import streamlit as st
import pandas as pd
from src.core.auth import get_users, save_users
from src.core.data_manager import get_all_reports_metadata, assign_report, delete_report

def render_manager_panel_page():
    """Renders the admin panel for users with the 'manager' role."""
    
    # --- KIỂM TRA QUYỀN TRUY CẬP ---
    allowed_roles = ['manager', 'super_admin']
    if st.session_state.get('role') not in allowed_roles:
        st.error("⛔ Bạn không có quyền truy cập trang này.")
        st.stop()

    # Custom CSS for Manager Panel
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .manager-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: slideInDown 0.8s ease-out;
    }
    
    .manager-header h1 {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .manager-header .subtitle {
        color: #e8f4f8;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid #e3e8ef;
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .section-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    }
    
    .section-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f0f2f6;
    }
    
    .section-icon {
        font-size: 2rem;
        margin-right: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-title {
        color: #2d3748;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.5rem;
        margin: 0;
    }
    
    .action-expander {
        margin: 1rem 0;
        border: 1px solid #e3e8ef;
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .action-expander:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        animation: bounceIn 0.6s ease-out;
    }
    
    .warning-message {
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        animation: pulse 2s infinite;
    }
    
    .danger-zone {
        background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
    
    .danger-zone h4 {
        margin: 0 0 0.5rem 0;
        font-weight: 600;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        animation: fadeInScale 0.8s ease-out;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    .custom-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .custom-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
    }
    
    .delete-button {
        background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
    
    .delete-button:hover {
        box-shadow: 0 6px 16px rgba(239, 68, 68, 0.4);
    }
    
    .floating-elements-manager {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .floating-icon {
        position: absolute;
        opacity: 0.05;
        animation: floatManager 8s ease-in-out infinite;
        font-size: 4rem;
    }
    
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes bounceIn {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            opacity: 1;
            transform: scale(1.05);
        }
        70% {
            transform: scale(0.9);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.02);
        }
    }
    
    @keyframes floatManager {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        25% { transform: translateY(-15px) rotate(90deg); }
        50% { transform: translateY(-30px) rotate(180deg); }
        75% { transform: translateY(-15px) rotate(270deg); }
    }
    
    /* Custom dataframe styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Custom selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid #e3e8ef;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    # Floating background elements
    st.markdown("""
    <div class="floating-elements-manager">
        <div class="floating-icon" style="top: 10%; left: 5%;">👥</div>
        <div class="floating-icon" style="top: 20%; right: 10%; animation-delay: -2s;">📊</div>
        <div class="floating-icon" style="top: 60%; left: 8%; animation-delay: -4s;">📋</div>
        <div class="floating-icon" style="top: 70%; right: 5%; animation-delay: -1s;">⚙️</div>
        <div class="floating-icon" style="top: 40%; right: 15%; animation-delay: -3s;">🎯</div>
    </div>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="manager-header">
        <h1>👨‍💼 Bảng điều khiển của Quản lý</h1>
        <div class="subtitle">Manager's Admin Panel - Quản lý người dùng và báo cáo</div>
    </div>
    """, unsafe_allow_html=True)

    # --- QUẢN LÝ NGƯỜI DÙNG ---
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-icon">👥</div>
            <h2 class="section-title">Quản lý Người dùng</h2>
        </div>
    """, unsafe_allow_html=True)
    
    users_data = get_users()
    manageable_users = {u: d for u, d in users_data.items() if d.get('role') in ['user', 'admin']}

    if not manageable_users:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #6b7280;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">👤</div>
            <p>Không có user hoặc admin nào để quản lý.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Stats
        user_count = len([u for u, d in manageable_users.items() if d.get('role') == 'user'])
        admin_count = len([u for u, d in manageable_users.items() if d.get('role') == 'admin'])
        
        st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{user_count}</div>
                <div class="stat-label">Người dùng</div>
            </div>
            <div class="stat-card" style="animation-delay: 0.2s;">
                <div class="stat-number">{admin_count}</div>
                <div class="stat-label">Quản trị viên</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        df_users = pd.DataFrame([{"Username": u, "Role": d.get('role')} for u, d in manageable_users.items()])
        st.dataframe(df_users, use_container_width=True)
        
        with st.expander("⚙️ Thay đổi vai trò người dùng"):
            selected_user_for_role_change = st.selectbox(
                "Chọn người dùng", 
                options=list(manageable_users.keys()),
                key="role_change_user_select"
            )
            current_role = manageable_users[selected_user_for_role_change]['role']
            role_options = ["user", "admin"]
            default_index = role_options.index(current_role) if current_role in role_options else 0
            
            new_role = st.selectbox(
                "Chọn vai trò mới", 
                options=role_options,
                index=default_index,
                key="role_change_new_role_select"
            )
            if st.button("Cập nhật vai trò", key="update_role_button"):
                users_data[selected_user_for_role_change]['role'] = new_role
                save_users(users_data)
                st.success(f"Đã cập nhật vai trò cho {selected_user_for_role_change} thành {new_role}.")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # --- QUẢN LÝ BÁO CÁO ---
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-icon">📊</div>
            <h2 class="section-title">Quản lý Báo cáo</h2>
        </div>
    """, unsafe_allow_html=True)
    
    all_reports = get_all_reports_metadata()
    if not all_reports:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #6b7280;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📋</div>
            <p>Chưa có báo cáo nào được tạo.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Report stats
        total_reports = len(all_reports)
        pending_reports = len([r for r in all_reports if r.get('status') == 'pending_review'])
        completed_reports = len([r for r in all_reports if r.get('status') == 'completed'])
        
        st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_reports}</div>
                <div class="stat-label">Tổng báo cáo</div>
            </div>
            <div class="stat-card" style="animation-delay: 0.2s;">
                <div class="stat-number">{pending_reports}</div>
                <div class="stat-label">Đang chờ</div>
            </div>
            <div class="stat-card" style="animation-delay: 0.4s;">
                <div class="stat-number">{completed_reports}</div>
                <div class="stat-label">Hoàn thành</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        df_reports = pd.DataFrame(all_reports)
        st.dataframe(df_reports[['report_name', 'status', 'created_by', 'assigned_to']])
        
        # --- CHỈ ĐỊNH BÁO CÁO ---
        with st.expander("🎯 Chỉ định báo cáo cho Admin/Xuất báo cáo"):
            if not all_reports:
                st.write("Chưa có báo cáo nào để chỉ định.")
            else:
                report_to_assign_name = st.selectbox(
                    "Chọn báo cáo để chỉ định", 
                    options=[r['report_name'] for r in all_reports],
                    key="assign_report_select"
                )
                report_to_assign_id = next(r['report_id'] for r in all_reports if r['report_name'] == report_to_assign_name)
            
                admin_list = [u for u, d in users_data.items() if d.get('role') == 'admin']
                if not admin_list:
                    st.markdown("""
                    <div class="warning-message">
                        ⚠️ Chưa có người dùng nào có vai trò 'admin' để chỉ định.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    admin_to_assign = st.selectbox("Chọn Admin", options=admin_list, key="assign_admin_select")
                    if st.button("Xác nhận chỉ định"):
                        assign_report(report_to_assign_id, admin_to_assign)
                        st.markdown(f"""
                        <div class="success-message">
                            ✅ Đã chỉ định báo cáo '{report_to_assign_name}' cho {admin_to_assign}.
                        </div>
                        """, unsafe_allow_html=True)
                        st.rerun()

        # --- XÓA BÁO CÁO ---
        with st.expander("🗑️ Xóa báo cáo"):
            st.markdown("""
            <div class="danger-zone">
                <h4>⚠️ Vùng Nguy Hiểm</h4>
                <p>Hành động này không thể hoàn tác. Vui lòng cân nhắc kỹ trước khi thực hiện.</p>
            </div>
            """, unsafe_allow_html=True)
            
            report_to_delete_name = st.selectbox(
                "Chọn báo cáo để xóa", 
                options=[r['report_name'] for r in all_reports],
                key="delete_report_select"
            )
            
            st.markdown(f"""
            <div class="warning-message">
                ⚠️ Bạn có chắc chắn muốn xóa vĩnh viễn báo cáo '{report_to_delete_name}' không?
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("XÁC NHẬN XÓA", type="primary", key="confirm_delete_button"):
                report_id = next((r['report_id'] for r in all_reports if r['report_name'] == report_to_delete_name), None)
                if report_id:
                    success, message = delete_report(report_id)
                    if success: 
                        st.markdown(f"""
                        <div class="success-message">
                            ✅ {message}
                        </div>
                        """, unsafe_allow_html=True)
                        st.rerun()
                    else: 
                        st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)