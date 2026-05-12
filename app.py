import streamlit as st
from groq import Groq
from docx import Document
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="robot.png", layout="wide")

# 2. CSS "VÀNG" - ÉP TÂM TUYỆT ĐỐI
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    /* Nền gradient hiện đại */
    .stApp { background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%); }

    /* Cấu trúc ép mọi thứ vào giữa màn hình */
    .st-emotion-cache-1jicfl2 { width: 100% !important; padding: 0 !important; }
    
    .main-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        min-height: 80vh;
        width: 100%;
    }

    /* Thẻ Card đăng nhập xịn */
    .login-card {
        background: #ffffff;
        padding: 45px;
        border-radius: 30px;
        box-shadow: 0 20px 50px rgba(0, 68, 148, 0.15);
        border: 1px solid #ffffff;
        max-width: 500px;
        width: 90%;
        margin: 0 auto;
    }

    /* Robot căn giữa và bay nhấp nhô */
    .robot-container {
        margin-bottom: -20px;
        z-index: 100;
        animation: float 3s ease-in-out infinite;
        display: flex;
        justify-content: center;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }

    /* Nút bấm Blue Neon */
    div.stButton > button {
        background: linear-gradient(90deg, #004494 0%, #0066cc 100%) !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        height: 55px !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 18px !important;
        box-shadow: 0 10px 20px rgba(0, 68, 148, 0.2);
        transition: 0.3s;
    }
    div.stButton > button:hover { transform: scale(1.03); box-shadow: 0 15px 25px rgba(0, 68, 148, 0.3); }

    /* Sidebar và Footer */
    [data-testid="stSidebar"] { background: #004494 !important; }
    .sidebar-text { color: white !important; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 3. Hàm nạp dữ liệu
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
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 4. Quản lý trạng thái
if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

# 5. GIAO DIỆN ĐĂNG NHẬP (ÉP GIỮA)
if not st.session_state.logged:
    # Sử dụng HTML wrapper để chắc chắn căn giữa
    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
    
    # Robot bay ở trên
    st.markdown('<div class="robot-container">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=220)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bảng Card ở dưới
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h1 style='color: #004494; font-size: 2.2rem; margin-bottom: 0;'>HÒA KHÁNH DIGITAL AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; font-weight: 500; margin-top: 10px; margin-bottom: 30px;'>Hệ thống Trợ lý số phục vụ Công đoàn cơ sở</p>", unsafe_allow_html=True)
    
    name = st.text_input("Nhập họ tên của Anh/Chị:", placeholder="Ví dụ: Nguyễn Thị Lan", label_visibility="collapsed")
    
    if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
        if name:
            st.session_state.user = name
            st.session_state.logged = True
            st.rerun()
        else:
            st.warning("Vui lòng nhập họ tên để định danh!")

    st.markdown(f"<p style='font-size: 0.8rem; color: #999; margin-top: 40px;'>Xây dựng và vận hành bởi: <br><b>Lương Tấn Phát</b></p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Đóng card
    st.markdown('</div>', unsafe_allow_html=True) # Đóng wrapper

else:
    # 6. GIAO DIỆN CHAT (SIDEBAR)
    with st.sidebar:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=120)
        st.markdown(f"<p class='sidebar-text' style='font-size: 1.1rem;'>Chào: <b>{st.session_state.user}</b></p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        
        # Nút hỏi nhanh
        if st.button("📩 Phản ánh kiến nghị"):
            st.session_state.messages.append({"role": "user", "content": "Quy trình tiếp nhận phản ánh kiến nghị"})
            st.rerun()
        if st.button("📝 Đăng ký Công đoàn"):
            st.session_state.messages.append({"role": "user", "content": "Cho tôi mẫu đơn gia nhập công đoàn"})
            st.rerun()
        if st.button("🗑️ Xóa hội thoại"):
            st.session_state.messages = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Hiển thị Chat
    st.markdown(f"<h3 style='color: #004494;'>🤖 Trợ lý AI xã Hòa Khánh sẵn sàng!</h3>", unsafe_allow_html=True)
    
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and "đơn gia nhập" in msg["content"].lower():
                target = "MAU 02- MẪU 5a+5b ĐƠN XIN GIA NHẬP CÔNG ĐOÀN.docx"
                if target in all_files:
                    with open(all_files[target], "rb") as f:
                        st.download_button(label="📥 Tải Mẫu đơn 02 (Word)", data=f, file_name=target, key=f"dl_{idx}")

    if prompt := st.chat_input("Hỏi tôi về nghiệp vụ công đoàn..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            try:
                res = client.chat.completions.create(
                    messages=[{"role": "system", "content": f"Bạn là trợ lý AI công đoàn xã Hòa Khánh. Dùng dữ liệu {knowledge_context[:10000]}."},
                              {"role": "user", "content": st.session_state.messages[-1]["content"]}],
                    model="llama-3.1-8b-instant")
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                st.rerun()
            except: st.error("Lỗi AI!")

st.markdown(f'<div style="text-align:center; color:#888; font-size:0.8rem; margin-top:30px;">Tác giả: <b>Lương Tấn Phát</b> | Dự án Chuyển đổi số cơ sở</div>', unsafe_allow_html=True)
