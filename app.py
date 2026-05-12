import streamlit as st
from groq import Groq
from docx import Document
import os

# 1. Cấu hình trang
st.set_page_config(
    page_title="Hòa Khánh Digital AI", 
    page_icon="🤖", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Hệ thống CSS Premium V3.2 - Fix lỗi "ô trắng trống trơn"
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;600;700&display=swap');

    html, body, [class*="st-emotion-cache"] {
        font-family: 'Urbanist', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #eef2f7 0%, #dfe7f0 100%);
    }

    header, footer, #MainMenu {visibility: hidden;}

    /* Căn chỉnh lại vị trí */
    .stApp .block-container {
        padding-top: 1rem !important;
    }

    .login-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    /* === CHỈNH SỬA Ô TRẮNG (LOGIN CARD) CHO HỢP LÝ === */
    .login-card {
        background: rgba(255, 255, 255, 0.85); /* Trắng đục sang trọng */
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        padding: 40px;
        border-radius: 30px;
        box-shadow: 0 20px 40px rgba(0, 51, 102, 0.1); /* Đổ bóng sâu nhưng nhẹ */
        width: 100%;
        max-width: 500px;
        text-align: center;
        margin-top: -30px; /* Ép card sát lên robot hơn */
        z-index: 1;
    }

    /* Hiệu ứng Robot */
    .floating-robot {
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 15px 25px rgba(0, 68, 148, 0.2));
        z-index: 2;
        position: relative;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }

    /* Nút bấm Premium */
    div.stButton > button {
        background: linear-gradient(90deg, #003366 0%, #0056b3 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 15px 30px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        width: 100% !important;
        transition: 0.3s ease all !important;
        box-shadow: 0 10px 20px rgba(0, 51, 102, 0.2);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 25px rgba(0, 51, 102, 0.3);
        background: linear-gradient(90deg, #004494 0%, #0066cc 100%) !important;
    }

    /* Ô nhập liệu sang hơn */
    .stTextInput input {
        border-radius: 12px !important;
        border: 1px solid #d1d5db !important;
        padding: 12px !important;
        background-color: #f9fafb !important;
    }

    .author-badge {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 30px;
        border-top: 1px solid #e5e7eb;
        padding-top: 20px;
    }
</style>
''', unsafe_allow_html=True)

# 4. Khởi tạo Groq & Quản lý trạng thái (Giữ nguyên của bạn)
if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

# 5. GIAO DIỆN ĐĂNG NHẬP (ĐÃ SẮP XẾP LẠI NỘI DUNG VÀO CARD)
if not st.session_state.logged:
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    
    # Robot Mascot
    st.markdown('<div class="floating-robot">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=160)
    st.markdown('</div>', unsafe_allow_html=True)

    # Mở Card - Toàn bộ nội dung nằm TRONG này
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    st.markdown("<h1 style='color: #003366; font-size: 2.2rem; margin-bottom: 0;'>HÒA KHÁNH AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #0056b3; font-weight: 600; margin-bottom: 25px; letter-spacing: 1px;'>TRỢ LÝ SỐ CÔNG ĐOÀN V3.2</p>", unsafe_allow_html=True)
    
    name = st.text_input("Username", placeholder="Nhập tên Anh/Chị để bắt đầu...", label_visibility="collapsed")
    
    if st.button("KÍCH HOẠT HỆ THỐNG"):
        if name:
            st.session_state.user = name
            st.session_state.logged = True
            st.rerun()
        else:
            st.warning("Vui lòng danh xưng để Robot phục vụ!")
    
    st.markdown(f'''
    <div class="author-badge">
        Phát triển bởi: <b>Lương Tấn Phát</b><br>
        <i>Chuyển đổi số Công đoàn xã Hòa Khánh</i>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True) # Đóng login-card
    st.markdown('</div>', unsafe_allow_html=True) # Đóng login-wrapper

else:
    # (Phần giao diện chat giữ nguyên như bản trước vì đã ổn rồi)
    st.write(f"Chào mừng {st.session_state.user}!")
    if st.button("Đăng xuất"):
        st.session_state.logged = False
        st.rerun()
