import streamlit as st
from groq import Groq
from docx import Document
import os

# 1. CẤU HÌNH TRANG - ƯU TIÊN HIỂN THỊ
st.set_page_config(
    page_title="Hòa Khánh Digital AI", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. HỆ THỐNG CSS CAO CẤP (CUSTOM UI V3.0)
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;600;700&display=swap');

    /* Tổng thể ứng dụng */
    html, body, [class*="st-emotion-cache"] {
        font-family: 'Urbanist', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #eef2f7 0%, #dfe7f0 100%);
    }

    /* Ẩn Header & Footer mặc định */
    header, footer, #MainMenu {visibility: hidden;}

    /* SIDEBAR CHUYÊN NGHIỆP */
    [data-testid="stSidebar"] {
        background-color: #004494 !important;
        background-image: linear-gradient(180deg, #004494 0%, #002d62 100%) !important;
    }
    
    .sidebar-content {
        color: white;
        text-align: center;
        padding: 20px;
    }

    /* CARD ĐĂNG NHẬP GLASSMORPHISM */
    .login-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 85vh;
    }

    .login-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 50px;
        border-radius: 30px;
        box-shadow: 0 25px 45px rgba(0, 0, 0, 0.1);
        width: 100%;
        max-width: 480px;
        text-align: center;
    }

    /* HIỆU ỨNG ROBOT BAY */
    .floating-robot {
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 10px 15px rgba(0, 68, 148, 0.3));
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-25px) rotate(2deg); }
    }

    /* NÚT BẤM HIỆN ĐẠI */
    div.stButton > button {
        background: linear-gradient(90deg, #004494 0%, #00b4d8 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        border: none !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 180, 216, 0.4);
    }

    /* TÙY CHỈNH BONG BÓNG CHAT */
    [data-testid="stChatMessage"] {
        background-color: white !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
        border: 1px solid #eef2f7 !important;
    }

    /* Thanh Chat Input */
    .stChatInputContainer {
        padding: 1rem 3rem !important;
        background: transparent !important;
    }

    .stChatInputContainer > div {
        border-radius: 25px !important;
        border: 1px solid #004494 !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05) !important;
    }

    /* Badge tác giả */
    .author-badge {
        font-size: 0.85rem;
        color: #64748b;
        text-align: center;
        margin-top: 2rem;
        border-top: 1px solid #cbd5e1;
        padding-top: 1rem;
    }
</style>
''', unsafe_allow_html=True)

# 3. HÀM NẠP DỮ LIỆU (GIỮ NGUYÊN LOGIC CỦA BẠN)
@st.cache_resource
def load_data():
    knowledge = ""
    file_map = {}
    if os.path.exists("data"):
        for fn in os.listdir("data"):
            path = os.path.join("data", fn)
            file_map[fn] = path
            if fn.endswith((".docx", ".doc")):
                try:
                    doc = Document(path)
                    knowledge += f"\nFILE: {fn}\n" + "\n".join([p.text for p in doc.paragraphs])
                except: pass
    return knowledge, file_map

knowledge_context, all_files = load_data()

# 4. KHỞI TẠO GROQ
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Chưa cấu hình GROQ_API_KEY trong secrets!")

# 5. QUẢN LÝ TRẠNG THÁI
if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

# 6. GIAO DIỆN ĐĂNG NHẬP
if not st.session_state.logged:
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    
    # Robot Mascot
    st.markdown('<div class="floating-robot">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=200)
    st.markdown('</div>', unsafe_allow_html=True)

    # Login Card
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h1 style='color: #004494; font-size: 2rem; margin-bottom: 5px;'>HÒA KHÁNH AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #00b4d8; font-weight: 600; margin-bottom: 30px;'>TRỢ LÝ SỐ CÔNG ĐOÀN V3.0</p>", unsafe_allow_html=True)
    
    name = st.text_input("Username", placeholder="Nhập tên Anh/Chị để bắt đầu...", label_visibility="collapsed")
    
    if st.button("KÍCH HOẠT HỆ THỐNG"):
        if name:
            st.session_state.user = name
            st.session_state.logged = True
            st.rerun()
        else:
            st.warning("Vui lòng danh xưng để Robot phục vụ!")
    
    st.markdown(f'''
    <div class="author-badge">
        Phát triển bởi: <b>Lương Tấn Phát</b><br>
        <i>Chuyển đổi số Công đoàn xã Hòa Khánh</i>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

else:
    # 7. GIAO DIỆN CHAT CHÍNH
    with st.sidebar:
        st.markdown('<div style="text-align: center; padding: 20px 0;">', unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=120)
        st.markdown(f"<h3 style='color: white;'>{st.session_state.user}</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #00b4d8;'>Đã sẵn sàng hỗ trợ</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("<p style='color: white; font-weight: bold;'>TRUY CẬP NHANH</p>", unsafe_allow_html=True)
        
        if st.button("📝 Đơn Gia Nhập Công Đoàn"):
            st.session_state.messages.append({"role": "user", "content": "Cho tôi mẫu đơn gia nhập công đoàn"})
            st.rerun()
            
        if st.button("📩 Phản Ánh / Kiến Nghị"):
            st.session_state.messages.append({"role": "user", "content": "Quy trình gửi phản ánh kiến nghị"})
            st.rerun()

        if st.button("⚖️ Pháp Luật Lao Động"):
            st.session_state.messages.append({"role": "user", "content": "Tóm tắt quyền lợi người lao động"})
            st.rerun()
            
        st.markdown("---")
        if st.button("🗑️ Làm mới hội thoại"):
            st.session_state.messages = []
            st.rerun()

    # KHÔNG GIAN CHAT
    st.markdown(f"<h2 style='color: #004494;'><i class='fa-solid fa-robot'></i> Hòa Khánh Digital AI</h2>", unsafe_allow_html=True)
    
    # Render tin nhắn
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            # Xử lý hiển thị nút tải file nếu AI nhắc tới đơn gia nhập
            if msg["role"] == "assistant" and "đơn gia nhập" in msg["content"].lower():
                target = "MAU 02- MẪU 5a+5b ĐƠN XIN GIA NHẬP CÔNG ĐOÀN.docx"
                if target in all_files:
                    with open(all_files[target], "rb") as f:
                        st.download_button(
                            label=f"📥 Tải xuống: {target}", 
                            data=f, 
                            file_name=target, 
                            key=f"dl_{idx}"
                        )

    # Input người dùng
    if prompt := st.chat_input("Hãy hỏi tôi bất cứ điều gì về nghiệp vụ..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # Phản hồi từ AI
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Đang truy xuất dữ liệu xã..."):
                try:
                    # RAG đơn giản: Lấy 10k ký tự đầu của file làm ngữ cảnh
                    system_prompt = f"""Bạn là trợ lý AI công đoàn xã Hòa Khánh. 
                    Dùng dữ liệu sau để trả lời: {knowledge_context[:12000]}. 
                    Trả lời thân thiện, chuyên nghiệp bằng tiếng Việt."""
                    
                    res = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": st.session_state.messages[-1]["content"]}
                        ],
                        model="llama-3.1-8b-instant"
                    )
                    ans = res.choices[0].message.content
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi hệ thống: {e}")

    # Footer trang chat
    st.markdown(f'<div style="text-align:center; color:#94a3b8; font-size:0.8rem; margin-top:50px; padding-bottom: 20px;">Hệ thống hỗ trợ Công đoàn xã Hòa Khánh | Phiên bản 3.0</div>', unsafe_allow_html=True)
