import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="robot.png", layout="wide")

# 2. Hàm đọc dữ liệu từ các file Phát đã chuẩn bị
@st.cache_resource
def load_knowledge_base():
    combined_text = ""
    data_folder = "data" # Phát tạo thư mục tên 'data' trên GitHub và bỏ các file vào đó
    if os.path.exists(data_folder):
        for filename in os.listdir(data_folder):
            file_path = os.path.join(data_folder, filename)
            try:
                if filename.endswith(".pdf"):
                    reader = PdfReader(file_path)
                    for page in reader.pages:
                        combined_text += page.extract_text() + "\n"
                elif filename.endswith(".docx") or filename.endswith(".doc"):
                    doc = Document(file_path)
                    combined_text += "\n".join([para.text for para in doc.paragraphs]) + "\n"
            except Exception as e:
                print(f"Lỗi đọc file {filename}: {e}")
    return combined_text

# 3. CSS Giao diện (Giữ nguyên phong cách AI căn giữa)
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #004494 0%, #001a35 100%) !important; }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { align-items: center !important; text-align: center !important; }
    .sidebar-text { color: #e0e0e0 !important; }
    .stButton > button {
        background: linear-gradient(90deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%) !important;
        color: white !important;
        border-radius: 20px !important;
        width: 100% !important;
        margin-bottom: 5px;
        font-size: 0.85rem !important;
    }
    .robot-box { animation: float 3s ease-in-out infinite; display: flex; justify-content: center; width: 100%; }
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-15px); } 100% { transform: translateY(0px); } }
    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 4. Khởi tạo dữ liệu và API
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Thiếu API Key!")
    st.stop()

knowledge_data = load_knowledge_base()

if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

# 5. Logic Đăng nhập / Chat
if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
    with col2:
        st.markdown('<div class="robot-box"><img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="200"></div>', unsafe_allow_html=True)
        name = st.text_input("Định danh Cán bộ/Đoàn viên:", placeholder="Nhập tên...")
        if st.button("🚀 KÍCH HOẠT"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
else:
    with st.sidebar:
        st.markdown('<div class="robot-box"><img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="110"></div>', unsafe_allow_html=True)
        st.markdown(f"<p class='sidebar-text'>Cán bộ: <b style='color:#00d4ff;'>{st.session_state.user}</b></p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        st.markdown("<p class='sidebar-text' style='font-size:0.8rem; opacity:0.7;'>TRA CỨU NHANH:</p>", unsafe_allow_html=True)
        
        # Nút bấm đề xuất theo yêu cầu của Phát
        if st.button("📩 Phản ánh kiến nghị"):
            st.session_state.messages.append({"role": "user", "content": "Quy trình tiếp nhận phản ánh kiến nghị như thế nào?"})
            st.rerun()
        if st.button("🆘 Yêu cầu hỗ trợ"):
            st.session_state.messages.append({"role": "user", "content": "Tôi muốn biết các bước yêu cầu hỗ trợ từ Công đoàn"})
            st.rerun()
        if st.button("📝 Đăng ký Công đoàn"):
            st.session_state.messages.append({"role": "user", "content": "Cho tôi xem mẫu đơn và cách đăng ký gia nhập Công đoàn"})
            st.rerun()

        if st.button("🗑️ XÓA PHIÊN CHAT"):
            st.session_state.messages = []
            st.rerun()

    # Hiển thị Chat
    st.markdown(f"<h4 style='color:#004494;'>Hòa Khánh Digital AI xin chào!</h4>", unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Hỏi tôi về thủ tục, hồ sơ..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # AI trả lời dựa trên dữ liệu file của Phát
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Đang lục tìm hồ sơ..."):
                try:
                    user_query = st.session_state.messages[-1]["content"]
                    # Đưa dữ liệu từ file vào Context
                    context = f"DỮ LIỆU NGHIỆP VỤ CÔNG ĐOÀN:\n{knowledge_data[:10000]}" 
                    
                    res = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": f"Bạn là trợ lý AI Công đoàn xã Hòa Khánh. Hãy dùng dữ liệu được cung cấp để hướng dẫn chi tiết quy trình, mẫu đơn cho Anh/Chị {st.session_state.user}. Nếu dữ liệu có mẫu đơn, hãy trích dẫn các mục cần điền."},
                            {"role": "user", "content": f"{context}\n\nCÂU HỎI: {user_query}"}
                        ],
                        model="llama-3.1-8b-instant"
                    )
                    ans = res.choices[0].message.content
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except:
                    st.error("Lỗi xử lý dữ liệu!")
