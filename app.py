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

# --- 2. CSS SIÊU CÔNG NGHỆ (ĐÃ FIX CHỮ NÚT BẤM & CARD) ---
st.markdown('''
<style>
    /* Nền tổng thể */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%);
    }

    /* Tùy chỉnh Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #002B5B 0%, #001524 100%) !important;
        box-shadow: 4px 0px 15px rgba(0,0,0,0.1);
    }
    
    .sidebar-content {
        padding: 20px;
        text-align: center;
    }

    /* Card Đăng nhập xịn mịn */
    .login-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.5);
        text-align: center;
        backdrop-filter: blur(10px);
    }

    /* Hiệu ứng Floating cho Robot */
    .robot-container {
        display: flex;
        justify-content: center;
        padding-bottom: 20px;
    }
    .floating { 
        animation: float 3.5s ease-in-out infinite; 
        width: 150px;
        filter: drop-shadow(0 10px 15px rgba(0,0,0,0.2));
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    /* CHỈNH LẠI NÚT KÍCH HOẠT ĐỂ THẤY CHỮ RÕ RÀNG */
    div.stButton > button {
        background: #0047AB !important; /* Màu xanh đậm làm nền chủ đạo */
        background: linear-gradient(90deg, #0047AB 0%, #0072ff 100%) !important;
        color: #FFFFFF !important; /* Ép chữ thành màu TRẮNG tuyệt đối */
        font-weight: 800 !important; /* Làm chữ đậm hơn */
        font-size: 1.2rem !important; /* Chữ to rõ */
        text-transform: uppercase !important; /* Chữ in hoa */
        letter-spacing: 1px !important;
        border-radius: 15px !important;
        border: none !important;
        padding: 15px 30px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(0, 71, 171, 0.4) !important;
        transition: all 0.3s ease !important;
        opacity: 1 !important; /* Đảm bảo không bị mờ */
    }
    
    div.stButton > button:hover {
        background: #003399 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 71, 171, 0.6) !important;
        color: #FFFFFF !important;
    }

    /* Chat bubble */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .gradient-text {
        background: -webkit-linear-gradient(#002B5B, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 2.2rem;
    }
</style>
''', unsafe_allow_html=True)

# --- 3. KHỞI TẠO CLIENT & SESSION STATE ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Vui lòng cấu hình GROQ_API_KEY trong Secrets!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "logged" not in st.session_state:
    st.session_state.logged = False

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- 5. GIAO DIỆN MÀN HÌNH CHÀO (FIXED) ---
if not st.session_state.logged:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 2, 1])
    
    with col_mid:
        # Bọc toàn bộ vào Card để robot và nút nằm chung một khối sạch sẽ
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown(f'''
            <div class="robot-container">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" class="floating">
            </div>
            <h1 class="gradient-text">HÒA KHÁNH DIGITAL AI</h1>
            <p style="color:#555; margin-bottom: 2rem;">Hệ thống trí tuệ nhân tạo hỗ trợ công tác Công đoàn</p>
        ''', unsafe_allow_html=True)
        
        name = st.text_input("👤 Định danh của bạn:", placeholder="Ví dụ: Nguyễn Văn A...", key="login_name")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
            else:
                st.warning("Vui lòng nhập định danh để tiếp tục!")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; margin-top:2rem; font-size:0.8rem; color:#888;'>© 2024 Dự án Chuyển đổi số - Hòa Khánh Digital</p>", unsafe_allow_html=True)

# --- 6. GIAO DIỆN CHÍNH (SAU KHI ĐĂNG NHẬP) ---
else:
    with st.sidebar:
        st.markdown(f'''
            <div class="sidebar-content">
                <div class="robot-container">
                    <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="80">
                </div>
                <h3 style="color:white; margin-bottom:0;">{st.session_state.user}</h3>
                <p style="color:#00d4ff; font-size:0.8rem;">Cán bộ đang truy cập</p>
            </div>
            <hr style="opacity:0.2; margin:10px 0;">
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

    # Khung chat chính
    st.markdown(f"### <span class='gradient-text' style='font-size:1.8rem;'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)
    st.write("Tôi có thể giúp gì cho Anh/Chị trong công tác Công đoàn hôm nay?")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
        add_message("user", prompt)
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": f"Bạn là trợ lý AI công đoàn xã Hòa Khánh. Hãy trả lời chuyên nghiệp, thân thiện. Gọi người dùng là Anh/Chị {st.session_state.user}."},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    stream=True,
                )
                for chunk in completion:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                add_message("assistant", full_response)
            except Exception as e:
                st.error(f"Lỗi: {str(e)}")
