import streamlit as st
import pandas as pd
from src.core.supabase_client import supabase, get_users, save_users
from src.core.data_manager import get_all_reports_metadata, assign_report, delete_report

def render_manager_panel_page():
    """Renders the admin panel for users with the 'manager' role."""
    
    # --- KIỂM TRA QUYỀN TRUY CẬP ---
    allowed_roles = ['manager', 'super_admin']
    if st.session_state.get('role') not in allowed_roles:
        st.error("⛔ Bạn không có quyền truy cập trang này.")
        st.stop()

    # Modern CSS styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="%23ffffff" fill-opacity="0.05"><circle cx="30" cy="30" r="4"/></g></svg>');
        pointer-events: none;
    }
    
    .main-header h1 {
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-header .subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .content-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .section-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .section-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .section-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.15);
    }
    
    .section-header {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.1);
    }
    
    .section-icon {
        font-size: 2.5rem;
        margin-right: 1rem;
        padding: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    
    .section-title {
        color: #2d3748;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.8rem;
        margin: 0;
    }
    
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        transition: all 0.5s ease;
        transform: scale(0);
    }
    
    .stat-card:hover::before {
        transform: scale(1);
    }
    
    .stat-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.4);
    }
    
    .stat-number {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    .data-table {
        background: white;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        margin: 1.5rem 0;
    }
    
    .action-section {
        background: rgba(255, 255, 255, 0.6);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
        backdrop-filter: blur(5px);
    }
    
    .action-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        color: #2d3748;
        font-weight: 600;
    }
    
    .action-header .icon {
        margin-right: 0.5rem;
        font-size: 1.2rem;
    }
    
    .success-alert {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
        display: flex;
        align-items: center;
    }
    
    .warning-alert {
        background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3);
        display: flex;
        align-items: center;
    }
    
    .danger-alert {
        background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.3);
    }
    
    .alert-icon {
        margin-right: 0.75rem;
        font-size: 1.25rem;
    }
    
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: #6b7280;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 16px;
        margin: 2rem 0;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        opacity: 0.5;
    }
    
    .empty-state-text {
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Custom selectbox styling */
    .stSelectbox > div > div {
        border-radius: 12px !important;
        border: 2px solid rgba(102, 126, 234, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(102, 126, 234, 0.05) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(102, 126, 234, 0.1) !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.8) !important;
        border-radius: 0 0 12px 12px !important;
        border: 1px solid rgba(102, 126, 234, 0.1) !important;
        border-top: none !important;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """, unsafe_allow_html=True)

    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>👨‍💼 Bảng điều khiển Quản lý</h1>
        <div class="subtitle">Manager's Control Panel - Quản lý người dùng và báo cáo hiệu quả</div>
    </div>
    """, unsafe_allow_html=True)

    # Content Grid
    st.markdown('<div class="content-grid">', unsafe_allow_html=True)

    # === QUẢN LÝ NGƯỜI DÙNG ===
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <div class="section-icon">👥</div>
            <h2 class="section-title">Quản lý Người dùng</h2>
        </div>
    """, unsafe_allow_html=True)
    
    users_data = get_users()
    manageable_users = {user['username']: user for user in users_data if user.get('role') in ['user', 'admin']}

    if not manageable_users:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">👤</div>
            <p class="empty-state-text">Không có người dùng nào để quản lý</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # User Statistics
        user_count = len([u for u, d in manageable_users.items() if d.get('role') == 'user'])
        admin_count = len([u for u, d in manageable_users.items() if d.get('role') == 'admin'])
        
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-number">{user_count}</div>
                <div class="stat-label">👤 Người dùng</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{admin_count}</div>
                <div class="stat-label">⚡ Quản trị viên</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(manageable_users)}</div>
                <div class="stat-label">📊 Tổng cộng</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Users Table
        df_users = pd.DataFrame([{"Username": u, "Role": d.get('role')} for u, d in manageable_users.items()])
        st.markdown('<div class="data-table">', unsafe_allow_html=True)
        st.dataframe(df_users, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Role Management
        with st.expander("⚙️ Thay đổi vai trò người dùng"):
            st.markdown("""
            <div class="action-header">
                <span class="icon">🔄</span>
                <span>Cập nhật quyền truy cập</span>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                selected_user_for_role_change = st.selectbox(
                    "👤 Chọn người dùng", 
                    options=list(manageable_users.keys()),
                    key="role_change_user_select"
                )
            
            with col2:
                current_role = manageable_users[selected_user_for_role_change]['role']
                role_options = ["user", "admin"]
                default_index = role_options.index(current_role) if current_role in role_options else 0
                
                new_role = st.selectbox(
                    "🎯 Vai trò mới", 
                    options=role_options,
                    index=default_index,
                    key="role_change_new_role_select"
                )
            
            if current_role != new_role:
                st.markdown(f"""
                <div class="warning-alert">
                    <span class="alert-icon">⚠️</span>
                    <span>Thay đổi vai trò từ <strong>{current_role}</strong> thành <strong>{new_role}</strong></span>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("🔄 Cập nhật vai trò", key="update_role_button", use_container_width=True):
                users_data[selected_user_for_role_change]['role'] = new_role
                save_users(users_data)
                st.markdown(f"""
                <div class="success-alert">
                    <span class="alert-icon">✅</span>
                    <span>Đã cập nhật vai trò cho <strong>{selected_user_for_role_change}</strong> thành <strong>{new_role}</strong></span>
                </div>
                """, unsafe_allow_html=True)
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # === QUẢN LÝ BÁO CÁO ===
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
        <div class="empty-state">
            <div class="empty-state-icon">📋</div>
            <p class="empty-state-text">Chưa có báo cáo nào được tạo</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Report Statistics
        total_reports = len(all_reports)
        pending_reports = len([r for r in all_reports if r.get('status') == 'pending_review'])
        completed_reports = len([r for r in all_reports if r.get('status') == 'completed'])
        in_progress_reports = total_reports - pending_reports - completed_reports
        
        st.markdown(f"""
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-number">{total_reports}</div>
                <div class="stat-label">📈 Tổng báo cáo</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{completed_reports}</div>
                <div class="stat-label">✅ Hoàn thành</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{in_progress_reports}</div>
                <div class="stat-label">🔄 Đang xử lý</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Reports Table
        df_reports = pd.DataFrame(all_reports)
        columns_to_show = ['report_name', 'status', 'created_by', 'assigned_to']
        available_columns = [col for col in columns_to_show if col in df_reports.columns]
        
        st.markdown('<div class="data-table">', unsafe_allow_html=True)
        st.dataframe(df_reports[available_columns], use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Report Assignment
        with st.expander("🎯 Chỉ định báo cáo cho Admin"):
            st.markdown("""
            <div class="action-header">
                <span class="icon">📤</span>
                <span>Phân công công việc</span>
            </div>
            """, unsafe_allow_html=True)
            
            admin_list = [u for u, d in users_data.items() if d.get('role') == 'admin']
            
            if not admin_list:
                st.markdown("""
                <div class="warning-alert">
                    <span class="alert-icon">⚠️</span>
                    <span>Chưa có người dùng nào có vai trò 'admin' để chỉ định</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                col1, col2 = st.columns(2)
                
                with col1:
                    report_to_assign_name = st.selectbox(
                        "📋 Chọn báo cáo", 
                        options=[r['report_name'] for r in all_reports],
                        key="assign_report_select"
                    )
                
                with col2:
                    admin_to_assign = st.selectbox(
                        "👨‍💼 Chọn Admin", 
                        options=admin_list, 
                        key="assign_admin_select"
                    )
                
                if st.button("🎯 Xác nhận chỉ định", key="assign_button", use_container_width=True):
                    report_to_assign_id = next(r['report_id'] for r in all_reports if r['report_name'] == report_to_assign_name)
                    assign_report(report_to_assign_id, admin_to_assign)
                    st.markdown(f"""
                    <div class="success-alert">
                        <span class="alert-icon">✅</span>
                        <span>Đã chỉ định báo cáo '<strong>{report_to_assign_name}</strong>' cho <strong>{admin_to_assign}</strong></span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.rerun()

        # Report Deletion
        with st.expander("🗑️ Xóa báo cáo"):
            st.markdown("""
            <div class="danger-alert">
                <h4 style="margin: 0 0 0.5rem 0; display: flex; align-items: center;">
                    <span style="margin-right: 0.5rem;">⚠️</span>
                    Vùng Nguy Hiểm
                </h4>
                <p style="margin: 0; opacity: 0.9;">
                    Hành động này không thể hoàn tác. Vui lòng cân nhắc kỹ trước khi thực hiện.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            report_to_delete_name = st.selectbox(
                "🗑️ Chọn báo cáo để xóa", 
                options=[r['report_name'] for r in all_reports],
                key="delete_report_select"
            )
            
            st.markdown(f"""
            <div class="warning-alert">
                <span class="alert-icon">⚠️</span>
                <span>Bạn có chắc chắn muốn xóa vĩnh viễn báo cáo '<strong>{report_to_delete_name}</strong>' không?</span>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("💥 XÁC NHẬN XÓA", key="confirm_delete_button", use_container_width=True):
                report_id = next((r['report_id'] for r in all_reports if r['report_name'] == report_to_delete_name), None)
                if report_id:
                    success, message = delete_report(report_id)
                    if success: 
                        st.markdown(f"""
                        <div class="success-alert">
                            <span class="alert-icon">✅</span>
                            <span>{message}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.rerun()
                    else: 
                        st.error(message)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)  # Close content-grid
