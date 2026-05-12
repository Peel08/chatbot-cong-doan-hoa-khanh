import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document
import io
import os

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Công đoàn Hòa Khánh", page_icon="logo.png", layout="wide")

# --- 2. HÀM ĐỌC DỮ LIỆU NỘI BỘ ---
@st.cache_resource
def load_internal_data():
    combined_text = ""
    data_folder = "data"
    if os.path.exists(data_folder):
        for filename in os.listdir(data_folder):
            file_path = os.path.join(data_folder, filename)
            try:
                if filename.endswith(".pdf"):
                    reader = PdfReader(file_path)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text: combined_text += text + "\n"
                elif filename.endswith(".docx"):
                    doc = Document(file_path)
                    combined_text += "\n".join([para.text for para in doc.paragraphs]) + "\n"
            except: pass
    return combined_text

# --- 3. CSS TỐI ƯU GIAO DIỆN & FIX ICON IPHONE ---
st.markdown("""
    <head>
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/logo.png">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    </head>
    <style>
    /* Ẩn các menu thừa của Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Nền trắng chủ đạo */
    .stApp { background-color: #ffffff; }

    /* Sidebar xanh đậm Công đoàn */
    [data-testid="stSidebar"] { background-color: #004494 !important; }
    .sidebar-text { color: white; text-align: center; font-size: 0.95rem; margin-top: 10px; line-height: 1.4; }
    
    /* Nút bấm bo tròn chuyên nghiệp */
    div.stButton > button {
        background-color: #004494 !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        height: 48px !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Căn chỉnh khung Đăng nhập */
    .login-container {
        text-align: center;
        padding: 40px 20px;
        background: #fdfdfd;
        border-radius: 30px;
        border: 1px solid #eee;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-top: 20px;
    }

    /* Định dạng tin nhắn chat */
    .stChatMessage { border-radius: 20px !important; padding: 15px !important; }

    /* Chân trang */
    .footer-custom {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        margin-top: 60px;
        padding: 20px;
        border-top: 1px solid #f0f0f0;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. KẾT NỐI API GROQ ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Lỗi: Chưa cấu hình GROQ_API_KEY trong mục Secrets!")
    st.stop()

internal_knowledge = load_internal_data()

# --- 5. LOGIC ĐĂNG NHẬP ---
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if not st.session_state.is_logged_in:
    # HIỂN THỊ MÀN HÌNH CHÀO
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.image("logo.png", width=130)
        st.markdown("<h1 style='color: #004494; font-size: 1.8rem;'>TRỢ LÝ ẢO CÔNG ĐOÀN</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #555;'>Chào mừng Anh/Chị đến với hệ thống hỗ trợ trực tuyến xã Hòa Khánh</p>", unsafe_allow_html=True)
        
        user_name = st.text_input("Vui lòng nhập họ tên của Anh/Chị:", placeholder="Ví dụ: Nguyễn Thị Lan")
        
        if st.button("🚀 BẮT ĐẦU SỬ DỤNG"):
            if user_name:
                st.session_state.user_full_name = user_name
                st.session_state.is_logged_in = True
                st.rerun()
            else:
                st.warning("Anh/Chị cần nhập tên để hệ thống nhận diện nhé!")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # --- GIAO DIỆN CHAT CHÍNH ---
    with st.sidebar:
        st.image("logo.png", width=110)
        st.markdown(f"<div class='sidebar-text'>Thành viên đang truy cập:<br><b style='font-size:1.1rem;'>{st.session_state.user_full_name}</b></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🗑️ Xóa hội thoại"):
            st.session_state.messages = []
            st.rerun()
            
        if st.button("🚪 Đăng xuất"):
            st.session_state.is_logged_in = False
            st.rerun()
            
        st.markdown(f"<p class='sidebar-text' style='opacity:0.6; font-size:0.8rem; margin-top:50px;'>Thiết kế bởi:<br>Lương Tấn Phát</p>", unsafe_allow_html=True)

    # Tiêu đề chat
    st.markdown(f"<h4 style='color: #004494; text-align:center;'>Chào Anh/Chị {st.session_state.user_full_name}!</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:0.9rem; color:#666;'>Tôi có thể hỗ trợ gì cho Anh/Chị về công tác Công đoàn hôm nay?</p>", unsafe_allow_html=True)

    # Khởi tạo tin nhắn
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Xử lý nhập liệu
    if prompt := st.chat_input("Hãy đặt câu hỏi cho Trợ lý tại đây..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("⚡ Đang tra cứu thông tin..."):
                try:
                    user_name = st.session_state.user_full_name
                    context = f"DỮ LIỆU NỘI BỘ CÔNG ĐOÀN XÃ HÒA KHÁNH:\n{internal_knowledge[:8000]}"
                    
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": f"Bạn là Trợ lý AI chính thức của Công đoàn xã Hòa Khánh. Nhiệm vụ của bạn là hỗ trợ cán bộ và người lao động. Luôn gọi người dùng là Anh/Chị {user_name}. Trả lời ngắn gọn, lịch sự, đúng nghiệp vụ. Không dùng từ 'Quý khách', 'Bác', 'Chú'."},
                            {"role": "user", "content": f"{context}\n\nCÂU HỎI CỦA NGƯỜI DÙNG: {prompt}"}
                        ],
                        model="llama-3.1-8b-instant",
                        temperature=0.4
                    )
                    response = chat_completion.choices[0].message.content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except:
                    st.error("Kết nối bị gián đoạn. Anh/Chị vui lòng thử lại sau giây lát!")

# --- 6. CHÂN TRANG ---
st.markdown(f'<div class="footer-custom">Xây dựng và vận hành bởi <b>Lương Tấn Phát</b><br>© 2026 Công đoàn xã Hòa Khánh, Tây Ninh</div>', unsafe_allow_html=True)
