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

# --- 2. CSS "ÉP" HIỆN NÚT MENU TRÊN ĐIỆN THOẠI ---
st.markdown('''
<style>
    /* Nền tổng thể */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%);
    }

    /* ÉP HIỆN NÚT SIDEBAR TRÊN MOBILE VÀ ĐỔI MÀU CHO RÕ */
    /* Đoạn này sẽ biến cái nút vốn bị ẩn thành một nút xanh nổi bật */
    [data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        background-color: #0047AB !important; /* Màu xanh đậm */
        border-radius: 0 10px 10px 0 !important;
        left: 0 !important;
        top: 10px !important;
        width: 60px !important;
        height: 45px !important;
        z-index: 999999 !important;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2) !important;
    }
    
    /* Làm cho biểu tượng mũi tên/menu bên trong màu trắng to rõ */
    [data-testid="stSidebarCollapsedControl"] svg {
        fill: white !important;
        color: white !important;
        width: 35px !important;
        height: 35px !important;
    }

    /* Style Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #002B5B 0%, #001524 100%) !important;
    }

    /* Style cho các nút Nhiệm vụ nhanh trong Sidebar */
    div.stButton > button {
        background: linear-gradient(90deg, #0047AB 0%, #0072ff 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        opacity: 1 !important;
        text-transform: uppercase !important;
    }

    .gradient-text {
        background: -webkit-linear-gradient(#004494, #00d4ff);
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

# --- 4. GIAO DIỆN CHÀO ---
if not st.session_state.logged:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div style="text-align:center;"><img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="150"></div>', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#004494;'>HÒA KHÁNH DIGITAL AI</h2>", unsafe_allow_html=True)
        name = st.text_input("👤 Định danh của bạn:", placeholder="Nhập tên...")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()

# --- 5. GIAO DIỆN CHÍNH ---
else:
    with st.sidebar:
        st.markdown(f'''
            <div style="text-align:center; padding:10px;">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="80">
                <h3 style="color:white; margin-bottom:0;">{st.session_state.user}</h3>
                <p style="color:#00d4ff; font-size:0.8rem;">Cán bộ đang trực tuyến</p>
            </div>
            <hr style="opacity:0.2;">
        ''', unsafe_allow_html=True)

        st.markdown("<p style='color:white; font-size:0.7rem; opacity:0.6; margin-left:10px;'>NHIỆM VỤ NHANH</p>", unsafe_allow_html=True)
        
        suggestions = {
            "📩 Phản ánh kiến nghị": "Tôi muốn gửi một phản ánh kiến nghị công việc.",
            "🆘 Yêu cầu hỗ trợ": "Hướng dẫn tôi cách yêu cầu hỗ trợ kỹ thuật.",
            "📝 Đăng ký Công đoàn": "Cho tôi hỏi thủ tục đăng ký tham gia công đoàn.",
            "📜 Quy định chính sách": "Các chính sách mới nhất cho công đoàn viên là gì?"
        }

        for label, prompt_text in suggestions.items():
            if st.button(label):
                add_message("user", prompt_text)
                st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🗑️ Làm mới phiên chat"):
            st.session_state.messages = []
            st.rerun()

    # Chat chính
    st.markdown(f"### <span class='gradient-text'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
        add_message("user", prompt)
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_res = ""
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Bạn là trợ lý AI công đoàn xã Hòa Khánh."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=True,
            )
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
            add_message("assistant", full_res)
