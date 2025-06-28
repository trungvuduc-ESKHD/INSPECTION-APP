
import streamlit as st
import pandas as pd
from src.core.utils import generate_id
from src.ui.components.ui_helpers import create_styled_header, create_bilingual_label
# --- DÒNG MỚI: Import hàm lưu dữ liệu ---
from src.core.data_manager import save_report_data

def render_product_form():
    """Render the product information form with add & save functionality."""
    create_styled_header("Thông tin sản phẩm/Product Information")
    
    # Lấy dữ liệu từ session state
    inspection_data = st.session_state.inspection_data
    products_list = inspection_data.get('products', [])

    # Hiển thị bảng sản phẩm hiện có
    if products_list:
        products_df = pd.DataFrame(products_list)
        # Chỉ hiển thị các cột cần thiết
        display_columns = {
            'name': "Tên sản phẩm/Product name",
            'size': "Kích cỡ/Size",
            'receivedQuantity': "Số lượng nhận/Received Qty",
            'netWeight': "Trọng lượng tịnh/Net Weight"
        }
        # Lọc các cột có trong DataFrame để tránh lỗi
        cols_to_show = [col for col in display_columns.keys() if col in products_df.columns]
        products_df_display = products_df[cols_to_show].rename(columns=display_columns)
        st.table(products_df_display)
    
    # --- Form để thêm sản phẩm mới ---
    with st.expander("Thêm sản phẩm mới / Add new product", expanded=True):
        with st.form(key="new_product_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                create_bilingual_label("Tên sản phẩm", "Product name")
                product_name = st.text_input("Product Name", label_visibility="collapsed", placeholder="Nhập tên sản phẩm")
                
                create_bilingual_label("Số lượng nhận", "Received quantity")
                received_quantity = st.text_input("Received Quantity", label_visibility="collapsed", placeholder="cartons")
            
            with col2:
                create_bilingual_label("Kích cỡ", "Size")
                product_size = st.text_input("Product Size", label_visibility="collapsed", placeholder="Nhập kích cỡ")
                
                create_bilingual_label("Trọng lượng tịnh", "Net weight")
                net_weight = st.text_input("Net Weight", label_visibility="collapsed", placeholder="kg")

            # Nút "Thêm sản phẩm" nằm trong form
            submitted = st.form_submit_button("Thêm sản phẩm / Add Product")

            if submitted:
                if not product_name or not product_size:
                    st.error("Vui lòng nhập Tên sản phẩm và Kích cỡ.")
                else:
                    new_product = {
                        'id': generate_id(),
                        'name': product_name,
                        'size': product_size,
                        'receivedQuantity': received_quantity,
                        'netWeight': net_weight
                    }
                    # 1. Thêm vào session state
                    st.session_state.inspection_data['products'].append(new_product)
                    
                    # 2. Lấy tên file báo cáo hiện tại
                    report_id = st.session_state.get('current_report_id')
                    # Cần có logic để lấy file_name từ report_id, nên chúng ta sẽ lấy nó từ generalInfo
                    file_name = f"{report_id}.json"

                    # 3. Lưu lại toàn bộ dữ liệu vào file JSON
                    save_report_data(file_name, st.session_state.inspection_data)
                    
                    st.success(f"Đã thêm và lưu sản phẩm: {product_name}")
                    # Không cần st.rerun() vì st.form_submit_button đã tự làm điều đó