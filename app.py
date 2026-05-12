import streamlit as st
from groq import Groq
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Trợ lý ảo Hòa Khánh", page_icon="robot.png", layout="wide")

# 2. CSS "SẠCH & CÔNG NGHỆ" (Mô phỏng giao diện Tây Ninh Digital)
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    /* Nền trắng sáng hiện đại */
    .stApp { background-color: #f8faff; }

    /* Định dạng ảnh Robot căn giữa */
    .robot-container { text-align: center; padding: 20px 0; }
    .robot-img { width: 180px; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.1)); }

    /* Tiêu đề xanh Tây Ninh */
    .main-title { color: #004494; text-align: center; font-weight: bold; font-family: sans-serif; margin-bottom: 5px; }
    .sub-title { color: #555; text-align: center; font-size: 1.1rem; margin-bottom: 30px; }

    /* Thẻ tính năng (Cards) */
    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #ffcc00;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }
    .feature-icon { font-size: 24px; margin-right: 15px; }

    /* Nút bấm bo tròn đậm chất App */
    div.stButton > button {
        background: linear-gradient(180deg, #0056b3 0%, #004494 100%) !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        height: 50px !important;
        width: 100% !important;
        font-weight: bold !important;
        box-shadow: 0 4px 10px rgba(0,68,148,0.3);
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] { background-color: #004494 !important; }
    .sidebar-text { color: white !important; text-align: center; }

    /* Chân trang */
    .footer { text-align: center; color: #888; font-size: 0.85rem; margin-top: 60px; padding: 20px; }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 3. Kết nối API
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Chưa cấu hình API Key!")
    st.stop()

# 4. Quản lý Đăng nhập
if "logged" not in st.session_state: st.session_state.logged = False

if not st.session_state.logged:
    # --- MÀN HÌNH CHÀO (GIỐNG MẪU TÂY NINH) ---
    st.markdown('<div class="robot-container">', unsafe_allow_html=True)
    # Nếu Phát có file robot.png trên GitHub thì dùng dòng dưới, không thì dùng link tạm này
    st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=180) 
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">Trợ lý ảo</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="main-title" style="font-size: 1.8rem;">Công đoàn Hòa Khánh</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        # Giới thiệu tính năng dạng Card
        st.markdown('''
            <div class="feature-card">
                <div class="feature-icon" style="color: #ffcc00;"><i class="fas fa-file-alt"></i></div>
                <div><b>Hỗ trợ nghiệp vụ</b><br><span style="font-size:0.8rem; color:#777;">Tra cứu hồ sơ, chính sách Công đoàn</span></div>
            </div>
            <div class="feature-card">
                <div class="feature-icon" style="color: #28a745;"><i class="fas fa-robot"></i></div>
                <div><b>Tư vấn 24/7</b><br><span style="font-size:0.8rem; color:#777;">Giải đáp thắc mắc bằng trí tuệ nhân tạo</span></div>
            </div>
        ''', unsafe_allow_html=True)

        name = st.text_input("Định danh Cán bộ/Đoàn viên:", placeholder="Nhập họ và tên...")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
            else:
                st.warning("Vui lòng nhập tên để tiếp tục!")

else:
    # --- GIAO DIỆN CHAT ---
    with st.sidebar:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        st.image("logo.png", width=100) # Logo Công đoàn
        st.markdown(f"<p class='sidebar-text'>Phiên làm việc:<br><b>{st.session_state.user}</b></p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🗑️ XÓA DỮ LIỆU CHAT"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown(f"<p class='sidebar-text' style='margin-top:150px; opacity:0.6;'>Thiết kế: <b>Lương Tấn Phát</b><br>Dự án Chuyển đổi số</p>", unsafe_allow_html=True)

    st.markdown(f"<h4 style='color: #004494;'><i class='fas fa-robot'></i> Chào Anh/Chị {st.session_state.user}, tôi có thể giúp gì?</h4>", unsafe_allow_html=True)

    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Hỏi Trợ lý ảo về hồ sơ, quy trình..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                res = client.chat.completions.create(
                    messages=[{"role": "system", "content": f"Bạn là trợ lý ảo Công đoàn Hòa Khánh. Gọi người dùng là Anh/Chị {st.session_state.user}."},
                              {"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except: st.error("AI đang bận!")

# 5. Chân trang
st.markdown(f'''
    <div class="footer">
        2026 © Sản phẩm của <b>Lương Tấn Phát</b><br>
        <span style="color:#004494; font-weight:bold;">CÔNG ĐOÀN XÃ HÒA KHÁNH</span>
    </div>
''', unsafe_allow_html=True)
