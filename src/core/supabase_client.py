
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_supabase_connection():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase: Client = init_supabase_connection()

def get_users():
    response = supabase.table("users").select("*").execute()
    return response.data
def save_users(users):
    for user in users:
        supabase.table("users").insert(user).execute()

def upload_file(bucket_name: str, file_path: str, file_body: bytes, file_options: dict = None):
    """Tải một file lên Supabase Storage, xử lý trường hợp file đã tồn tại."""
    if file_options is None:
        file_options = {"content-type": "application/octet-stream", "upsert": "true"}
    else:
        # Đảm bảo upsert là true để có thể ghi đè
        file_options["upsert"] = "true" 
    try:
        # Sử dụng tham số upsert=True trong chính lệnh upload
        # để Supabase tự động xử lý việc tạo mới hoặc cập nhật.
        # Điều này đơn giản và hiệu quả hơn việc bắt lỗi "Duplicate".
        supabase.storage.from_(bucket_name).upload(
            path=file_path,
            file=file_body,
            file_options=file_options
        )
        # Lấy URL công khai của file vừa tải lên/cập nhật
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
        return public_url
    except GotrueError as e:
        st.error(f"Lỗi xác thực khi tải file: {e}")
        return None
    except Exception as e:
        st.error(f"Lỗi không xác định khi tải file lên Supabase: {e}")
        return None
