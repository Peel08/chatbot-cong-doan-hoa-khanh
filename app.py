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

# --- 2. CSS SIÊU CÔNG NGHỆ (CUSTOM STYLE) ---
st.markdown('''
<style>
    /* Tổng thể nền */
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

    /* Hiệu ứng Floating cho Robot */
    .robot-container {
        display: flex;
        justify-content: center;
        padding: 20px 0;
    }
    .floating { 
        animation: float 3.5s ease-in-out infinite; 
        width: 120px;
        filter: drop-shadow(0 10px 15px rgba(0,0,0,0.2));
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    /* Style cho các nút bấm Đề xuất */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        text-align: left !important;
        padding: 10px 15px !important;
    }
    div.stButton > button:hover {
        background: rgba(0, 212, 255, 0.2) !important;
        border-color: #00d4ff !important;
        transform: translateX(5px);
    }

    /* Chat bubble tinh tế hơn */
    .stChatMessage {
        border-radius: 15px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
    }
    
    /* Ẩn Header/Footer thừa */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Tiêu đề gradient */
    .gradient-text {
        background: -webkit-linear-gradient(#004494, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
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

# --- 4. HÀM XỬ LÝ LOGIC ---
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- 5. GIAO DIỆN MÀN HÌNH CHÀO ---
if not st.session_state.logged:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f'''
            <div class="robot-container">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" class="floating">
            </div>
            <h2 style="text-align:center; color:#004494;">HÒA KHÁNH DIGITAL AI</h2>
            <p style="text-align:center; color:#666;">Trợ lý ảo thông minh dành cho Cán bộ & Đoàn viên</p>
        ''', unsafe_allow_html=True)
        
        name = st.text_input("👤 Định danh của bạn:", placeholder="Ví dụ: Nguyễn Văn A...")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG", use_container_width=True):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
            else:
                st.warning("Vui lòng nhập tên để tiếp tục!")

# --- 6. GIAO DIỆN CHÍNH (SAU KHI ĐĂNG NHẬP) ---
else:
    # Sidebar
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
                # Gán cờ để gọi AI ngay sau rerun
                st.session_state.run_ai = True 
                st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🗑️ Làm mới phiên chat"):
            st.session_state.messages = []
            st.rerun()

        st.markdown(f'''
            <div style="position: fixed; bottom: 20px; left: 20px; color: rgba(255,255,255,0.4); font-size: 0.7rem;">
                Phát triển bởi: <b>Lương Tấn Phát</b><br>
                Hòa Khánh Digital Project © 2024
            </div>
        ''', unsafe_allow_html=True)

    # Khung chat chính
    st.markdown(f"### <span class='gradient-text'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)
    st.write("Tôi có thể giúp gì cho Anh/Chị trong công tác Công đoàn hôm nay?")

    # Hiển thị lịch sử chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Xử lý Input từ người dùng
    if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
        add_message("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Gọi AI
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                # Tạo hiệu ứng streaming (chạy chữ)
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
                st.error(f"Hệ thống đang bận, vui lòng thử lại sau! (Lỗi: {str(e)})")
