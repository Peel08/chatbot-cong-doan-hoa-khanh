import streamlit as st
from groq import Groq
from docx import Document
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="🤖", layout="centered")

# 2. CSS "ÉP CHỮ VÀO Ô" - BIẾN Ô TRỐNG THÀNH BANNER SANG TRỌNG
st.markdown('''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;600;700&display=swap');

    html, body, [class*="st-emotion-cache"] {
        font-family: 'Urbanist', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%);
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* Căn chỉnh lại vị trí */
    .stApp .block-container {
        padding-top: 2rem !important;
    }

    .login-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    /* === BIẾN Ô TRẮNG THÀNH BANNER CHỮ === */
    .brand-banner {
        background: #003366; /* Màu xanh Navy sang trọng */
        color: white;
        padding: 15px 40px;
        border-radius: 50px; /* Bo tròn cực đại như cái ô trong hình của bạn */
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: 2px;
        box-shadow: 0 10px 25px rgba(0, 51, 102, 0.2);
        margin-top: -20px;
        margin-bottom: 20px;
        border: 2px solid #ffffff;
        text-align: center;
        min-width: 350px;
    }

    /* Card Đăng nhập phía dưới */
    .login-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
        width: 100%;
        max-width: 480px;
        text-align: center;
    }

    /* Robot bay */
    .floating-robot {
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 15px 25px rgba(0, 68, 148, 0.2));
        z-index: 10;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }

    /* Nút bấm */
    div.stButton > button {
        background: linear-gradient(90deg, #003366 0%, #0056b3 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        height: 55px !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 17px !important;
        border: none !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 51, 102, 0.3);
    }
</style>
''', unsafe_allow_html=True)

# 3. Quản lý trạng thái (Giữ nguyên)
if "logged" not in st.session_state: st.session_state.logged = False

# 4. GIAO DIỆN ĐĂNG NHẬP
if not st.session_state.logged:
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    
    # 1. Con Robot
    st.markdown('<div class="floating-robot">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=160)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. CÁI Ô TRẮNG GIỜ ĐÃ CÓ CHỮ (BRAND BANNER)
    st.markdown('<div class="brand-banner">HÒA KHÁNH AI</div>', unsafe_allow_html=True)

    # 3. Card nhập liệu phía dưới
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<p style='color: #003366; font-weight: 600; margin-bottom: 25px;'>TRỢ LÝ SỐ CÔNG ĐOÀN V3.3</p>", unsafe_allow_html=True)
    
    name = st.text_input("Username", placeholder="Nhập tên Anh/Chị để bắt đầu...", label_visibility="collapsed")
    
    if st.button("KÍCH HOẠT HỆ THỐNG"):
        if name:
            st.session_state.user = name
            st.session_state.logged = True
            st.rerun()
        else:
            st.warning("Vui lòng nhập tên!")
    
    st.markdown(f'''
    <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 30px; border-top: 1px solid #eee; padding-top: 20px;">
        Phát triển bởi: <b>Lương Tấn Phát</b><br>
        <i>Chuyển đổi số Công đoàn xã Hòa Khánh</i>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

else:
    st.success(f"Chào mừng {st.session_state.user} đã quay trở lại!")
    if st.button("Đăng xuất"):
        st.session_state.logged = False
        st.rerun()
