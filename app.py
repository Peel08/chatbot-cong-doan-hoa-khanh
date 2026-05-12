import streamlit as st
from groq import Groq
from docx import Document
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="robot.png", layout="wide")

# 2. CSS "SIÊU CĂN TÂM" - Đảm bảo cân đối trên mọi màn hình
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    /* Nền sáng công nghệ */
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #d6e4f0 100%); }

    /* Ép toàn bộ khối đăng nhập ra giữa màn hình */
    .main-login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding-top: 50px;
    }

    /* Thẻ Card trắng chứa nội dung */
    .login-card {
        background: #ffffff;
        padding: 40px;
        border-radius: 25px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.08);
        text-align: center;
        width: 100%;
        max-width: 500px;
        border: 1px solid #e1e8ed;
    }

    /* Hiệu ứng Robot bay căn giữa */
    .robot-box {
        margin-bottom: 25px;
        animation: float 3.5s ease-in-out infinite;
        display: flex;
        justify-content: center;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }

    /* Nút bấm Neon Blue */
    div.stButton > button {
        background: linear-gradient(90deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%) !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        height: 50px !important;
        width: 100% !important;
        font-weight: bold !important;
        box-shadow: 0 5px 15px rgba(0, 82, 212, 0.3);
        margin-top: 15px;
    }

    /* Sidebar và các thành phần khác */
    [data-testid="stSidebar"] { background: #004494 !important; }
    .sidebar-text { color: #ffffff !important; text-align: center; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 3. Hàm nạp dữ liệu từ thư mục data
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

# 4. Logic Đăng nhập
if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

if not st.session_state.logged:
    # HIỂN THỊ MÀN HÌNH CHÀO CĂN GIỮA TUYỆT ĐỐI
    st.markdown('<div class="main-login-container">', unsafe_allow_html=True)
    
    # 1. Robot nằm trên
    st.markdown('<div class="robot-box">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=200)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 2. Card đăng nhập
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h1 style='color: #004494; font-size: 2rem; margin-bottom: 10px;'>HÒA KHÁNH DIGITAL AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #5d6d7e; font-weight: 500; margin-bottom: 25px;'>Trợ lý số phục vụ Công đoàn & Chuyển đổi số</p>", unsafe_allow_html=True)
    
    name = st.text_input("Định danh cán bộ:", placeholder="Nhập họ tên tại đây...", label_visibility="collapsed")
    
    if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
        if name:
            st.session_state.user = name
            st.session_state.logged = True
            st.rerun()
        else:
            st.warning("Vui lòng nhập tên!")
            
    st.markdown(f"<p style='font-size: 0.85rem; color: #aab8c2; margin-top: 30px;'>Phát triển bởi: <b>Lương Tấn Phát</b></p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Đóng login-card
    st.markdown('</div>', unsafe_allow_html=True) # Đóng main-login-container

else:
    # GIAO DIỆN CHAT CHÍNH
    with st.sidebar:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=110)
        st.markdown(f"<p class='sidebar-text' style='font-size: 1.1rem;'>Chào: <b>{st.session_state.user}</b></p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        
        if st.button("📩 Phản ánh kiến nghị"):
            st.session_state.messages.append({"role": "user", "content": "Quy trình tiếp nhận phản ánh kiến nghị"})
            st.rerun()
        if st.button("📝 Đăng ký Công đoàn"):
            st.session_state.messages.append({"role": "user", "content": "Cho tôi mẫu đơn gia nhập công đoàn"})
            st.rerun()
        if st.button("🗑️ XÓA PHIÊN CHAT"):
            st.session_state.messages = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Hiển thị hội thoại
    st.markdown(f"<h3 style='color: #004494;'>AI Hòa Khánh sẵn sàng!</h3>", unsafe_allow_html=True)
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and "đơn gia nhập" in msg["content"].lower():
                target = "MAU 02- MẪU 5a+5b ĐƠN XIN GIA NHẬP CÔNG ĐOÀN.docx"
                if target in all_files:
                    with open(all_files[target], "rb") as f:
                        st.download_button(label="📥 Tải Mẫu đơn 02 (Word)", data=f, file_name=target, key=f"dl_{idx}")

    if prompt := st.chat_input("Nhập câu hỏi..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            try:
                res = client.chat.completions.create(
                    messages=[{"role": "system", "content": f"Bạn là trợ lý công đoàn xã Hòa Khánh. Dùng dữ liệu {knowledge_context[:10000]}. Gọi là Anh/Chị {st.session_state.user}."},
                              {"role": "user", "content": st.session_state.messages[-1]["content"]}],
                    model="llama-3.1-8b-instant")
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                st.rerun()
            except: st.error("Lỗi AI!")
