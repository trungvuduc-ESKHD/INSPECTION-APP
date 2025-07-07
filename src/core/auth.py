# src/core/auth.py (LOGIC ONLY)

from .supabase_client import supabase
import streamlit as st # Chỉ dùng để debug hoặc báo lỗi

def sign_up(email, password, username):
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "username": username
                }
            }
        })
        return True, "Đăng ký thành công! Vui lòng kiểm tra email để xác nhận."
    except Exception as e:
        error_str = str(e)
        if 'duplicate key value violates unique constraint "profiles_username_key"' in error_str:
            return False, "Tên người dùng đã tồn tại."
        if 'User already registered' in error_str:
            return False, "Email này đã được đăng ký."
        if 'Database error saving new user' in error_str:
             return False, "Lỗi CSDL khi tạo người dùng. Có thể do Trigger hoặc cấu trúc bảng 'profiles' bị sai."
        return False, error_str

def sign_in(email, password):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        if res.user:
            profile_res = supabase.table("profiles").select("role, username").eq("id", res.user.id).single().execute()
            if profile_res.data:
                role = profile_res.data.get("role", "user")
                username = profile_res.data.get("username", "N/A")
                return res.user, username, role
            else:
                return None, None, "Không tìm thấy hồ sơ người dùng tương ứng."
    except Exception as e:
        return None, None, str(e)

def sign_out():
    try:
        supabase.auth.sign_out()
    except Exception as e:
        st.warning(f"Lỗi khi đăng xuất: {e}")

def get_all_users():
    try:
        response = supabase.table('profiles').select('id, username, role').execute()
        return response.data
    except Exception as e:
        st.error(f"Lỗi khi lấy danh sách người dùng: {e}")
        return []

def update_user_role(user_id, new_role):
    try:
        supabase.table('profiles').update({'role': new_role}).eq('id', user_id).execute()
        return True, f"Đã cập nhật vai trò thành công."
    except Exception as e:
        return False, f"Lỗi khi cập nhật vai trò: {e}"
