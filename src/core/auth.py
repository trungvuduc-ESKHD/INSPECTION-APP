from .supabase_client import supabase

def sign_up(email, password, username):
    try:
        # Đăng ký người dùng vào Supabase Auth
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
        })
        # Sau khi đăng ký thành công, tạo profile cho họ
        if res.user:
            # Mặc định role là 'user'
            profile_data = {"id": res.user.id, "username": username, "role": "user"}
            supabase.table("profiles").insert(profile_data).execute()
            return True, "Đăng ký thành công! Vui lòng kiểm tra email để xác nhận."
    except Exception as e:
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
