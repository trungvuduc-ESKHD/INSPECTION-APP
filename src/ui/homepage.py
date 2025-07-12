import streamlit as st
from PIL import Image
import os
import time
import base64

def get_base64_image(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

def render_homepage():
    # Custom CSS for animations and styling
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        animation: fadeInDown 1s ease-out;
    }
    
    .main-header h1 {
        color: white;
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: #f0f8ff;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    .image-carousel {
        position: relative;
        height: 400px;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin: 2rem 0;
        background: linear-gradient(45deg, #ff6b35, #f7931e, #63d471, #36c5f0, #8e44ad);
        background-size: 300% 300%;
        animation: gradientShift 8s ease infinite;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .carousel-content {
        color: white;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        animation: pulse 2s ease-in-out infinite;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        animation: fadeInUp 1s ease-out;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .feature-title {
        color: #333;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.3rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #666;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    
    .stats-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        animation: pulse 2s infinite;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stats-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    .info-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 2rem 0;
        animation: slideInLeft 1s ease-out;
    }
    
    .info-section h3 {
        color: #333;
        margin-bottom: 1rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .info-section ul {
        color: #555;
        line-height: 1.8;
    }
    
    .info-section li {
        margin-bottom: 0.5rem;
    }
    
    .cta-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        text-decoration: none;
        display: inline-block;
    }
    
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.6);
    }
    
    @keyframes gradientShift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.02);
        }
        100% {
            transform: scale(1);
        }
    }
    
    .floating-elements {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .floating-fruit {
        position: absolute;
        opacity: 0.1;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 15px;
        color: #666;
    }
    
    .footer p {
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Floating background elements
    st.markdown("""
    <div class="floating-elements">
        <div class="floating-fruit" style="top: 10%; left: 10%; font-size: 3rem;">🍎</div>
        <div class="floating-fruit" style="top: 20%; right: 15%; font-size: 2.5rem; animation-delay: -2s;">🍊</div>
        <div class="floating-fruit" style="top: 60%; left: 5%; font-size: 2rem; animation-delay: -4s;">🍌</div>
        <div class="floating-fruit" style="top: 70%; right: 10%; font-size: 3.5rem; animation-delay: -1s;">🥝</div>
        <div class="floating-fruit" style="top: 40%; right: 20%; font-size: 2.8rem; animation-delay: -3s;">🍇</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>🔬 Hệ Thống Giám Định Eurofins</h1>
        <p>Công nghệ tiên tiến cho việc phân tích và đánh giá chất lượng trái cây</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simplified animated banner instead of complex carousel
    st.markdown("""
    <div class="image-carousel">
        <div class="carousel-content">
            🍎 Trái Cây Tươi 🍊
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stats-container">
            <div class="stats-number">99.9%</div>
            <div class="stats-label">Độ chính xác</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stats-container" style="animation-delay: 0.5s;">
            <div class="stats-number">10K+</div>
            <div class="stats-label">Mẫu đã phân tích</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stats-container" style="animation-delay: 1s;">
            <div class="stats-number">24/7</div>
            <div class="stats-label">Hoạt động</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("## 🌟 Tính Năng Nổi Bật")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Phân Tích Hình Ảnh AI</div>
            <div class="feature-desc">
                Sử dụng công nghệ trí tuệ nhân tạo tiên tiến để phân tích 
                hình ảnh trái cây với độ chính xác cao, nhận diện các đặc 
                điểm về màu sắc, hình dạng và chất lượng.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="animation-delay: 0.2s;">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Báo Cáo Chi Tiết</div>
            <div class="feature-desc">
                Tạo ra các báo cáo phân tích đầy đủ với biểu đồ, 
                thống kê và đánh giá chất lượng theo tiêu chuẩn 
                quốc tế Eurofins.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="feature-card" style="animation-delay: 0.4s;">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Xử Lý Nhanh Chóng</div>
            <div class="feature-desc">
                Phân tích và đưa ra kết quả trong vòng vài giây, 
                giúp tối ưu hóa quy trình kiểm định và tiết kiệm 
                thời gian.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card" style="animation-delay: 0.6s;">
            <div class="feature-icon">🛡️</div>
            <div class="feature-title">Bảo Mật Cao</div>
            <div class="feature-desc">
                Đảm bảo an toàn thông tin với các biện pháp bảo mật 
                tiên tiến, tuân thủ các tiêu chuẩn bảo mật quốc tế.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Information Section
    st.markdown("""
    <div class="info-section">
        <h3>💡 Hướng Dẫn Sử Dụng</h3>
        <p>
            Để bắt đầu sử dụng hệ thống, vui lòng chọn một trong các chức năng sau từ menu bên trái:
        </p>
        <ul>
            <li><strong>📸 Phân Tích Hình Ảnh:</strong> Upload hình ảnh trái cây để phân tích chất lượng</li>
            <li><strong>📋 Lịch Sử Kiểm Định:</strong> Xem lại các kết quả phân tích trước đó</li>
            <li><strong>📊 Thống Kê:</strong> Xem báo cáo tổng quan và thống kê</li>
            <li><strong>⚙️ Cài Đặt:</strong> Tùy chỉnh các thông số hệ thống</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="text-align: center; margin: 3rem 0;">', unsafe_allow_html=True)

    # Call to Action
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0;">
            <div class="cta-button">
                🚀 Bắt Đầu Phân Tích Ngay
            </div>
            <p style="margin-top: 1rem; color: #666; font-size: 0.9rem;">
                Vui lòng chọn chức năng từ menu bên trái để bắt đầu!
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 2rem; 
                background: #f8f9fa; border-radius: 15px; color: #666;">
        <p>© 2025 Eurofins SKHD </p>
        <p>📧 trung.vuduc@eurofinsasia.com | 📞 0377 1000 86 | 🌐 www.eurofins.com.vn
    </div>
    """, unsafe_allow_html=True)

