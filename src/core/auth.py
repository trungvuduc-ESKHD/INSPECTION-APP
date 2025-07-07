# src/core/auth.py (FINAL CORRECTED VERSION)

from .supabase_client import supabase

def sign_up(email, password, username):
    try:
        # Gửi username trong phần 'data' (sẽ trở thành raw_user_meta_data)
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
        # Xử lý các lỗi phổ biến một cách tường minh
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
            # Lấy cả role và username từ bảng profiles
            profile_res = supabase.table("profiles").select("role, username").eq("id", res.user.id).single().execute()
            
            # Kiểm tra xem có lấy được profile không
            if profile_res.data:
                role = profile_res.data.get("role", "user")
                username = profile_res.data.get("username", "N/A")
                return res.user, username, role
            else:
                # Trường hợp không có profile tương ứng
                return None, None, "Không tìm thấy hồ sơ người dùng tương ứng."
    except Exception as e:
        return None, None, str(e)

# Các hàm khác như sign_out, get_all_users, update_user_role không cần thay đổi
