import streamlit as st
from groq import Groq
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="logo.png", layout="wide")

# 2. CSS CĂN GIỮA TUYỆT ĐỐI
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    /* Nền gradient công nghệ */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Sidebar Glassmorphism & Căn giữa nội dung */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #004494 0%, #001a35 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Ép tất cả widget trong sidebar ra giữa */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        align-items: center !important;
        text-align: center !important;
    }

    /* Khung đăng nhập căn giữa màn hình */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        max-width: 600px;
        margin: 0 auto;
        text-align: center;
    }

    .login-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 35px;
        border-radius: 30px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        width: 100%;
        border: 1px solid #ffffff;
    }

    /* Hiệu ứng Robot bay căn giữa */
    .robot-box {
        display: flex;
        justify-content: center;
        width: 100%;
        margin-bottom: 10px;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    /* Nút bấm Neon Blue */
    div.stButton > button {
        background: linear-gradient(90deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%) !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        height: 50px !important;
        width: 100% !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(0, 82, 212, 0.4);
    }

    .sidebar-text { color: #e0e0e0 !important; }
    .digital-footer { text-align: center; color: #5d6d7e; font-size: 0.85rem; margin-top: 50px; padding: 20px; border-top: 1px solid rgba(0,0,0,0.05); }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 3. Kết nối API
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Lỗi: Thiếu API Key trong Secrets!")
    st.stop()

# 4. Quản lý trạng thái
if "logged" not in st.session_state: st.session_state.logged = False

if not st.session_state.logged:
    # --- MÀN HÌNH CHÀO CĂN GIỮA ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Dùng container để bọc mọi thứ vào giữa cột trung tâm
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # 1. Robot ở trên cùng
        st.markdown('<div class="robot-box">', unsafe_allow_html=True)
        st.image("robot.png", width=200)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 2. Bảng đăng nhập ở dưới
        st.markdown('''
        <div class="login-card">
            <h1 style='color: #004494; margin-bottom:5px;'>HÒA KHÁNH DIGITAL AI</h1>
            <p style="color: #666; font-weight: bold; margin-bottom: 20px;">Hệ thống Trợ lý số phục vụ Công đoàn & Chuyển đổi số</p>
        ''', unsafe_allow_html=True)
        
        name = st.text_input("Định danh Cán bộ/Đoàn viên:", placeholder="Nhập họ tên tại đây...", label_visibility="collapsed")
        
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
            else:
                st.warning("Vui lòng nhập tên!")
        
        st.markdown(f'''
            <p style="font-size: 0.85rem; color: #888; margin-top: 20px;">Phát triển bởi: <b>Lương Tấn Phát</b></p>
        </div>''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- GIAO DIỆN CHAT ---
    with st.sidebar:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        st.markdown('<div class="robot-box" style="margin-bottom: 0px;">', unsafe_allow_html=True)
        st.image("robot.png", width=110)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'''
            <div style="margin-top: 10px;">
                <p class='sidebar-text' style='margin-bottom: 5px; opacity: 0.8;'>Cán bộ truy cập:</p>
                <b style='font-size: 1.2rem; color: #00d4ff;'>{st.session_state.user}</b>
            </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 25px 0;'>", unsafe_allow_html=True)
        
        if st.button("XÓA DỮ LIỆU PHIÊN"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown(f'''
            <div style="margin-top: 80px; opacity: 0.8;">
                <i class="fas fa-code" style="color: white; font-size: 18px;"></i>
                <p class='sidebar-text' style='font-size:0.75rem; margin-top: 10px;'>
                    Tác giả: <b>Lương Tấn Phát</b><br>
                    Dự án Chuyển đổi số cơ sở
                </p>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<h3 style='color: #004494;'><i class='fas fa-robot'></i> Chào Anh/Chị {st.session_state.user}, AI đã sẵn sàng!</h3>", unsafe_allow_html=True)

    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Nhập nội dung cần hỗ trợ..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                res = client.chat.completions.create(
                    messages=[{"role": "system", "content": f"Bạn là trợ lý AI công đoàn xã Hòa Khánh. Gọi người dùng là Anh/Chị {st.session_state.user}."},
                              {"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant"
                )
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except: st.error("AI đang bận!")

# --- 5. CHÂN TRANG ---
st.markdown(f'''
    <div class="digital-footer">
        <i class="fas fa-microchip"></i> Dự án Số hóa Công đoàn & Hành chính công<br>
        Tác giả: <b>Lương Tấn Phát</b> | Xã Hòa Khánh, Tây Ninh
    </div>
''', unsafe_allow_html=True)
