import streamlit as st
import pandas as pd
from src.ui.components.ui_helpers import create_styled_header, create_bilingual_label

def render_quality_tab():
    """Render the quality inspection tab"""
    if not st.session_state.inspection_data['products']:
        st.warning("Vui lòng thêm sản phẩm trước / Please add products first")
    else:
        create_styled_header("Tổng hợp giám định chất lượng/Quality Inspection Recap")
        
        # 1. Product specifications
        st.subheader("1. Những đặc điểm kỹ thuật của sản phẩm/Product specifications")
        
        quality_data = []
        for product in st.session_state.inspection_data['products']:
            quality_data.append([
                product['id'],
                product['name'],
                product['size'],
                product.get('varietyCharacteristics', ''),
                product.get('juicyLevel', ''),
                product.get('brixDegree', ''),
                product.get('firmness', '')
            ])
        
        quality_df = pd.DataFrame(
            quality_data,
            columns=["ID", "Tên sản phẩm/Product name", "Kích cỡ/Size", "Đặc điểm của giống trái/Variety characteristics", "Mọng nước/Juicy", "Độ Brix/Brix degree", "Độ cứng/Average Firmness"]
        )
        
        for i, row in quality_df.iterrows():
            product_id = row['ID']
            st.markdown(f"#### Sản phẩm / Product: {row['Tên sản phẩm/Product name']}")
            
            col1, col2 = st.columns(2)
            with col1:
                create_bilingual_label("Đặc điểm của giống trái", "Variety characteristics")
                variety_characteristics = st.text_input(
                    "Variety characteristics", 
                    value=row['Đặc điểm của giống trái/Variety characteristics'],
                    key=f"variety_{product_id}",
                    label_visibility="collapsed"
                )
                
                create_bilingual_label("Độ Brix", "Brix degree")
                brix_degree = st.text_input(
                    "Brix degree", 
                    value=row['Độ Brix/Brix degree'],
                    key=f"brix_{product_id}",
                    label_visibility="collapsed"
                )
            
            with col2:
                create_bilingual_label("Mọng nước", "Juicy")
                juicy_level = st.text_input(
                    "Juicy", 
                    value=row['Mọng nước/Juicy'],
                    key=f"juicy_{product_id}",
                    label_visibility="collapsed"
                )
                
                create_bilingual_label("Độ cứng", "Average Firmness")
                firmness = st.text_input(
                    "Firmness", 
                    value=row['Độ cứng/Average Firmness'],
                    key=f"firmness_{product_id}",
                    label_visibility="collapsed"
                )
            
            # Update the product quality info in the state
            for product in st.session_state.inspection_data['products']:
                if product['id'] == product_id:
                    product['varietyCharacteristics'] = variety_characteristics
                    product['juicyLevel'] = juicy_level
                    product['brixDegree'] = brix_degree
                    product['firmness'] = firmness
            
            st.markdown("---")
        
        # Quality comments
        create_bilingual_label("Bình luận thêm nếu \"không được chấp nhận\" hay \"treo\"", "Comments (if Rejected or Pending)")
        st.session_state.inspection_data['qualityComments'] = st.text_area(
            "Quality Comments", 
            value=st.session_state.inspection_data.get('qualityComments', ''),
            label_visibility="collapsed",
            height=100
        )
        
        # 2. Tổng hợp thông tin về kiểm tra khối lượng tịnh/Net weight checking recap
        st.subheader("2. Tổng hợp thông tin về kiểm tra khối lượng tịnh/Net weight checking recap")
        
        weight_data_recap = []
        for product in st.session_state.inspection_data['products']:
            product_id = str(product['id'])
            weight_sampling = st.session_state.inspection_data['weightSampling'].get(product_id, {})
            
            # --- LOGIC MỚI: TỰ ĐỘNG QUYẾT ĐỊNH STATUS ---
            status = 'N/A'
            try:
                avg_weight = float(weight_sampling.get('averageWeight', 0))
                target_weight = float(weight_sampling.get('targetWeight', 0))
                if avg_weight > 0 and target_weight > 0:
                    status = "C" if avg_weight >= target_weight else "NC"
            except (ValueError, TypeError):
                status = "Lỗi"
            # Cập nhật lại status vào session state
            product['weightStatus'] = status
            # ---------------------------------------------
            
            weight_data_recap.append([
                product['name'],
                product['size'],
                weight_sampling.get('averageWeight', ''),
                weight_sampling.get('targetWeight', ''),
                status # Sử dụng status vừa được quyết định
            ])
        
        recap_df = pd.DataFrame(
            weight_data_recap,
            columns=["Tên sản phẩm/Product name", "Kích cỡ/Size", "KL tịnh TB (kg)", "Mục tiêu (Kg)", "Status"]
        )
        st.table(recap_df)
        
        # 3. Defects assessment recap
        st.subheader("3. Tổng hợp thông tin về đánh giá các lỗi/Defects assessment recap")
        
        defect_data = []
        for product in st.session_state.inspection_data['products']:
            product_id = product['id']
            defect_assessment = st.session_state.inspection_data['defectAssessment'].get(str(product_id), {})
            defect_data.append([
                product_id,
                product['name'],
                product['size'],
                defect_assessment.get('seriousDefectsPercentage', '0'),
                defect_assessment.get('majorDefectsPercentage', '0'),
                defect_assessment.get('minorDefectsPercentage', '0'),
                defect_assessment.get('shatteringBerriesPercentage', '0')
            ])
        
        defect_df = pd.DataFrame(
            defect_data,
            columns=["ID", "Tên sản phẩm/Product name", "Kích cỡ/Size", 
                    "Tổng Lỗi nghiêm trọng/Total Serious Defects (%)",
                    "Tổng Lỗi lớn/Total Major Defects (%)",
                    "Tổng Lỗi nhẹ/Total Minor Defects (%)",
                    "Tổng Quả Bị Rụng/Total Shattering Berries (%)"]
        )
        
        st.table(defect_df[["Tên sản phẩm/Product name", "Kích cỡ/Size", 
                           "Tổng Lỗi nghiêm trọng/Total Serious Defects (%)",
                           "Tổng Lỗi lớn/Total Major Defects (%)",
                           "Tổng Lỗi nhẹ/Total Minor Defects (%)",
                           "Tổng Quả Bị Rụng/Total Shattering Berries (%)"]])
