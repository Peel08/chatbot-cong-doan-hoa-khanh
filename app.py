import streamlit as st
from groq import Groq

# 1. CẤU HÌNH TRANG CAO CẤP
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="🏛️", layout="wide")

# 2. HỆ THỐNG GIAO DIỆN NGUYÊN KHỐI (DIỆT TẬN GỐC LỖI Ô TRẮNG)
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;600;900&display=swap');

    /* Nền tổng thể: Gradient tối sang trọng */
    .stApp {
        background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
        font-family: 'Urbanist', sans-serif;
    }

    /* DIỆT TẬN GỐC Ô TRẮNG: Ép toàn bộ container của Streamlit về tàng hình */
    [data-testid="stVerticalBlock"], [data-testid="stColumn"], [data-testid="stImage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Khung đăng nhập phong cách Glassmorphism (Kính mờ) */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 80vh;
        width: 100%;
    }

    .login-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 50px 40px;
        width: 100%;
        max-width: 420px;
        text-align: center;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
    }

    /* Hiệu ứng Robot bay lơ lửng thực thụ */
    .robot-img {
        width: 180px;
        filter: drop-shadow(0 20px 30px rgba(0, 100, 255, 0.3));
        margin-bottom: -30px;
        z-index: 100;
        animation: float 4s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-20px); }
    }

    /* Tiêu đề & Chữ */
    .title-main { color: #f8fafc; font-weight: 900; font-size: 2.5rem; letter-spacing: -1px; margin: 0; }
    .subtitle { color: #38bdf8; font-weight: 600; letter-spacing: 3px; font-size: 0.8rem; margin-bottom: 30px; }

    /* Input mượt mà */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 15px !important;
        height: 50px !important;
        text-align: center;
    }

    /* Nút bấm Gold Luxury */
    div.stButton > button {
        background: linear-gradient(135deg, #ffd700 0%, #b8860b 100%) !important;
        color: #0f172a !important;
        border: none !important;
        border-radius: 15px !important;
        height: 55px !important;
        width: 100% !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        text-transform: uppercase;
        transition: 0.4s all;
    }
    div.stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.4);
    }

    /* Bản quyền tác giả Phát */
    .author-info { margin-top: 35px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px; }
    .author-name { color: #ffd700; font-size: 1.1rem; font-weight: 800; display: block; }
    .author-sub { color: #94a3b8; font-size: 0.75rem; }

    header, footer, #MainMenu {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 3. KHO DỮ LIỆU CHÍNH XÁC
KNOWLEDGE_BASE = "Dữ liệu Công đoàn xã Hòa Khánh: Lương Tấn Phát phát triển, số hóa hành chính 2026."

# 4. API GROQ
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("🔑 API Key missing!")
    st.stop()

if "logged" not in st.session_state: st.session_state.logged = False

# --- GIAO DIỆN ĐĂNG NHẬP ---
if not st.session_state.logged:
    # Dùng HTML thủ công để đảm bảo robot nằm đúng chỗ không bị dính ô trắng
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Hiển thị robot lơ lửng
    st.markdown(f'<center><img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" class="robot-img"></center>', unsafe_allow_html=True)
    
    # Card đăng nhập
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<h1 class="title-main">HÒA KHÁNH AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">KỶ NGUYÊN SỐ CÔNG ĐOÀN V4.0</p>', unsafe_allow_html=True)
    
    name = st.text_input("Username", placeholder="Danh tính cán bộ...", label_visibility="collapsed")
    
    if st.button("KÍCH HOẠT HỆ THỐNG"):
        if name:
            st.session_state.user = name
            st.session_state.logged = True
            st.rerun()
        else: st.warning("Vui lòng nhập tên!")

    st.markdown(f'''
        <div class="author-info">
            <span class="author-sub">Kiến tạo bởi:</span>
            <span class="author-name">LƯƠNG TẤN PHÁT</span>
            <span class="author-sub">Hòa Khánh Digital AI © 2026</span>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# --- GIAO DIỆN CHAT (LUXURY MODE) ---
else:
    with st.sidebar:
        st.markdown(f"<div style='text-align:center;'><img src='https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png' width='100'><h3 style='color:white;'>{st.session_state.user}</h3><p style='color:#ffd700;'>ADMIN ACTIVE</p></div>", unsafe_allow_html=True)
        if st.button("LÀM MỚI"): st.rerun()
        if st.button("ĐĂNG XUẤT"): 
            st.session_state.logged = False
            st.rerun()

    st.markdown("<h2 style='color:white; border-bottom: 2px solid #ffd700; padding-bottom:10px;'>🏛️ TRỢ LÝ SỐ NGHIỆP VỤ</h2>", unsafe_allow_html=True)
    # Phần Chat anh giữ nguyên logic cũ vì nó đã ổn định.
