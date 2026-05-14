import streamlit as st
from groq import Groq
import os

# 1. CẤU HÌNH TRANG PREMIUM
st.set_page_config(
    page_title="Hòa Khánh Digital AI - Lương Tấn Phát", 
    page_icon="🏛️", 
    layout="wide"
)

# 2. HỆ THỐNG GIAO DIỆN (Lấp đầy ô trống bằng chữ HÒA KHÁNH)
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&display=swap');

    /* Nền tổng thể Dark Luxury */
    .stApp {
        background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
        font-family: 'Montserrat', sans-serif;
    }

    /* DIỆT TẬN GỐC CÁC KHUNG TRẮNG MẶC ĐỊNH */
    [data-testid="stVerticalBlock"], [data-testid="stColumn"], [data-testid="stImage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* BRANDING CONTAINER: Robot + Bảng tên Hòa Khánh */
    .brand-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-bottom: -50px;
        z-index: 100;
        position: relative;
    }

    /* BIẾN Ô TRẮNG THÀNH BẢNG TÊN SANG TRỌNG */
    .brand-label {
        background: white;
        padding: 12px 60px;
        border-radius: 50px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        border: 3px solid #ffd700; /* Viền vàng Gold sang trọng */
        color: #003366;
        font-weight: 900;
        font-size: 2rem;
        letter-spacing: 8px; /* Dãn chữ kiểu hiện đại */
        margin-top: -30px;
        text-transform: uppercase;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { box-shadow: 0 0 10px rgba(255, 215, 0, 0.2); }
        to { box-shadow: 0 0 30px rgba(255, 215, 0, 0.5); }
    }

    .robot-main {
        width: 180px;
        filter: drop-shadow(0 20px 30px rgba(0, 100, 255, 0.3));
        animation: float 4s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-15px); }
    }

    /* CARD ĐĂNG NHẬP */
    .login-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 60px 40px 40px 40px;
        width: 100%;
        max-width: 450px;
        text-align: center;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
        margin: auto;
    }

    /* Input & Nút bấm */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border-radius: 15px !important;
        height: 50px !important;
        text-align: center;
        font-size: 1.1rem !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #ffd700 0%, #b8860b 100%) !important;
        color: #0f172a !important;
        border-radius: 15px !important;
        height: 55px !important;
        width: 100% !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        border: none !important;
        transition: 0.4s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.4);
    }

    /* Sidebar Dark */
    [data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    header, footer, #MainMenu {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 3. KHO DỮ LIỆU & KẾT NỐI API
KNOWLEDGE_BASE = """
THÔNG TIN NGHIỆP VỤ CÔNG ĐOÀN XÃ HÒA KHÁNH:
- Chủ quản: Công đoàn xã Hòa Khánh, huyện Đức Hòa, tỉnh Long An.
- Tác giả hệ thống: Lương Tấn Phát (Phòng Chuyển đổi số cơ sở).
- Mục tiêu: Số hóa văn bản nghiệp vụ, hỗ trợ đoàn viên nhanh chóng.
"""

if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("🔑 Chưa có API Key!")
    st.stop()

if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

# --- GIAO DIỆN ĐĂNG NHẬP ---
if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Khu vực trung tâm
    st.markdown('<div class="brand-section">', unsafe_allow_html=True)
    st.markdown(f'<img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" class="robot-main">', unsafe_allow_html=True)
    st.markdown('<div class="brand-label">HÒA KHÁNH</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    _, col_card, _ = st.columns([1, 1.5, 1])
    with col_card:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='color: white; margin: 0; font-weight: 900;'>AI SYSTEM</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #38bdf8; font-weight: 600; letter-spacing: 2px; margin-bottom: 30px;'>KỶ NGUYÊN SỐ CÔNG ĐOÀN V4.0</p>", unsafe_allow_html=True)
        
        name = st.text_input("Username", placeholder="Danh tính cán bộ...", label_visibility="collapsed")
        
        if st.button("KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
            else: st.warning("Vui lòng nhập tên!")

        st.markdown(f'''
            <div style="margin-top: 35px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px;">
                <p style="color: #94a3b8; font-size: 0.75rem;">Kiến tạo bởi:</p>
                <b style="color:#ffd700; font-size: 1.1rem; letter-spacing: 1px;">LƯƠNG TẤN PHÁT</b><br>
                <span style="color: #64748b; font-size: 0.7rem;">Hòa Khánh Digital AI © 2026</span>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- GIAO DIỆN CHÍNH (SAU KHI LOGGED) ---
else:
    with st.sidebar:
        st.markdown(f'''
            <div style="text-align:center; padding: 20px;">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="100">
                <h3 style="color:white; margin-top:10px;">{st.session_state.user}</h3>
                <p style="color:#ffd700;">HÒA KHÁNH ADMIN</p>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("LÀM MỚI CHAT"):
            st.session_state.messages = []
            st.rerun()
        if st.button("ĐĂNG XUẤT"):
            st.session_state.logged = False
            st.rerun()

    st.markdown("<h2 style='color:white; border-bottom: 2px solid #ffd700; padding-bottom:10px;'>🏛️ TRỢ LÝ SỐ NGHIỆP VỤ</h2>", unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Hỏi tôi về nghiệp vụ công đoàn..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Đang trích xuất dữ liệu..."):
                try:
                    res = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": f"Bạn là trợ lý AI Công đoàn xã Hòa Khánh. Sử dụng dữ liệu: {KNOWLEDGE_BASE}. Gọi người dùng là Anh/Chị {st.session_state.user}."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.3-70b-versatile"
                    )
                    ans = res.choices[0].message.content
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except:
                    st.error("Lỗi kết nối AI!")
