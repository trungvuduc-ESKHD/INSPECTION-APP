import streamlit as st
from PIL import Image
from io import BytesIO
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import zipfile
import datetime

# ===================================================================
# HÀM TẠO BÁO CÁO WORD CHO MỘT SẢN PHẨM DUY NHẤT
# ===================================================================
def create_single_product_photo_report(product, product_images):
    doc = Document()
    section = doc.sections[0]
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    
    product_name = product.get('name', 'Unknown Product')
    product_size = product.get('size', '')

    # --- Tiêu đề ---
    p = doc.add_paragraph()
    p.add_run('GENERAL PHOTO\n').bold = True
    p.add_run(f'TỔNG QUAN VỀ SẢN PHẨM/ PRODUCT OVERVIEW\n').bold = True
    p.add_run(f"{product_name} SIZE {product_size}").bold = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph()

    # --- Vẽ các bảng ảnh ---
    for category, images in product_images.items():
        if not images:
            continue

        p = doc.add_paragraph()
        p.add_run(category.replace('_', ' ').title()).bold = True # Chuyển "overview" thành "Overview"

        cols = 2
        rows = (len(images) + 1) // cols
        table = doc.add_table(rows=rows, cols=cols)
        table.style = 'Table Grid'
        
        # Thiết lập chiều rộng cột
        for col in table.columns:
            col.width = Inches(3.5)

        # Chèn ảnh vào các ô
        img_idx = 0
        for r in range(rows):
            for c in range(cols):
                if img_idx < len(images):
                    try:
                        cell = table.cell(r, c)
                        cell.paragraphs[0].clear()
                        run = cell.paragraphs[0].add_run()
                        run.add_picture(BytesIO(images[img_idx]), width=Inches(3.2))
                        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                    except Exception as e:
                        print(f"Error adding image to report: {e}")
                    img_idx += 1

        doc.add_paragraph()

    doc_stream = BytesIO()
    doc.save(doc_stream)
    doc_stream.seek(0)
    return doc_stream

def handle_new_photo():
    """
    Hàm này được gọi mỗi khi st.camera_input có ảnh mới.
    Nó sẽ lưu ảnh và tăng key của camera để làm mới widget.
    """
    # Lấy thông tin từ session state
    product_name = st.session_state.get('camera_current_product')
    category = st.session_state.get('camera_current_category')
    camera_key = st.session_state.get('camera_widget_key') # Key của camera_input

    if not product_name or not category or not camera_key:
        return

    # Lấy dữ liệu ảnh từ widget camera thông qua key của nó
    img_buffer = st.session_state[camera_key]
    
    if img_buffer:
        # Thêm ảnh vào danh sách
        st.session_state.camera_images[product_name][category].append(img_buffer.getvalue())
        # Tăng key của camera để "buộc" nó làm mới cho lần chụp tiếp theo
        st.session_state.camera_key_counter += 1

# ===================================================================
# HÀM RENDER CHÍNH CỦA TAB
# ===================================================================
def render_camera_tab():
    st.header("Chụp ảnh báo cáo / Photo Report Capturing")

    # --- KHỞI TẠO CÁC BIẾN CẦN THIẾT ---
    if 'camera_images' not in st.session_state:
        st.session_state.camera_images = {}
    if 'camera_key_counter' not in st.session_state:
        st.session_state.camera_key_counter = 0

    if not st.session_state.get('inspection_data') or not st.session_state.inspection_data.get('products'):
        st.warning("Vui lòng thêm sản phẩm ở tab 'Thông tin/General' trước.")
        return

    # --- GIAO DIỆN CHỌN SẢN PHẨM VÀ DANH MỤC ---
    product_names = [p['name'] for p in st.session_state.inspection_data['products']]
    selected_product_name = st.selectbox("1. Chọn sản phẩm", product_names, key="camera_product_selector")

    categories = {
        "Overview": "Tổng quan", "Checking_weight": "Kiểm tra khối lượng",
        "Checking_size": "Kiểm tra kích cỡ", "Checking_Brix": "Kiểm tra độ Brix",
        "Checking_Firmness": "Kiểm tra độ cứng", "Serious_defects": "Lỗi nghiêm trọng",
        "Major_defects": "Lỗi lớn", "Minor_defects": "Lỗi nhẹ",
        "Shattering_Berries": "Quả bị rụng"
    }
    selected_category = st.selectbox("2. Chọn danh mục ảnh", options=list(categories.keys()), format_func=lambda k: categories[k])

    # Lưu lựa chọn hiện tại vào session để hàm callback có thể truy cập
    st.session_state.camera_current_product = selected_product_name
    st.session_state.camera_current_category = selected_category

    # Khởi tạo cấu trúc lưu trữ cho sản phẩm nếu chưa có
    if selected_product_name not in st.session_state.camera_images:
        st.session_state.camera_images[selected_product_name] = {cat: [] for cat in categories}

    st.markdown("---")
    
    # --- GIAO DIỆN CHỤP ẢNH LIỀN MẠCH ---
    st.subheader(f"3. Chụp ảnh cho '{categories[selected_category]}'")

    # Tạo key động cho camera_input
    camera_key = f"camera_widget_{st.session_state.camera_key_counter}"
    st.session_state.camera_widget_key = camera_key

    st.camera_input(
        "Nhấn để chụp ảnh",
        key=camera_key,
        on_change=handle_new_photo # GỌI HÀM CALLBACK KHI CÓ THAY ĐỔI
    )

    # --- HIỂN THỊ CÁC ẢNH ĐÃ CHỤP ---
    st.markdown("---")
    st.subheader(f"Các ảnh đã chụp cho mục này")
    
    current_images = st.session_state.camera_images.get(selected_product_name, {}).get(selected_category, [])
    
    if not current_images:
        st.info("Chưa có ảnh nào cho mục này.")
    else:
        cols = st.columns(4) 
        for i, img_bytes in enumerate(current_images):
            with cols[i % 4]:
                st.image(img_bytes, use_container_width=True)
                if st.button(f"Xóa ảnh {i+1}", key=f"del_{selected_product_name}_{selected_category}_{i}", use_container_width=True):
                    del st.session_state.camera_images[selected_product_name][selected_category][i]
                    st.rerun()

    # --- TẠO VÀ TẢI BÁO CÁO ---
    st.markdown("---")
    st.header("Tạo và Tải báo cáo")
    st.info("Báo cáo sẽ được tạo riêng cho từng sản phẩm có ảnh. Bạn có thể tải từng file hoặc tải tất cả trong một file nén (.zip).")

    # Lấy danh sách sản phẩm có ảnh
    products_with_images = []
    all_products = st.session_state.inspection_data.get('products', [])
    for product in all_products:
        if product['name'] in st.session_state.camera_images and any(st.session_state.camera_images[product['name']].values()):
            products_with_images.append(product)

    if not products_with_images:
        st.warning("Chưa có ảnh nào được chụp.")
    else:
        # Tạo các nút download riêng lẻ
        for product in products_with_images:
            product_name = product['name']
            report_stream = create_single_product_photo_report(product, st.session_state.camera_images[product_name])
            st.download_button(
                label=f"Tải Báo cáo cho '{product_name}'",
                data=report_stream,
                file_name=f"Photo_Report_{product_name.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        # Tạo nút tải file ZIP
        if len(products_with_images) > 1:
            if st.button("Tải tất cả dưới dạng file ZIP"):
                with st.spinner("Đang nén các báo cáo..."):
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                        for product in products_with_images:
                            product_name = product['name']
                            report_stream = create_single_product_photo_report(product, st.session_state.camera_images[product_name])
                            file_name = f"Photo_Report_{product_name.replace(' ', '_')}.docx"
                            zip_file.writestr(file_name, report_stream.getvalue())
                    
                    st.download_button(
                        label="Tải xuống file ZIP",
                        data=zip_buffer.getvalue(),
                        file_name="All_Photo_Reports.zip",
                        mime="application/zip"
                    )