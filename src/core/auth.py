import json
import streamlit as st
from pathlib import Path
import bcrypt

# --- DATABASE SETUP ---
# Trỏ đến vị trí mới trong thư mục data
DB_FILE = Path(__file__).parent.parent.parent / "data" / "users.json"

def init_user_db():
    """Tạo file users.json nếu chưa tồn tại với một admin mặc định, sử dụng bcrypt."""
    if not DB_FILE.exists():

        password_bytes = 'admin'.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        # ---------------------------

        default_users = {
            "admin": {
                # Lưu chuỗi bytes đã được mã hóa dưới dạng string để ghi vào JSON
                "password": hashed_password.decode('utf-8'), 
                "role": "manager"
            }
        }
        with open(DB_FILE, 'w') as f:
            json.dump(default_users, f, indent=4)

def get_users():
    """Đọc toàn bộ người dùng từ file JSON."""
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_users(users_dict):
    """Lưu lại toàn bộ người dùng vào file JSON."""
    with open(DB_FILE, 'w') as f:
        json.dump(users_dict, f, indent=4)

# --- AUTHENTICATION FUNCTIONS ---

def verify_password(plain_password, hashed_password_str):
    """Kiểm tra mật khẩu sử dụng bcrypt."""
    password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password_str.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)

def check_login(username, password):
    """Kiểm tra thông tin đăng nhập và trả về vai trò nếu thành công."""
    users = get_users()
    if username in users:
        user_data = users[username]
        if verify_password(password, user_data["password"]):
            return user_data["role"]
    return None

def register_user(username, password, role="user"):
    """Đăng ký người dùng mới với mật khẩu được băm bằng bcrypt."""
    users = get_users()
    if username in users:
        return False, "Tên đăng nhập đã tồn tại."
    if len(password) < 6:
        return False, "Mật khẩu phải có ít nhất 6 ký tự."
        
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    # ---------------------------
    
    users[username] = {
        "password": hashed_password.decode('utf-8'), 
        "role": role
    }
    save_users(users)
    return True, "Đăng ký thành công!"
