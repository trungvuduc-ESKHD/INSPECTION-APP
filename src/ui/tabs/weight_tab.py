import streamlit as st
import pandas as pd
from src.ui.components.ui_helpers import create_styled_header, create_bilingual_label

def render_weight_tab():
    if not st.session_state.inspection_data['products']:
        st.warning("Vui lòng thêm sản phẩm trước / Please add products first")
        return

    create_styled_header("Kế hoạch lấy mẫu & kiểm tra khối lượng/Sampling Plan & Weight Checking")
    
    product_names = [p['name'] for p in st.session_state.inspection_data['products']]
    selected_product_index = st.selectbox(
        "Chọn sản phẩm / Select product",
        range(len(product_names)),
        format_func=lambda i: product_names[i]
    )
    
    selected_product = st.session_state.inspection_data['products'][selected_product_index]
    product_id = selected_product['id']
    
    # Khởi tạo dữ liệu cân nặng nếu chưa có
    if str(product_id) not in st.session_state.inspection_data['weightSampling']:
        st.session_state.inspection_data['weightSampling'][str(product_id)] = {
            "bags": "", "samplingPlan": "",
            "emptyBagWeights": ["", "", ""], "emptyBagWeightAverage": "",
            "averageWeight": "",
            # Lấy target từ thông tin sản phẩm
            "targetWeight": selected_product.get('netWeight', ''),
            "totalGrossWeight": "0.000", "totalNetWeight": "0.000",
            "samples": [{"id": i+1, "grossWeight": "", "netWeight": ""} for i in range(40)]
        }
    
    weight_sampling = st.session_state.inspection_data['weightSampling'][str(product_id)]

    # --- TỰ ĐỘNG CẬP NHẬT TARGET KHI CHỌN SẢN PHẨM KHÁC ---
    weight_sampling['targetWeight'] = selected_product.get('netWeight', '')

    st.markdown(f"### Sản phẩm / Product: {selected_product['name']} ({selected_product['size']})")
    
    # --- Dòng 1: Số bao và Kế hoạch lấy mẫu ---
    col1, col2 = st.columns(2)
    with col1:
        create_bilingual_label("Số bao", "Qty of bags")
        weight_sampling['bags'] = st.text_input("Bags", value=weight_sampling.get('bags', ''), key=f"bags_{product_id}", label_visibility="collapsed")
    with col2:
        create_bilingual_label("Kế hoạch lấy mẫu", "Sampling plan")
        weight_sampling['samplingPlan'] = st.text_input("Sampling Plan", value=weight_sampling.get('samplingPlan', ''), key=f"sampling_plan_{product_id}", label_visibility="collapsed", placeholder="túi/bags")
    
    st.markdown("---")

    # --- Dòng 2: Khối lượng túi rỗng ---
    create_bilingual_label("Khối lượng của túi rỗng (Kg)", "Empty weight of bag (Kg)")
    cols = st.columns(4)
    with cols[0]:
        weight_sampling['emptyBagWeights'][0] = st.text_input("Túi 1/Bag 1", value=weight_sampling['emptyBagWeights'][0], key=f"ew_1_{product_id}")
    with cols[1]:
        weight_sampling['emptyBagWeights'][1] = st.text_input("Túi 2/Bag 2", value=weight_sampling['emptyBagWeights'][1], key=f"ew_2_{product_id}")
    with cols[2]:
        weight_sampling['emptyBagWeights'][2] = st.text_input("Túi 3/Bag 3", value=weight_sampling['emptyBagWeights'][2], key=f"ew_3_{product_id}")
    
    try:
        weights = [float(w) for w in weight_sampling['emptyBagWeights'] if w]
        if weights:
            avg = sum(weights) / len(weights)
            weight_sampling['emptyBagWeightAverage'] = f"{avg:.3f}"
        else:
            weight_sampling['emptyBagWeightAverage'] = ""
    except (ValueError, TypeError):
        weight_sampling['emptyBagWeightAverage'] = "Lỗi"

    with cols[3]:
        st.text_input("Trung bình/Average", value=weight_sampling['emptyBagWeightAverage'], key=f"ew_avg_{product_id}", disabled=True)
    st.markdown("---")

    # --- Dòng 3: Trung bình (của mẫu) và Target ---
    col1, col2 = st.columns(2)
    with col1:
        create_bilingual_label("Trung bình / Average", "Average of net weight (Kg)")
        # Ô này sẽ được điền tự động sau khi nhấn nút "Tính toán"
        st.text_input(
            "Average Weight Display", 
            value=weight_sampling.get('averageWeight', ''),
            key=f"avg_weight_display_{product_id}",
            label_visibility="collapsed",
            disabled=True
        )
    with col1:
        create_bilingual_label("Mục tiêu / Target", "Target (Kg)")
        weight_sampling['targetWeight'] = st.text_input(
            "Target Weight", 
            value=weight_sampling.get('targetWeight', ''),
            key=f"target_weight_{product_id}",
            label_visibility="collapsed",
            placeholder="Kgs"
        )
    st.markdown("---")

    # --- Bảng nhập liệu Gross Weight ---
    st.markdown("##### Khối lượng tổng cộng của mỗi túi có tính bao bì (Kg)/ Gross weight per bag (Kg)")
    for row_idx in range(4):
        cols = st.columns(10)
        start_id = row_idx * 10 + 1
        st.markdown(f"**{start_id}-{start_id + 9}**")
        for col_idx, col in enumerate(cols):
            sample_id = start_id + col_idx
            sample = next((s for s in weight_sampling['samples'] if s['id'] == sample_id), None)
            if sample:
                gross_weight = col.text_input(
                    f"Sample {sample_id}", value=sample['grossWeight'],
                    key=f"gross_weight_{product_id}_{sample_id}", label_visibility="collapsed", placeholder=f"{sample_id}"
                )
                sample['grossWeight'] = gross_weight
                try:
                    empty_weight = float(weight_sampling['emptyBagWeightAverage'] or 0)
                    gross = float(gross_weight or 0)
                    sample['netWeight'] = f"{(gross - empty_weight):.3f}" if gross > 0 else ""
                except (ValueError, TypeError):
                    sample['netWeight'] = ""
    st.markdown("---")

    # --- Hiển thị Target (tự động điền, không cho sửa) ---
    create_bilingual_label("Mục tiêu / Target", "Target (Kg)")
    st.text_input(
        "Target Weight Display", 
        value=weight_sampling.get('targetWeight', ''),
        key=f"target_weight_display_{product_id}",
        label_visibility="collapsed",
        disabled=True,
        help="Giá trị này được lấy tự động từ 'Trọng lượng tịnh' của sản phẩm."
    )
    st.markdown("---")
    
    # --- Bảng hiển thị Net Weight (tự động tính) ---
    st.markdown("##### Khối lượng tổng cộng của mỗi túi có trừ bao bì (Kg)/ Net weight per bag (Kg)")
    for row_idx in range(4):
        cols = st.columns(10)
        start_id = row_idx * 10 + 1
        st.markdown(f"**{start_id}-{start_id + 9}**")
        for col_idx, col in enumerate(cols):
            sample_id = start_id + col_idx
            sample = next((s for s in weight_sampling['samples'] if s['id'] == sample_id), None)
            if sample:
                col.text_input(
                    f"Net Sample {sample_id}", value=sample['netWeight'],
                    key=f"net_weight_{product_id}_{sample_id}", label_visibility="collapsed", placeholder=f"{sample_id}", disabled=True
                )
    st.markdown("---")

    # --- Nút Tính toán và hiển thị tổng hợp ---
    if st.button("Tính toán & Tổng hợp / Calculate & Summarize", key=f"calculate_{product_id}"):
        valid_gross_samples = [float(s['grossWeight']) for s in weight_sampling['samples'] if s.get('grossWeight')]
        valid_net_samples = [float(s['netWeight']) for s in weight_sampling['samples'] if s.get('netWeight')]
        
        weight_sampling['totalGrossWeight'] = f"{sum(valid_gross_samples):.3f}"
        weight_sampling['totalNetWeight'] = f"{sum(valid_net_samples):.3f}"
        
        if valid_net_samples:
            weight_sampling['averageWeight'] = f"{sum(valid_net_samples) / len(valid_net_samples):.3f}"
        else:
            weight_sampling['averageWeight'] = "0.000"
        
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tổng khối lượng có bì / Total gross weight (Kgs)", weight_sampling['totalGrossWeight'])
    with col2:
        st.metric("Tổng khối lượng trừ bì / Total net weight (Kgs)", weight_sampling['totalNetWeight'])
        # --- CẬP NHẬT TỔNG KHỐI LƯỢNG MẪU CHO TAB LỖI ---
        # Đây là cầu nối dữ liệu quan trọng
        if product_id in st.session_state.inspection_data['defectAssessment']:
            st.session_state.inspection_data['defectAssessment'][product_id]['totalSampleWeight'] = weight_sampling.get('totalNetWeight', '0')