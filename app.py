import streamlit as st
from groq import Groq
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Hòa Khánh Digital AI", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="collapsed" # Ẩn luôn sidebar cho rảnh nợ
)

# --- 2. CSS SIÊU CÔNG NGHỆ (FIX CHỮ NÚT & MOBILE) ---
st.markdown('''
<style>
    .stApp {
        background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%);
    }

    /* NÚT KÍCH HOẠT & NHIỆM VỤ NHANH - ÉP CHỮ TRẮNG TO RÕ */
    div.stButton > button {
        background: linear-gradient(90deg, #0047AB 0%, #0072ff 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 8px 15px !important;
        width: 100% !important;
        opacity: 1 !important;
        box-shadow: 0 4px 10px rgba(0, 71, 171, 0.2) !important;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 71, 171, 0.4) !important;
    }

    .gradient-text {
        background: -webkit-linear-gradient(#004494, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# --- 3. KHỞI TẠO CLIENT ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Thiếu API Key!")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
if "logged" not in st.session_state: st.session_state.logged = False

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- 4. MÀN HÌNH ĐĂNG NHẬP ---
if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align:center;"><img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="150" style="animation: float 3s ease-in-out infinite;"></div>', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#004494;'>HÒA KHÁNH DIGITAL AI</h2>", unsafe_allow_html=True)
        name = st.text_input("👤 Định danh của bạn:", placeholder="Nhập tên...")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()

# --- 5. GIAO DIỆN CHAT CHÍNH ---
else:
    # HIỆN MENU NHIỆM VỤ NHANH NGAY TRÊN ĐẦU (CHO CẢ MOBILE & PC)
    with st.container():
        st.markdown(f"### <span class='gradient-text'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)
        
        # Tạo lưới nút bấm 2x2 cho Mobile cực đẹp
        col_task1, col_task2 = st.columns(2)
        
        quick_tasks = [
            ("📩 Phản ánh", "Tôi muốn gửi một phản ánh kiến nghị công việc."),
            ("🆘 Hỗ trợ", "Hướng dẫn tôi cách yêu cầu hỗ trợ kỹ thuật."),
            ("📝 Đăng ký", "Cho tôi hỏi thủ tục đăng ký tham gia công đoàn."),
            ("🗑️ Làm mới", "CLEAR_SESSION")
        ]

        for i, (label, task_text) in enumerate(quick_tasks):
            with (col_task1 if i % 2 == 0 else col_task2):
                if st.button(label, key=f"q_{i}"):
                    if task_text == "CLEAR_SESSION":
                        st.session_state.messages = []
                        st.rerun()
                    else:
                        add_message("user", task_text)
                        st.session_state.run_ai = True
                        st.rerun()

    st.markdown("---") # Đường kẻ ngăn cách Menu và Chat

    # Hiển thị nội dung Chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Ô nhập liệu phía dưới
    if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
        add_message("user", prompt)
        st.rerun()

    # Xử lý phản hồi AI
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_res = ""
            try:
                stream = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": f"Bạn là trợ lý AI công đoàn xã Hòa Khánh. Gọi người dùng là Anh/Chị {st.session_state.user}."},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    stream=True
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_res += chunk.choices[0].delta.content
                        placeholder.markdown(full_res + "▌")
                placeholder.markdown(full_res)
                add_message("assistant", full_res)
            except:
                st.error("Lỗi kết nối!")
