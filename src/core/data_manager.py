import json
import streamlit as st
from pathlib import Path
import datetime
import uuid
import numpy as np
import base64
from PIL import Image
from io import BytesIO
from .default_data import get_default_inspection_data
import os

# --- CẤU HÌNH ĐƯỜNG DẪN ---
DATA_DIR = Path(__file__).parent.parent.parent / "data"
REPORTS_DIR = DATA_DIR / "reports"
REPORTS_DB_FILE = DATA_DIR / "reports_db.json"

# ==========================================================
class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            try:
                img = Image.fromarray(obj.astype(np.uint8))
                buffer = BytesIO()
                img.save(buffer, format="PNG")
                return f"base64_image:{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
            except Exception:
                return None
        return json.JSONEncoder.default(self, obj)
# HÀM KHỞI TẠO ĐÃ ĐƯỢC CẢI TIẾN
# ==========================================================
def init_report_db():
    """
    Ensures the data directory and reports database file exist and are valid.
    If the DB file is empty or invalid, it initializes it with an empty list.
    """
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    
    # Kiểm tra xem file có tồn tại và có nội dung không
    try:
        # Nếu file tồn tại và có kích thước > 0
        if REPORTS_DB_FILE.exists() and REPORTS_DB_FILE.stat().st_size > 0:
            # Thử đọc file để chắc chắn nó là JSON hợp lệ
            with open(REPORTS_DB_FILE, 'r') as f:
                json.load(f)
        else:
            # Nếu file không tồn tại hoặc trống, tạo/ghi đè với danh sách rỗng
            with open(REPORTS_DB_FILE, 'w') as f:
                json.dump([], f)
    except json.JSONDecodeError:
        # Nếu file tồn tại nhưng chứa nội dung không hợp lệ, ghi đè nó
        with open(REPORTS_DB_FILE, 'w') as f:
            json.dump([], f)

# --- CÁC HÀM QUẢN LÝ BÁO CÁO ---
def get_all_reports_metadata():
    init_report_db()
    with open(REPORTS_DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_all_reports_metadata(metadata_list):
    init_report_db()
    with open(REPORTS_DB_FILE, 'w') as f:
        json.dump(metadata_list, f, indent=4)

def create_new_report(username: str, report_name: str):
    init_report_db()
    report_id = str(uuid.uuid4())
    file_name = f"{report_id}.json"
    new_report_data = get_default_inspection_data()
    
    new_report_data['generalInfo']['report_name'] = report_name
    new_report_data['generalInfo']['report_id'] = report_id

    # Gọi hàm save_report_data để đảm bảo dùng đúng bộ mã hóa
    save_report_data(file_name, new_report_data)

    metadata = get_all_reports_metadata()
    metadata.append({
        "report_id": report_id, "report_name": report_name, "file_name": file_name,
        "created_by": username, "created_at": datetime.datetime.now().isoformat(),
        "status": "draft", "assigned_to": None
    })
    save_all_reports_metadata(metadata)
    return report_id

def load_report_data(file_name: str):
    """Tải dữ liệu và giải mã ảnh chữ ký."""
    file_path = REPORTS_DIR / file_name
    if not file_path.exists():
        return None
        
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
            # --- LOGIC GIẢI MÃ CHỮ KÝ ---
            for key in ['inspector_signature', 'reviewer_signature']:
                if key in data and isinstance(data[key], str) and data[key].startswith("base64_image:"):
                    base64_str = data[key].split(':', 1)[1]
                    img_bytes = base64.b64decode(base64_str)
                    img = Image.open(BytesIO(img_bytes))
                    data[key] = np.array(img)
            return data
        except json.JSONDecodeError:
            st.error(f"Lỗi đọc file báo cáo '{file_name}'. File có thể bị hỏng.")
            return None # Trả về None nếu file hỏng

def save_report_data(file_name: str, data: dict):
    """Lưu dữ liệu và mã hóa ảnh chữ ký."""
    file_path = REPORTS_DIR / file_name
    with open(file_path, 'w') as f:
        # Sử dụng bộ mã hóa tùy chỉnh khi lưu
        json.dump(data, f, indent=4, cls=NumpyArrayEncoder)


def update_report_status(report_id: str, new_status: str):
    """Cập nhật trạng thái của một báo cáo."""
    metadata = get_all_reports_metadata()
    for report in metadata:
        if report['report_id'] == report_id:
            report['status'] = new_status
            break
    save_all_reports_metadata(metadata)

def assign_report(report_id: str, admin_username: str):
    """Giao một báo cáo cho admin."""
    metadata = get_all_reports_metadata()
    for report in metadata:
        if report['report_id'] == report_id:
            report['assigned_to'] = admin_username
            report['status'] = 'pending_review' # Tự động chuyển trạng thái
            break
    save_all_reports_metadata(metadata)

def delete_report(report_id: str):
    """Xóa một báo cáo dựa trên ID của nó."""
    all_metadata = get_all_reports_metadata()
    
    report_to_delete = None
    for report in all_metadata:
        if report['report_id'] == report_id:
            report_to_delete = report
            break
            
    if report_to_delete:
        # Xóa file JSON chi tiết
        file_path = REPORTS_DIR / report_to_delete['file_name']
        try:
            if file_path.exists():
                os.remove(file_path)
        except OSError as e:
            st.error(f"Lỗi khi xóa file báo cáo: {e}")
            return False, f"Không thể xóa file: {report_to_delete['file_name']}"

        # Xóa entry khỏi metadata
        updated_metadata = [r for r in all_metadata if r['report_id'] != report_id]
        save_all_reports_metadata(updated_metadata)
        return True, f"Đã xóa thành công báo cáo: {report_to_delete['report_name']}"
    
    return False, "Không tìm thấy báo cáo để xóa."