import streamlit as st
from groq import Groq
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Công đoàn Hòa Khánh", page_icon="logo.png", layout="wide")

# 2. CSS "Sạch" - Đảm bảo không hiện chữ thừa
st.markdown('''
<style>
    /* Sidebar xanh đậm */
    [data-testid="stSidebar"] { background-color: #004494 !important; }
    .sidebar-text { color: white !important; text-align: center; font-size: 0.9rem; }
    
    /* Nút bấm bo tròn */
    div.stButton > button {
        background-color: #004494 !important;
        color: white !important;
        border-radius: 20px !important;
        width: 100% !important;
        font-weight: bold !important;
        height: 45px !important;
    }
    
    /* Chân trang tác giả */
    .author-footer {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        margin-top: 50px;
        padding: 20px;
        border-top: 1px solid #eee;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 3. Kết nối API
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Lỗi: Thiếu API Key trong mục Secrets!")
    st.stop()

# 4. Quản lý trạng thái
if "logged" not in st.session_state: st.session_state.logged = False

if not st.session_state.logged:
    # --- MÀN HÌNH CHÀO & TÁC GIẢ ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        st.image("logo.png", width=130)
        st.markdown("<h1 style='color: #004494; text-align:center;'>TRỢ LÝ ẢO CÔNG ĐOÀN</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>Xây dựng và vận hành bởi <b>Lương Tấn Phát</b></p>", unsafe_allow_html=True)
        
        name = st.text_input("Vui lòng nhập họ tên của Anh/Chị để bắt đầu:")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
            else:
                st.warning("Anh/Chị vui lòng nhập tên!")

else:
    # --- GIAO DIỆN CHAT & TÁC GIẢ SIDEBAR ---
    with st.sidebar:
        st.image("logo.png", width=100)
        st.markdown(f"<p class='sidebar-text'>Thành viên sử dụng:<br><b style='font-size:1.1rem;'>{st.session_state.user}</b></p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        
        if st.button("🗑️ XÓA HỘI THOẠI"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("🚪 ĐĂNG XUẤT"):
            st.session_state.logged = False
            st.rerun()
            
        st.markdown(f"<p class='sidebar-text' style='margin-top:100px; opacity:0.7;'>Thiết kế bởi:<br><b>Lương Tấn Phát</b></p>", unsafe_allow_html=True)

    st.markdown(f"<h4 style='color: #004494;'>Trợ lý Công đoàn xã Hòa Khánh xin chào Anh/Chị {st.session_state.user}</h4>", unsafe_allow_html=True)

    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            try:
                res = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"Bạn là trợ lý công đoàn xã Hòa Khánh. Gọi người dùng là Anh/Chị {st.session_state.user}. Trả lời lịch sự."},
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.1-8b-instant"
                )
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except:
                st.error("Lỗi kết nối AI!")

# --- 5. CHÂN TRANG TÁC GIẢ ---
st.markdown(f'<div class="author-footer">Hệ thống được phát triển bởi <b>Lương Tấn Phát</b><br>© 2026 Công đoàn xã Hòa Khánh, Tây Ninh</div>', unsafe_allow_html=True)
