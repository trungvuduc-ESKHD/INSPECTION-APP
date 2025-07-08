
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
    """Tải một file lên Supabase Storage."""
    if file_options is None:
        file_options = {"content-type": "application/octet-stream"}
    try:
        # Tải file lên
        supabase.storage.from_(bucket_name).upload(
            path=file_path,
            file=file_body,
            file_options=file_options
        )
        # Lấy URL công khai của file vừa tải lên
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
        return public_url
    except Exception as e:
        # Xử lý trường hợp file đã tồn tại
        if "Duplicate" in str(e):
            # Cập nhật file đã có
            supabase.storage.from_(bucket_name).update(
                path=file_path,
                file=file_body,
                file_options=file_options
            )
            public_url = supabase.storage.from_(bucket_name).get_public_url(file_path)
            return public_url
        else:
            st.error(f"Lỗi khi tải file lên Supabase: {e}")
            return None
