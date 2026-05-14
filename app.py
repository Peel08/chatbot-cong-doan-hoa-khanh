import streamlit as st
from groq import Groq
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Hòa Khánh Digital AI", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS SIÊU CÔNG NGHỆ (FIX MOBILE & BUTTON) ---
st.markdown('''
<style>
    .stApp {
        background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #002B5B 0%, #001524 100%) !important;
    }

    /* NÚT KÍCH HOẠT & NHIỆM VỤ NHANH - ÉP CHỮ TRẮNG RÕ NÉT */
    div.stButton > button {
        background: linear-gradient(90deg, #0047AB 0%, #0072ff 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        width: 100% !important;
        opacity: 1 !important;
        box-shadow: 0 4px 12px rgba(0, 71, 171, 0.3) !important;
    }

    /* Tiêu đề gradient */
    .gradient-text {
        background: -webkit-linear-gradient(#004494, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }

    .robot-container {
        display: flex;
        justify-content: center;
        padding: 10px 0;
    }
    .floating { 
        animation: float 3.5s ease-in-out infinite; 
        width: 120px;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# --- 3. KHỞI TẠO ---
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
        st.markdown('<div style="text-align:center;"><img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" class="floating"></div>', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#004494;'>HÒA KHÁNH DIGITAL AI</h2>", unsafe_allow_html=True)
        name = st.text_input("👤 Định danh của bạn:", placeholder="Nhập tên...")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()

# --- 5. GIAO DIỆN CHAT ---
else:
    # Sidebar vẫn giữ để làm sạch phiên
    with st.sidebar:
        st.markdown(f"<h3 style='color:white; text-align:center;'>{st.session_state.user}</h3>", unsafe_allow_html=True)
        if st.button("🗑️ Làm mới hội thoại"):
            st.session_state.messages = []
            st.rerun()

    st.markdown(f"### <span class='gradient-text'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)

    # NẾU CHƯA CÓ TIN NHẮN -> HIỆN NHIỆM VỤ NHANH RA GIỮA MÀN HÌNH (CHO ĐIỆN THOẠI)
    if len(st.session_state.messages) == 0:
        st.write("Chọn một nhiệm vụ dưới đây để bắt đầu nhanh:")
        
        # Chia cột để các nút nằm gọn đẹp
        c1, c2 = st.columns(2)
        
        quick_tasks = [
            ("📩 Phản ánh kiến nghị", "Tôi muốn gửi một phản ánh kiến nghị công việc."),
            ("🆘 Yêu cầu hỗ trợ", "Hướng dẫn tôi cách yêu cầu hỗ trợ kỹ thuật."),
            ("📝 Đăng ký Công đoàn", "Cho tôi hỏi thủ tục đăng ký tham gia công đoàn."),
            ("📜 Quy định chính sách", "Các chính sách mới nhất cho công đoàn viên là gì?")
        ]

        for i, (label, task_text) in enumerate(quick_tasks):
            with (c1 if i % 2 == 0 else c2):
                if st.button(label, key=f"quick_{i}"):
                    add_message("user", task_text)
                    st.rerun()
    
    # Hiển thị lịch sử chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Ô nhập liệu
    if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
        add_message("user", prompt)
        st.rerun()

    # Xử lý AI
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
            except Exception as e:
                st.error("Lỗi kết nối AI!")
