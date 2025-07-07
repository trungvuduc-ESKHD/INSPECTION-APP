from src.core.supabase_client import supabase

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
        if 'duplicate key value violates unique constraint "profiles_username_key"' in str(e):
            return False, "Tên người dùng đã tồn tại."
        if 'User already registered' in str(e):
            return False, "Email này đã được đăng ký."
        return False, str(e)

def sign_in(email, password):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        if res.user:
            # Lấy vai trò từ bảng profiles
            profile = supabase.table("profiles").select("role").eq("id", res.user.id).single().execute()
            role = profile.data.get("role", "user")
            return res.user, role
    except Exception as e:
        return None, str(e)
