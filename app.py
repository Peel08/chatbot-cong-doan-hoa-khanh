import streamlit as st
from groq import Groq
import os

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Hòa Khánh Digital AI - Lương Tấn Phát", page_icon="🏛️", layout="wide")

# 2. HỆ THỐNG CSS PHỦ ĐẦU - DIỆT TẬN GỐC Ô TRẮNG
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&display=swap');

    /* Nền tổng thể */
    .stApp {
        background: linear-gradient(160deg, #f0f4f8 0%, #d9e2ec 100%);
        font-family: 'Montserrat', sans-serif;
    }

    /* TRIỆT TIÊU Ô TRẮNG: Ép mọi container trung gian về trong suốt */
    [data-testid="stVerticalBlock"], 
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stColumn"],
    [data-testid="stHeader"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Thiết kế Card Đăng nhập tách biệt hoàn toàn */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        max-width: 450px;
        margin: auto;
    }

    .login-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        text-align: center;
        width: 100%;
        border: 1px solid rgba(255,255,255,0.4);
        margin-top: -30px; /* Đẩy card sát lên robot */
    }

    /* Hiệu ứng Nút bấm Gold-Navy */
    div.stButton > button {
        background: linear-gradient(90deg, #003366 0%, #0056b3 100%) !important;
        color: white !important;
        border: 1px solid #ffd700 !important;
        border-radius: 12px !important;
        height: 55px !important;
        width: 100% !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,51,102,0.3);
        border-color: white !important;
    }

    /* Sidebar Dark */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001e3c 0%, #003366 100%) !important;
        border-right: 2px solid #ffd700 !important;
    }

    /* Footer ẩn menu mặc định */
    header, footer, #MainMenu {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 3. KẾT NỐI API
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Thiếu API Key!")
    st.stop()

# 4. QUẢN LÝ ĐĂNG NHẬP
if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

# --- GIAO DIỆN ĐĂNG NHẬP ---
if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_main, _ = st.columns([1, 1.5, 1])
    
    with col_main:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        # Ảnh robot bay lơ lửng, không khung
        st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=180)
        
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='color:#003366; margin:0; font-weight:800;'>HÒA KHÁNH AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#0056b3; font-weight:600; margin-bottom:25px;'>KỶ NGUYÊN SỐ CÔNG ĐOÀN V4.0</p>", unsafe_allow_html=True)
        
        user_input = st.text_input("Tên", placeholder="Nhập họ tên Anh/Chị...", label_visibility="collapsed")
        
        if st.button("KÍCH HOẠT HỆ THỐNG"):
            if user_input:
                st.session_state.user = user_input
                st.session_state.logged = True
                st.rerun()
            else:
                st.warning("Vui lòng nhập định danh!")
        
        st.markdown(f'''
            <div style="margin-top:25px; border-top:1px solid #ddd; padding-top:15px;">
                <p style="font-size:0.75rem; color:#666;">Thiết kế & Phát triển bởi:<br>
                <b style="color:#003366; font-size:0.95rem;">LƯƠNG TẤN PHÁT</b><br>Hòa Khánh Digital AI © 2026</p>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

# --- GIAO DIỆN CHÍNH ---
else:
    with st.sidebar:
        st.markdown(f'''<div style="text-align:center;"><img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="100"><h3 style="color:white;">{st.session_state.user}</h3><span style="color:#ffd700;">ONLINE</span></div>''', unsafe_allow_html=True)
        if st.button("🔄 LÀM MỚI"): 
            st.session_state.messages = []
            st.rerun()
        if st.button("🚪 ĐĂNG XUẤT"): 
            st.session_state.logged = False
            st.rerun()

    st.markdown(f"<h2 style='color:#003366; border-bottom:3px solid #003366; padding-bottom:10px;'>🏛️ TRỢ LÝ SỐ HÒA KHÁNH</h2>", unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Hỏi tôi về nghiệp vụ..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                res = client.chat.completions.create(
                    messages=[{"role": "system", "content": "Bạn là trợ lý AI Công đoàn xã Hòa Khánh. Trả lời chuyên nghiệp."}, {"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                )
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except: st.error("Lỗi kết nối!")
