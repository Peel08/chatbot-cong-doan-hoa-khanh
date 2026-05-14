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

# --- 2. CSS PHỤC HỒI GIAO DIỆN SANG XỊN (FIX NÚT MENU MOBILE) ---
st.markdown('''
<style>
    /* Phục hồi nền Radial Gradient sang trọng */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%);
    }

    /* Sidebar Glassmorphism màu xanh đậm đặc trưng */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #002B5B 0%, #001524 100%) !important;
        box-shadow: 4px 0px 15px rgba(0,0,0,0.1);
    }
    
    /* ÉP HIỆN NÚT MENU TRÊN ĐIỆN THOẠI - PHƯƠNG PHÁP MỚI SIÊU NHẠY */
    /* Tạo một lớp phủ màu xanh ở góc trái để cán bộ biết chỗ bấm */
    [data-testid="stSidebarCollapsedControl"] {
        background-color: #0047AB !important;
        color: white !important;
        border-radius: 0 15px 15px 0 !important;
        width: 55px !important;
        height: 50px !important;
        left: 0px !important;
        top: 15px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        z-index: 1000000 !important;
        box-shadow: 3px 0 10px rgba(0,0,0,0.2) !important;
        visibility: visible !important;
    }
    
    /* Làm mũi tên/icon Menu to và trắng rõ */
    [data-testid="stSidebarCollapsedControl"] svg {
        fill: white !important;
        width: 30px !important;
        height: 30px !important;
    }

    /* FIX NÚT KÍCH HOẠT: Chữ trắng, nền xanh đậm, rõ nét 100% */
    div.stButton > button {
        background: linear-gradient(90deg, #0047AB 0%, #0072ff 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 10px 20px !important;
        width: 100% !important;
        opacity: 1 !important;
        box-shadow: 0 4px 15px rgba(0, 71, 171, 0.3) !important;
    }

    .robot-container {
        display: flex;
        justify-content: center;
        padding: 20px 0;
    }
    .floating { 
        animation: float 3.5s ease-in-out infinite; 
        width: 130px;
        filter: drop-shadow(0 10px 15px rgba(0,0,0,0.2));
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
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

# --- 3. KHỞI TẠO CLIENT & SESSION ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Cần GROQ_API_KEY trong Secrets!")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
if "logged" not in st.session_state: st.session_state.logged = False

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- 4. GIAO DIỆN MÀN HÌNH CHÀO ---
if not st.session_state.logged:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f'''
            <div class="robot-container">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" class="floating">
            </div>
            <h2 style="text-align:center; color:#004494;">HÒA KHÁNH DIGITAL AI</h2>
            <p style="text-align:center; color:#666;">Trợ lý ảo thông minh dành cho Cán bộ & Đoàn viên</p>
        ''', unsafe_allow_html=True)
        
        name = st.text_input("👤 Định danh của bạn:", placeholder="Nhập tên...")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()

# --- 5. GIAO DIỆN SIDEBAR (PHỤC HỒI NHIỆM VỤ NHANH) ---
else:
    with st.sidebar:
        st.markdown(f'''
            <div style="text-align:center; padding:20px;">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="90">
                <h3 style="color:white; margin-bottom:0;">{st.session_state.user}</h3>
                <p style="color:#00d4ff; font-size:0.8rem;">Cán bộ đang truy cập</p>
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

    # KHUNG CHAT CHÍNH
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
