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

# --- 2. CSS SIÊU CÔNG NGHỆ (FIX LỖI GIAO DIỆN) ---
st.markdown('''
<style>
    /* Nền tổng thể chuyên nghiệp */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #f0f2f6 0%, #e0e5ec 100%);
    }

    /* Tùy chỉnh Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #002B5B 0%, #001524 100%) !important;
        box-shadow: 4px 0px 15px rgba(0,0,0,0.1);
    }
    
    /* Login Card - Đã sửa để bao phủ toàn bộ nội dung */
    .login-card {
        background: rgba(255, 255, 255, 0.85);
        padding: 35px;
        border-radius: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.4);
        text-align: center;
        backdrop-filter: blur(12px);
        margin-top: 20px;
    }

    /* Hiệu ứng Floating cho Robot */
    .robot-container {
        display: flex;
        justify-content: center;
        margin-bottom: 10px;
    }
    .floating { 
        animation: float 3.5s ease-in-out infinite; 
        width: 150px;
        filter: drop-shadow(0 15px 15px rgba(0,0,0,0.1));
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    /* NÚT BẤM KÍCH HOẠT - Chữ trắng trên nền xanh đậm cực nét */
    .stButton > button {
        background: linear-gradient(90deg, #004494 0%, #0072ff 100%) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.7rem 2rem !important;
        box-shadow: 0 4px 15px rgba(0, 68, 148, 0.3) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 68, 148, 0.5) !important;
        color: #ffffff !important;
    }

    /* Tiêu đề gradient mạnh mẽ */
    .gradient-text {
        background: -webkit-linear-gradient(#002B5B, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.2rem;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    /* Ẩn Header/Footer mặc định của Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    [data-testid="stHeader"] {background-color: rgba(0,0,0,0);}
</style>
''', unsafe_allow_html=True)

# --- 3. KHỞI TẠO SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "logged" not in st.session_state:
    st.session_state.logged = False

# Kết nối API Groq
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Vui lòng cấu hình GROQ_API_KEY trong Secrets!")
    st.stop()

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- 4. GIAO DIỆN MÀN HÌNH CHÀO (FIXED VERSION) ---
if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 1.8, 1])
    
    with col_mid:
        # Mở thẻ DIV Card trước khi vẽ Robot
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        st.markdown(f'''
            <div class="robot-container">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" class="floating">
            </div>
            <h1 class="gradient-text">HÒA KHÁNH DIGITAL AI</h1>
            <p style="color:#555; font-weight:500;">Trợ lý ảo hỗ trợ công tác Công đoàn</p>
            <br>
        ''', unsafe_allow_html=True)
        
        name = st.text_input("👤 Định danh Cán bộ / Đoàn viên:", placeholder="Nhập tên của bạn...")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
            else:
                st.warning("Vui lòng nhập định danh để tiếp tục!")
        
        # Đóng thẻ DIV Card
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; margin-top:2rem; font-size:0.75rem; color:#aaa;'>© 2024 Dự án Chuyển đổi số - Hòa Khánh Digital</p>", unsafe_allow_html=True)

# --- 5. GIAO DIỆN CHAT AI CHÍNH ---
else:
    # Sidebar chuyên nghiệp
    with st.sidebar:
        st.markdown(f'''
            <div style="text-align:center; padding:10px;">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="90">
                <h3 style="color:white; margin-top:10px;">{st.session_state.user}</h3>
                <p style="color:#00d4ff; font-size:0.8rem;">Cán bộ đang trực tuyến</p>
            </div>
            <hr style="opacity:0.2;">
        ''', unsafe_allow_html=True)

        st.markdown("<p style='color:gray; font-size:0.7rem; margin-left:10px;'>NHIỆM VỤ NHANH</p>", unsafe_allow_html=True)
        
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

    # Khu vực chat chính
    st.markdown(f"### <span class='gradient-text' style='font-size:1.6rem;'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)
    st.write("Tôi là Trợ lý AI, tôi có thể giúp gì cho Anh/Chị?")

    # Hiển thị lịch sử chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Nhận câu hỏi
    if prompt := st.chat_input("Gửi tin nhắn cho AI..."):
        add_message("user", prompt)
        st.rerun()

    # Xử lý phản hồi AI (Streaming)
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
                st.error("Lỗi kết nối API. Vui lòng kiểm tra Groq Key.")
