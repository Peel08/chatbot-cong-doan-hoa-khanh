import streamlit as st
from groq import Groq
import os

# 1. THIẾT LẬP CẤU HÌNH TRANG
st.set_page_config(
    page_title="Hòa Khánh Digital AI - Lương Tấn Phát", 
    page_icon="🏛️", 
    layout="wide"
)

# 2. HỆ THỐNG GIAO DIỆN LUXURY - FIX TRIỆT ĐỂ LỖI Ô TRẮNG
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');

    /* Font và Nền */
    html, body, [class*="st-emotion-cache"] {
        font-family: 'Montserrat', sans-serif;
    }
    .stApp {
        background: linear-gradient(160deg, #f0f4f8 0%, #d9e2ec 100%);
    }

    /* XỬ LÝ LỖI Ô TRẮNG: Ép tất cả container chứa ảnh/cột về trong suốt */
    [data-testid="stVerticalBlock"] > div, 
    [data-testid="stHorizontalBlock"] > div,
    .stImage > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* Card Đăng nhập */
    .login-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        border-radius: 30px;
        padding: 40px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 25px 50px rgba(0, 30, 60, 0.1);
        text-align: center;
        margin-top: -30px; /* Ép card sát lên robot */
    }

    /* Sidebar Business Dark */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001e3c 0%, #003366 100%) !important;
        border-right: 2px solid #ffd700 !important;
    }

    /* Nút bấm Premium */
    div.stButton > button {
        background: linear-gradient(90deg, #003366 0%, #0056b3 100%) !important;
        color: #ffffff !important;
        border: 1px solid #ffd700 !important;
        border-radius: 12px !important;
        height: 50px !important;
        font-weight: 700 !important;
        width: 100% !important;
        transition: 0.3s all ease;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3);
    }

    /* Ẩn menu mặc định */
    header, footer, #MainMenu {visibility: hidden;}

    /* Footer */
    .premium-footer {
        text-align: center;
        padding: 25px;
        color: #486581;
        font-size: 0.85rem;
        border-top: 1px solid #bcccdc;
        margin-top: 50px;
    }
</style>
''', unsafe_allow_html=True)

# 3. KHO DỮ LIỆU NGHIỆP VỤ
KNOWLEDGE_BASE = """
DANH MỤC DỮ LIỆU CÔNG ĐOÀN XÃ HÒA KHÁNH (2026):
- Dự án "Hòa Khánh Digital AI" do Lương Tấn Phát phát triển.
- Công đoàn xã Hòa Khánh trực thuộc Liên đoàn Lao động huyện.
- Hỗ trợ giải đáp nghiệp vụ, điều lệ Đoàn và các thủ tục hành chính số.
"""

# 4. KẾT NỐI API
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Vui lòng cấu hình GROQ_API_KEY!")
    st.stop()

# 5. QUẢN LÝ TRẠNG THÁI
if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

# --- GIAO DIỆN ĐĂNG NHẬP ---
if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    # Dùng columns để căn giữa nhưng ép nền trong suốt bằng CSS ở trên
    _, col_login, _ = st.columns([1, 1.5, 1])
    
    with col_login:
        # Hiển thị ảnh Robot trực tiếp, CSS ở trên sẽ lo việc xóa ô trắng
        st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=180)
        
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='color: #003366; margin-bottom: 5px; font-weight: 800;'>HÒA KHÁNH AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #0056b3; font-weight: 600; letter-spacing: 1px; margin-bottom: 30px;'>KỶ NGUYÊN SỐ CÔNG ĐOÀN V4.0</p>", unsafe_allow_html=True)
        
        name = st.text_input("TÊN CÁN BỘ", placeholder="Họ tên Anh/Chị...", label_visibility="collapsed")
        
        if st.button("KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
            else:
                st.warning("⚠️ Vui lòng nhập định danh!")
        
        st.markdown(f'''
            <div style="margin-top: 30px; border-top: 1px solid #e2e8f0; padding-top: 20px;">
                <p style="font-size: 0.75rem; color: #64748b;">Thiết kế & Phát triển bởi:<br>
                <b style="color:#003366; font-size: 1rem;">LƯƠNG TẤN PHÁT</b><br>Hòa Khánh Digital AI</p>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- GIAO DIỆN LÀM VIỆC CHÍNH ---
else:
    with st.sidebar:
        st.markdown(f'''
            <div style="text-align: center; padding: 20px;">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="100">
                <p style="color: #ffd700; margin-top: 10px; font-weight: 600;">CÁN BỘ TRỰC</p>
                <h3 style="color: white; margin: 0;">{st.session_state.user}</h3>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 LÀM MỚI"):
            st.session_state.messages = []
            st.rerun()
        if st.button("🚪 ĐĂNG XUẤT"):
            st.session_state.logged = False
            st.rerun()

    st.markdown(f'''
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 3px solid #003366; padding-bottom: 10px; margin-bottom: 25px;">
            <h2 style='color: #003366; margin: 0; font-weight: 800;'>TRỢ LÝ SỐ HÒA KHÁNH</h2>
            <div style="background: #003366; color: #ffd700; padding: 5px 15px; border-radius: 10px; font-weight: 800;">V4.0 PREMIUM</div>
        </div>
    ''', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Hỏi tôi về nghiệp vụ Công đoàn..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                res = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"Bạn là trợ lý AI Công đoàn xã Hòa Khánh. Dữ liệu: {KNOWLEDGE_BASE}. Gọi người dùng là Anh/Chị {st.session_state.user}."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.3-70b-versatile"
                )
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except:
                st.error("Lỗi kết nối AI!")

st.markdown(f'''<div class="premium-footer">Tác giả: <b>Lương Tấn Phát</b> | Hòa Khánh Digital AI © 2026</div>''', unsafe_allow_html=True)
