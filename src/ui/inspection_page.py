import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from copy import deepcopy

# Import các hàm cần thiết
from src.core.data_manager import (
    get_all_reports_metadata, create_new_report,
    load_report_data, save_report_data,
    update_report_status, assign_report
)
from src.core.auth import get_users
from src.core.report_generator import generate_pdf_report
from src.ui.tabs.tabs_controller import render_tabs
from src.styles.theme import load_css
from src.ui.layout.footer import render_footer

def render_inspection_page():
    st.title("Báo cáo Giám định / Inspection Report")

    current_user = st.session_state.username
    user_role = st.session_state.role
    all_reports_metadata = get_all_reports_metadata()

    st.header("1. Chọn hoặc Tạo Báo cáo")

    reports_to_show = []
    if user_role == 'manager':
        reports_to_show = all_reports_metadata
    elif user_role == 'admin':
        reports_to_show = [r for r in all_reports_metadata if r.get('assigned_to') == current_user]
    else: # user
        reports_to_show = [r for r in all_reports_metadata if r.get('created_by') == current_user]
    
    report_options = {f"{r['report_name']} ({r['status']})": r['report_id'] for r in reports_to_show}
    report_options["--- TẠO BÁO CÁO MỚI ---"] = "new_report"

    default_index = 0
    if st.session_state.current_report_id:
        try:
            current_report_name = next(name for name, id in report_options.items() if id == st.session_state.current_report_id)
            default_index = list(report_options.keys()).index(current_report_name)
        except StopIteration:
            st.session_state.current_report_id = None # Reset nếu ID không còn hợp lệ

    selected_report_name = st.selectbox(
        "Chọn một báo cáo để xem/sửa, hoặc tạo mới:",
        options=list(report_options.keys()),
        index=default_index,
        key="report_selector"
    )

    if report_options[selected_report_name] == "new_report":
        with st.form("new_report_form"):
            new_report_name_input = st.text_input("Tên báo cáo mới (ví dụ: Lô Nho Xanh 27/06)")
            submitted = st.form_submit_button("Tạo và Bắt đầu")
            if submitted and new_report_name_input:
                with st.spinner("Đang tạo báo cáo mới..."):
                    report_id = create_new_report(current_user, new_report_name_input)
                    st.session_state.current_report_id = report_id
                    st.success(f"Đã tạo báo cáo '{new_report_name_input}'.")
                    st.rerun()
        return

    # Cập nhật ID báo cáo đang chọn
    st.session_state.current_report_id = report_options[selected_report_name]
    report_id = st.session_state.current_report_id

    # Tải dữ liệu báo cáo
    report_metadata = next((r for r in all_reports_metadata if r['report_id'] == report_id), None)
    if not report_metadata: st.error("Không tìm thấy thông tin báo cáo."); st.stop()
    
    # Chỉ tải lại dữ liệu từ file khi cần thiết
    if st.session_state.get('inspection_data') is None or st.session_state.inspection_data.get('generalInfo', {}).get('report_id') != report_id:
        st.session_state.inspection_data = load_report_data(report_metadata['file_name'])
        if st.session_state.inspection_data is None:
            st.error(f"Lỗi: Không thể tải file dữ liệu '{report_metadata['file_name']}'."); st.stop()
        st.rerun()

    # ==========================================================
    # KHỐI HIỂN THỊ DUY NHẤT SAU KHI CHỌN BÁO CÁO
    # ==========================================================
    
    # --- LOGIC PHÂN QUYỀN TRUNG TÂM ---
    report_status = report_metadata.get('status', 'draft')
    is_editable = (user_role == 'manager') or \
                  (user_role == 'admin' and report_status == 'pending_review') or \
                  (user_role == 'user' and report_status == 'draft')

    # --- HIỂN THỊ THÔNG TIN VÀ GIAO DIỆN NHẬP LIỆU ---
    st.header(f"2. Nhập liệu cho Báo cáo: {report_metadata.get('report_name')}")
    status_color = "blue" if report_status == 'draft' else "orange" if report_status == 'pending_review' else "green"
    st.markdown(f"Trạng thái: :{status_color}[**{report_status.upper()}**] | Người tạo: `{report_metadata.get('created_by')}`")
    
    if not is_editable:
        st.warning("🔒 Bạn chỉ có quyền xem báo cáo này. Mọi trường nhập liệu đã bị khóa.")
    st.markdown("---")

    # Vô hiệu hóa toàn bộ giao diện nếu không được sửa
    with st.container():
        st.empty().disabled = not is_editable
        load_css()
        render_tabs()
        render_footer()
    
    # --- CÁC NÚT HÀNH ĐỘNG ---
    st.markdown("---")
    st.header("3. Hành động & Hoàn tất")
    action_cols = st.columns(3)

    with action_cols[0]:
        if st.button("Lưu thay đổi", type="primary", use_container_width=True, disabled=not is_editable):
            save_report_data(report_metadata['file_name'], st.session_state.inspection_data)
            st.success("Đã lưu báo cáo thành công!")
            st.toast("Đã lưu!")

    with action_cols[1]:
        can_export = (user_role == 'manager') or (report_status == 'approved')
        if can_export:
            pdf_bytes = generate_pdf_report(st.session_state.inspection_data)
            if pdf_bytes:
                st.download_button(
                    label="Xuất Báo cáo PDF", data=pdf_bytes,
                    file_name=f"Report_{report_metadata.get('report_name', report_id)}.pdf",
                    mime="application/pdf", use_container_width=True
                )
        else:
            st.button("Xuất Báo cáo PDF", use_container_width=True, disabled=True, help="Báo cáo phải được 'approved' để có thể xuất.")

    with action_cols[2]:
        if is_editable:
            new_status = report_status
            if user_role == 'user' and report_status == 'draft':
                if st.button("Gửi đi để duyệt", use_container_width=True): new_status = 'pending_review'
            elif user_role == 'admin' and report_status == 'pending_review':
                if st.button("Phê duyệt báo cáo", use_container_width=True): new_status = 'approved'
            elif user_role == 'manager':
                status_options = ["draft", "pending_review", "approved"]
                new_status = st.selectbox("Đổi trạng thái:", status_options, index=status_options.index(report_status))

            if new_status != report_status:
                update_report_status(report_id, new_status)
                st.success(f"Đã cập nhật trạng thái thành '{new_status}'.")
                st.rerun()