import streamlit as st
from groq import Groq
import os

# 1. Cấu hình trang với Logo
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="logo.png", layout="wide")

# 2. CSS SIÊU CÔNG NGHỆ (AI & DIGITAL TRANSFORMATION)
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    /* Nền gradient công nghệ */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Sidebar phong cách Glassmorphism */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #004494 0%, #001a35 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    .sidebar-text { 
        color: #e0e0e0 !important; 
        text-align: center; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Nút bấm hiệu ứng Neon Blue */
    div.stButton > button {
        background: linear-gradient(90deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%) !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        height: 50px !important;
        width: 100% !important;
        font-weight: bold !important;
        transition: 0.3s all ease;
        box-shadow: 0 4px 15px rgba(0, 82, 212, 0.4);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 82, 212, 0.6);
    }

    /* Khung đăng nhập phong cách AI */
    .login-card {
        text-align: center;
        padding: 40px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid #fff;
    }

    /* Tin nhắn chat bo tròn hiện đại */
    .stChatMessage {
        border-radius: 20px !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
        background-color: white !important;
    }

    /* Chân trang chuyên nghiệp */
    .digital-footer {
        text-align: center;
        color: #5d6d7e;
        font-size: 0.85rem;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid rgba(0,0,0,0.05);
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 3. Kết nối API
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Lỗi: Thiếu API Key!")
    st.stop()

# 4. Quản lý trạng thái
if "logged" not in st.session_state: st.session_state.logged = False

if not st.session_state.logged:
    # --- MÀN HÌNH CHÀO DIGITAL ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        st.markdown('''
        <div class="login-card">
            <i class="fas fa-microchip" style="font-size: 50px; color: #004494; margin-bottom: 20px;"></i>
            <h1 style='color: #004494; font-family: sans-serif;'>HÒA KHÁNH DIGITAL AI</h1>
            <p style="color: #666;">Hệ thống Trợ lý số phục vụ Công đoàn & Chuyển đổi số cơ sở</p>
            <p style="font-size: 0.9rem;">Chuyên gia phát triển: <b>Lương Tấn Phát</b></p>
        </div>
        ''', unsafe_allow_html=True)
        
        name = st.text_input("Nhập danh tính Cán bộ/Đoàn viên:")
        if st.button("KÍCH HOẠT TRỢ LÝ SỐ"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
            else:
                st.warning("Vui lòng nhập tên để định danh hệ thống!")

else:
    # --- GIAO DIỆN CHAT AI ---
    with st.sidebar:
        st.markdown(f'''
            <div style="text-align:center;">
                <i class="fas fa-user-shield" style="font-size: 40px; color: white; margin-bottom: 15px;"></i>
                <p class='sidebar-text'>Cán bộ truy cập:<br><b style='font-size:1.2rem; color: #00d4ff;'>{st.session_state.user}</b></p>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        if st.button("XÓA DỮ LIỆU PHIÊN"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown(f'''
            <div style="margin-top: 100px; text-align:center; opacity: 0.8;">
                <i class="fas fa-code" style="color: white; font-size: 15px;"></i>
                <p class='sidebar-text' style='font-size:0.75rem;'>Phát triển bởi:<br><b>Lương Tấn Phát</b><br>IUH Student</p>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown(f"<h3 style='color: #004494;'><i class='fas fa-robot'></i> Chào Anh/Chị {st.session_state.user}, Trợ lý AI đã sẵn sàng!</h3>", unsafe_allow_html=True)

    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Nhập câu hỏi về Chuyển đổi số, Công đoàn..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                res = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"Bạn là trợ lý AI công đoàn xã Hòa Khánh. Hãy trả lời chuyên nghiệp, tích cực về chuyển đổi số. Gọi người dùng là Anh/Chị {st.session_state.user}."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.1-8b-instant"
                )
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except:
                st.error("Hệ thống AI đang quá tải, vui lòng đợi!")

# --- 5. CHÂN TRANG DIGITAL ---
st.markdown(f'''
    <div class="digital-footer">
        <i class="fas fa-project-diagram"></i> Dự án số hóa Công đoàn cơ sở<br>
        Tác giả: <b>Lương Tấn Phát</b> | Xã Hòa Khánh, Tây Ninh
    </div>
''', unsafe_allow_html=True)
