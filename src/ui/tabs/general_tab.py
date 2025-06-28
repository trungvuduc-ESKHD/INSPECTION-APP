import streamlit as st
from src.core.utils import parse_date # Đảm bảo import từ utils
from src.ui.components.ui_helpers import create_styled_header, create_bilingual_label
from src.ui.forms.product_form import render_product_form
from src.ui.forms.container_status_form import render_container_status

def render_general_tab():
    """Render the general information tab with unique keys for all widgets."""
    create_styled_header("Thông tin chung/General Information")
    
    # Lấy ra generalInfo để code gọn hơn
    # Dùng st.session_state.get('inspection_data', {}) để phòng trường hợp chưa có
    info = st.session_state.get('inspection_data', {}).get('generalInfo', {})
    if not info:
        st.warning("Không có dữ liệu báo cáo để hiển thị.")
        return

    col1, col2 = st.columns(2)
    with col1:
        create_bilingual_label("Số tài liệu", "Document No")
        info['documentNo'] = st.text_input("Document No Input", value=info.get('documentNo', ''), key='doc_no', label_visibility="collapsed", placeholder="EHC-TP8.4-02F01")
        
        create_bilingual_label("Ngày phát hành", "Published on")
        info['publishedDate'] = st.text_input("Published Date Input", value=info.get('publishedDate', ''), key='pub_date', label_visibility="collapsed")
        
        create_bilingual_label("Nguồn gốc - Tên nhà cung cấp", "Origin - Supplier name")
        info['supplierName'] = st.text_input("Supplier Name Input", value=info.get('supplierName', ''), key='supplier_name', label_visibility="collapsed")
        
        create_bilingual_label("Số hợp đồng", "PI Contract number")
        info['contractNumber'] = st.text_input("Contract Number Input", value=info.get('contractNumber', ''), key='contract_no', label_visibility="collapsed")
        
        create_bilingual_label("Số container/ xe lạnh", "Container number")
        info['containerNumber'] = st.text_input("Container Number Input", value=info.get('containerNumber', ''), key='container_no', label_visibility="collapsed")
        
        create_bilingual_label("Bộ phận chịu trách nhiệm", "Responsible department")
        info['department'] = st.text_input("Department Input", value=info.get('department', ''), key='department', label_visibility="collapsed")
        
        create_bilingual_label("Địa điểm kiểm hàng", "Inspection location")
        info['location'] = st.text_input("Location Input", value=info.get('location', ''), key='location', label_visibility="collapsed")
    
    with col2:
        create_bilingual_label("Số phiên bản", "Version No")
        info['versionNo'] = st.text_input("Version No Input", value=info.get('versionNo', ''), key='version_no', label_visibility="collapsed", placeholder="1")
        
        create_bilingual_label("Số đơn hàng", "Order No")
        info['orderNo'] = st.text_input("Order No Input", value=info.get('orderNo', ''), key='order_no', label_visibility="collapsed")
        
        create_bilingual_label("Tên khách hàng", "Partner name")
        info['customerName'] = st.text_input("Customer Name Input", value=info.get('customerName', ''), key='customer_name', label_visibility="collapsed")
        
        create_bilingual_label("Tổng lượng kiện được nhận", "Received total quantity (carton)")
        info['receivedQuantity'] = st.text_input("Received Quantity Input", value=info.get('receivedQuantity', ''), key='received_qty', label_visibility="collapsed")
        
        create_bilingual_label("Ngày hàng đến", "ETA")
        eta_date_obj = parse_date(info.get('eta'))
        selected_eta_date = st.date_input(
            "ETA Date Input", value=eta_date_obj, key='eta_date', label_visibility="collapsed"
        )
        if selected_eta_date:
            info['eta'] = selected_eta_date.strftime('%Y-%m-%d')
        else:
            info['eta'] = None
        
        create_bilingual_label("Kiểm hàng bởi", "Inspected by")
        info['inspectedBy'] = st.text_input("Inspected By Input", value=info.get('inspectedBy', ''), key='inspected_by', label_visibility="collapsed")
        
        create_bilingual_label("Ngày kiểm hàng", "Inspection date")
        inspection_date_obj = parse_date(info.get('inspectionDate'))
        selected_inspection_date = st.date_input(
            "Inspection Date Input", value=inspection_date_obj, key='inspection_date', label_visibility="collapsed"
        )
        if selected_inspection_date:
            info['inspectionDate'] = selected_inspection_date.strftime('%Y-%m-%d')
        else:
            info['inspectionDate'] = None
    
    # Product Information
    render_product_form()
    
    # Container Status Form
    render_container_status()