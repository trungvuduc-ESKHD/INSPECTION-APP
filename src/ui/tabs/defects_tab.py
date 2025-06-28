# src/ui/tabs/defects_tab.py (UPDATED WITH AUTO-CALCULATION)

import streamlit as st
from copy import deepcopy
from src.core.default_data import get_fixed_defects_structure
def render_defects_tab():
    if not st.session_state.inspection_data['products']:
        st.warning("Vui lòng thêm sản phẩm ở tab 'Thông tin/General' trước.")
        return

    st.header("Đánh giá các lỗi trên sản phẩm/Defects Assessment")

    product_names = [p['name'] for p in st.session_state.inspection_data['products']]
    selected_product_index = st.selectbox("Chọn sản phẩm", range(len(product_names)), format_func=lambda i: product_names[i])
    selected_product = st.session_state.inspection_data['products'][selected_product_index]
    product_id = str(selected_product['id'])

    if product_id not in st.session_state.inspection_data['detailedDefectAssessment']:
        # Gọi hàm để lấy cấu trúc thay vì truy cập session_state
        st.session_state.inspection_data['detailedDefectAssessment'][product_id] = deepcopy(get_fixed_defects_structure())
    if product_id not in st.session_state.inspection_data['defectAssessment']:
        st.session_state.inspection_data['defectAssessment'][product_id] = {}

    product_defects_data = st.session_state.inspection_data['detailedDefectAssessment'][product_id]
    product_summary_data = st.session_state.inspection_data['defectAssessment'][product_id]

    
    # --- Biến để lưu tổng % của mỗi loại lỗi ---
    summary_percentages = {
        'seriousDefectsPercentage': 0.0,
        'majorDefectsPercentage': 0.0,
        'minorDefectsPercentage': 0.0,
        'shatteringBerriesPercentage': 0.0,
    }

    st.markdown(f"### Sản phẩm / Product: {selected_product['name']} ({selected_product['size']})")
    
    # --- LẤY TỔNG KHỐI LƯỢNG MẪU TỰ ĐỘNG TỪ TAB WEIGHT ---
    total_sample_weight_str = product_summary_data.get('totalSampleWeight', '0')
    
    # Hiển thị cho người dùng biết
    st.info(f"Tổng khối lượng mẫu kiểm (lấy từ tab Khối lượng): **{total_sample_weight_str} Kg**")
    st.markdown("---")

    try:
        total_sample_weight = float(total_sample_weight_str) if total_sample_weight_str else 0
    except (ValueError, TypeError):
        total_sample_weight = 0

    if total_sample_weight <= 0:
        st.warning("Vui lòng qua tab 'Khối lượng' và nhấn 'Tính toán & Tổng hợp' để có tổng khối lượng mẫu.")

    def defect_entry_section(title, defect_key, summary_percent_key):
        st.subheader(title)
        for i, defect in enumerate(product_defects_data[defect_key]):
            st.markdown(f"**{defect['defectType']}**")
            with st.expander("Xem mô tả"):
                st.markdown(f"_{defect['description']}_")
            
            cols = st.columns(2)
            with cols[0]:
                new_weight = st.text_input(
                    "Khối lượng (Kg)", value=defect.get('weight', ''),
                    key=f"w_{product_id}_{defect_key}_{i}", label_visibility="collapsed"
                )
                defect['weight'] = new_weight
            with cols[1]:
                try:
                    percentage_val = (float(new_weight or 0) / total_sample_weight * 100) if total_sample_weight > 0 else 0
                    defect['percentage'] = f"{percentage_val:.4f}"
                    # Cộng dồn vào tổng
                    summary_percentages[summary_percent_key] += percentage_val
                except ValueError:
                    defect['percentage'] = "Lỗi"
                
                st.text_input(
                    "Phần trăm (%)", value=defect.get('percentage', ''),
                    key=f"p_{product_id}_{defect_key}_{i}", disabled=True, label_visibility="collapsed"
                )
            st.markdown("---")
            
    # --- Gọi hàm và truyền key của dictionary tổng hợp ---
    defect_entry_section("Các lỗi nghiêm trọng / Serious defects", "seriousDefects", 'seriousDefectsPercentage')
    defect_entry_section("Các lỗi lớn / Major defects", "majorDefects", 'majorDefectsPercentage')
    defect_entry_section("Các lỗi nhẹ / Minor defects", "minorDefects", 'minorDefectsPercentage')
    defect_entry_section("Quả bị rụng / Shattering (Loosing) berries", "shatteringBerries", 'shatteringBerriesPercentage')

    # --- TỰ ĐỘNG CẬP NHẬT DỮ LIỆU TÓM TẮT ---
    # Sau khi vòng lặp chạy xong, `summary_percentages` đã có đủ dữ liệu
    product_summary_data['seriousDefectsPercentage'] = f"{summary_percentages['seriousDefectsPercentage']:.4f}"
    product_summary_data['majorDefectsPercentage'] = f"{summary_percentages['majorDefectsPercentage']:.4f}"
    product_summary_data['minorDefectsPercentage'] = f"{summary_percentages['minorDefectsPercentage']:.4f}"
    product_summary_data['shatteringBerriesPercentage'] = f"{summary_percentages['shatteringBerriesPercentage']:.4f}"

    # Không cần nút "Tổng hợp" nữa
    st.success("Dữ liệu tóm tắt lỗi đã được tự động cập nhật sang tab 'Chất lượng'.")