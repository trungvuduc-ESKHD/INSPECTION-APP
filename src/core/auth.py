import json
import streamlit as st
from pathlib import Path
import hashlib

# --- DATABASE SETUP ---
DB_FILE = Path(__file__).parent.parent.parent / "data" / "users.json"

def init_user_db():
    """Tạo file users.json nếu chưa tồn tại với một admin mặc định."""
    if not DB_FILE.exists():
        # Mã hóa mật khẩu mặc định 'admin'
        hashed_password = hashlib.sha256('admin'.encode()).hexdigest()
        default_users = {
            "admin": {
                "password": hashed_password,
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
def verify_password(plain_password, hashed_password):
    """Kiểm tra mật khẩu."""
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password

def check_login(username, password):
    """Kiểm tra thông tin đăng nhập và trả về vai trò nếu thành công."""
    users = get_users()
    if username in users:
        user_data = users[username]
        if verify_password(password, user_data["password"]):
            return user_data["role"]
    return None

def register_user(username, password, role="user"):
    """Đăng ký người dùng mới."""
    users = get_users()
    if username in users:
        return False, "Tên đăng nhập đã tồn tại."
    if len(password) < 6:
        return False, "Mật khẩu phải có ít nhất 6 ký tự."
        
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users[username] = {"password": hashed_password, "role": role}
    save_users(users)
    return True, "Đăng ký thành công!"