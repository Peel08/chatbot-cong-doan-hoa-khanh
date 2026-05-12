import streamlit as st
from groq import Groq
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="robot.png", layout="wide")

# 2. CSS Siêu Công Nghệ & Tối ưu Sidebar
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #004494 0%, #001a35 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        align-items: center !important;
        text-align: center !important;
    }

    /* Nút đề xuất tìm kiếm (Quick Actions) */
    .stButton > button {
        background: linear-gradient(90deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%) !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        font-size: 0.85rem !important;
        width: 100% !important;
        margin-bottom: 5px;
        transition: 0.3s;
    }
    .stButton > button:hover { transform: scale(1.03); }

    /* Nút Xóa dữ liệu (màu khác biệt) */
    .delete-btn > div > button {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    .sidebar-text { color: #e0e0e0 !important; }
    .robot-box { animation: float 3s ease-in-out infinite; display: flex; justify-content: center; width: 100%; }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
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
if "messages" not in st.session_state: st.session_state.messages = []

# Hàm để xử lý khi nhấn nút đề xuất
def send_suggestion(text):
    st.session_state.messages.append({"role": "user", "content": text})
    # Ở đây có thể gọi API ngay hoặc để Streamlit rerun để hiện tin nhắn

if not st.session_state.logged:
    # --- MÀN HÌNH CHÀO ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
    with col2:
        st.markdown('<div style="text-align:center;" class="robot-box"><img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="200"></div>', unsafe_allow_html=True)
        name = st.text_input("Định danh Cán bộ/Đoàn viên:", placeholder="Nhập tên...")
        if st.button("🚀 KÍCH HOẠT"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()

else:
    # --- GIAO DIỆN CHAT AI ---
    with st.sidebar:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        st.markdown('<div class="robot-box"><img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="110"></div>', unsafe_allow_html=True)
        
        st.markdown(f"<p class='sidebar-text'>Cán bộ truy cập:<br><b style='font-size:1.1rem; color:#00d4ff;'>{st.session_state.user}</b></p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        # --- MỤC ĐỀ XUẤT TÌM KIẾM (MỚI) ---
        st.markdown("<p class='sidebar-text' style='font-size:0.8rem; opacity:0.7;'>ĐỀ XUẤT NHANH:</p>", unsafe_allow_html=True)
        
        if st.button("📩 Phản ánh kiến nghị"):
            st.session_state.messages.append({"role": "user", "content": "Tôi muốn phản ánh kiến nghị"})
            st.rerun()
            
        if st.button("🆘 Yêu cầu hỗ trợ"):
            st.session_state.messages.append({"role": "user", "content": "Tôi cần hỗ trợ kỹ thuật"})
            st.rerun()
            
        if st.button("📝 Đăng ký Công đoàn"):
            st.session_state.messages.append({"role": "user", "content": "Hướng dẫn đăng ký tham gia công đoàn"})
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Nút xóa phiên
        st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
        if st.button("🗑️ XÓA DỮ LIỆU PHIÊN"):
            st.session_state.messages = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'''<div style="margin-top:50px; opacity:0.8;"><i class="fas fa-code" style="color:white;"></i><p class='sidebar-text' style='font-size:0.7rem;'>Tác giả: <b>Lương Tấn Phát</b><br>Dự án Chuyển đổi số</p></div>''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Khung Chat chính
    st.markdown(f"<h4 style='color:#004494;'>Chào {st.session_state.user}, Trợ lý AI sẵn sàng!</h4>", unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    # Xử lý nhập liệu hoặc từ nút bấm đề xuất
    if prompt := st.chat_input("Nhập câu hỏi..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # Tự động phản hồi AI khi có tin nhắn mới từ User
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            try:
                user_msg = st.session_state.messages[-1]["content"]
                res = client.chat.completions.create(
                    messages=[{"role": "system", "content": f"Bạn là trợ lý AI công đoàn xã Hòa Khánh. Gọi người dùng là Anh/Chị {st.session_state.user}."},
                              {"role": "user", "content": user_msg}],
                    model="llama-3.1-8b-instant")
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except: st.error("Lỗi kết nối!")
