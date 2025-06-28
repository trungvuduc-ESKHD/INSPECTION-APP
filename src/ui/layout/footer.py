import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
# Không cần import data_manager và report_generator ở đây nữa

def render_footer():
    """Render the footer with comments and signatures section."""
    st.markdown("---")
    st.markdown('<div class="eurofins-blue"><h3>Nhận xét chung/Comments & Signatures</h3></div>', unsafe_allow_html=True)
    
    # --- Ô NHẬP NHẬN XÉT ---
    # Ô này sẽ cập nhật giá trị trong st.session_state.inspection_data
    # Dữ liệu sẽ được lưu khi người dùng nhấn nút "Lưu thay đổi" trên trang giám định
    st.session_state.inspection_data['comments'] = st.text_area(
        "Nhận xét / Comments",
        value=st.session_state.inspection_data.get('comments', ''),
        key='comments_input'
    )
    st.markdown("---")

    # --- KHUNG VẼ CHỮ KÝ ---
    col1, col2 = st.columns(2)

    # Chữ ký cho Người Giám định (Inspector)
    with col1:
        st.markdown('<div class="bilingual-label">Chữ ký Người giám định / Inspector Signature</div>', unsafe_allow_html=True)
        st.session_state.inspection_data['inspectorName'] = st.text_input(
            "Tên người giám định / Inspector Name",
            value=st.session_state.inspection_data.get('inspectorName', ''),
            key='inspector_name_input'
        )
        canvas_inspector = st_canvas(
            stroke_width=2, stroke_color="#000000", background_color="#FFFFFF",
            height=150, width=400, drawing_mode="freedraw",
            key="canvas_inspector"
        )
        if canvas_inspector.image_data is not None and np.any(canvas_inspector.image_data):
            st.session_state.inspection_data['inspector_signature'] = canvas_inspector.image_data

    # Chữ ký cho Người Duyệt (Reviewer)
    with col2:
        st.markdown('<div class="bilingual-label">Chữ ký Người duyệt / Reviewer Signature</div>', unsafe_allow_html=True)
        st.session_state.inspection_data['reviewerName'] = st.text_input(
            "Tên người duyệt / Reviewer Name",
            value=st.session_state.inspection_data.get('reviewerName', ''),
            key='reviewer_name_input'
        )
        canvas_reviewer = st_canvas(
            stroke_width=2, stroke_color="#000000", background_color="#FFFFFF",
            height=150, width=400, drawing_mode="freedraw",
            key="canvas_reviewer"
        )
        if canvas_reviewer.image_data is not None and np.any(canvas_reviewer.image_data):
            st.session_state.inspection_data['reviewer_signature'] = canvas_reviewer.image_data