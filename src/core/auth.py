from .supabase_client import supabase, get_users, save_users
import streamlit as st
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sign_up(email, password, username):
    """
    Đăng ký người dùng mới
    
    Args:
        email (str): Email của người dùng
        password (str): Mật khẩu
        username (str): Tên người dùng
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Validate input
        if not email or not password or not username:
            return False, "Vui lòng điền đầy đủ thông tin."
        
        if len(password) < 6:
            return False, "Mật khẩu phải có ít nhất 6 ký tự."
        
        if len(username) < 3:
            return False, "Tên người dùng phải có ít nhất 3 ký tự."
        
        # Check if username already exists
        existing_user = supabase.table("profiles").select("username").eq("username", username).execute()
        if existing_user.data:
            return False, "Tên người dùng đã tồn tại."
        
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "username": username
                }
            }
        })
        
        if res.user:
            # Try to create profile manually if trigger didn't work
            try:
                profile_data = {
                    "id": res.user.id,
                    "username": username,
                    "role": "user"
                }
                supabase.table("profiles").insert(profile_data).execute()
                logger.info(f"Profile created manually for user: {email}")
            except Exception as profile_error:
                logger.warning(f"Profile creation failed (might already exist): {profile_error}")
            
            logger.info(f"User registered successfully: {email}")
            return True, "Đăng ký thành công! Vui lòng kiểm tra email để xác nhận."
        else:
            return False, "Đăng ký thất bại. Vui lòng thử lại."
            
    except Exception as e:
        error_str = str(e)
        logger.error(f"Sign up error: {error_str}")
        
        # Handle specific errors
        if 'duplicate key value violates unique constraint "profiles_username_key"' in error_str:
            return False, "Tên người dùng đã tồn tại."
        elif 'User already registered' in error_str:
            return False, "Email này đã được đăng ký."
        elif 'Database error saving new user' in error_str:
            return False, "Lỗi CSDL khi tạo người dùng. Có thể do Trigger hoặc cấu trúc bảng 'profiles' bị sai."
        elif 'Invalid email' in error_str:
            return False, "Email không hợp lệ."
        elif 'Password should be at least 6 characters' in error_str:
            return False, "Mật khẩu phải có ít nhất 6 ký tự."
        else:
            return False, f"Lỗi đăng ký: {error_str}"

def sign_in(email, password):
    """
    Đăng nhập người dùng
    
    Args:
        email (str): Email của người dùng
        password (str): Mật khẩu
        
    Returns:
        tuple: (user, username, role) nếu thành công, (None, None, error_message) nếu thất bại
    """
    try:
        # Validate input
        if not email or not password:
            return None, None, "Vui lòng điền đầy đủ email và mật khẩu."
        
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        
        if res.user:
            # Get user profile
            try:
                profile_res = supabase.table("profiles").select("role, username").eq("id", res.user.id).single().execute()
                
                if profile_res.data:
                    role = profile_res.data.get("role", "user")
                    username = profile_res.data.get("username", "N/A")
                    logger.info(f"User signed in successfully: {email}")
                    return res.user, username, role
                else:
                    # Profile doesn't exist, create it
                    logger.warning(f"No profile found for user: {email}, creating one...")
                    username = res.user.user_metadata.get("username", f"user_{res.user.id[:8]}")
                    
                    profile_data = {
                        "id": res.user.id,
                        "username": username,
                        "role": "user"
                    }
                    
                    create_result = supabase.table("profiles").insert(profile_data).execute()
                    
                    if create_result.data:
                        logger.info(f"Profile created for existing user: {email}")
                        return res.user, username, "user"
                    else:
                        return None, None, "Không thể tạo hồ sơ người dùng."
                        
            except Exception as profile_error:
                logger.error(f"Profile error: {profile_error}")
                return None, None, f"Lỗi khi truy cập hồ sơ người dùng: {profile_error}"
        else:
            return None, None, "Đăng nhập thất bại."
            
    except Exception as e:
        error_str = str(e)
        logger.error(f"Sign in error: {error_str}")
        
        # Handle specific errors
        if 'Invalid login credentials' in error_str:
            return None, None, "Email hoặc mật khẩu không đúng."
        elif 'Email not confirmed' in error_str:
            return None, None, "Vui lòng xác nhận email trước khi đăng nhập."
        elif 'Too many requests' in error_str:
            return None, None, "Quá nhiều lần thử đăng nhập. Vui lòng thử lại sau."
        else:
            return None, None, f"Lỗi đăng nhập: {error_str}"

def sign_out():
    """
    Đăng xuất người dùng
    """
    try:
        supabase.auth.sign_out()
        logger.info("User signed out successfully")
    except Exception as e:
        logger.error(f"Sign out error: {str(e)}")
        st.warning(f"Lỗi khi đăng xuất: {e}")

def get_current_user():
    """
    Lấy thông tin người dùng hiện tại
    
    Returns:
        dict: Thông tin người dùng hoặc None nếu chưa đăng nhập
    """
    try:
        user = supabase.auth.get_user()
        if user and user.user:
            return user.user
        return None
    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        return None

def get_all_users():
    """
    Lấy danh sách tất cả người dùng (chỉ dành cho admin)
    
    Returns:
        list: Danh sách người dùng
    """
    try:
        response = supabase.table('profiles').select('id, username, role, created_at').order('created_at', desc=True).execute()
        return response.data
    except Exception as e:
        logger.error(f"Get all users error: {str(e)}")
        st.error(f"Lỗi khi lấy danh sách người dùng: {e}")
        return []

def update_user_role(user_id, new_role):
    """
    Cập nhật vai trò người dùng
    
    Args:
        user_id (str): ID người dùng
        new_role (str): Vai trò mới
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Validate role
        valid_roles = ['user', 'admin', 'moderator']
        if new_role not in valid_roles:
            return False, f"Vai trò không hợp lệ. Chỉ chấp nhận: {', '.join(valid_roles)}"
        
        result = supabase.table('profiles').update({'role': new_role}).eq('id', user_id).execute()
        
        if result.data:
            logger.info(f"User role updated: {user_id} -> {new_role}")
            return True, "Đã cập nhật vai trò thành công."
        else:
            return False, "Không tìm thấy người dùng để cập nhật."
            
    except Exception as e:
        logger.error(f"Update user role error: {str(e)}")
        return False, f"Lỗi khi cập nhật vai trò: {e}"

def delete_user(user_id):
    """
    Xóa người dùng (chỉ dành cho admin)
    
    Args:
        user_id (str): ID người dùng
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Delete from profiles table
        result = supabase.table('profiles').delete().eq('id', user_id).execute()
        
        if result.data:
            logger.info(f"User deleted: {user_id}")
            return True, "Đã xóa người dùng thành công."
        else:
            return False, "Không tìm thấy người dùng để xóa."
            
    except Exception as e:
        logger.error(f"Delete user error: {str(e)}")
        return False, f"Lỗi khi xóa người dùng: {e}"

def reset_password(email):
    """
    Gửi email đặt lại mật khẩu
    
    Args:
        email (str): Email người dùng
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        if not email:
            return False, "Vui lòng nhập email."
        
        supabase.auth.reset_password_email(email)
        logger.info(f"Password reset email sent to: {email}")
        return True, "Đã gửi email đặt lại mật khẩu. Vui lòng kiểm tra hộp thư."
        
    except Exception as e:
        logger.error(f"Reset password error: {str(e)}")
        return False, f"Lỗi khi gửi email đặt lại mật khẩu: {e}"
