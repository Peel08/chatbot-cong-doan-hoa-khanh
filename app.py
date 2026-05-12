import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document
import io
import os

# --- 1. CẤU HÌNH TRANG & ICON APP ---
# page_icon="logo.png" giúp hiện logo trên tab trình duyệt
st.set_page_config(page_title="Công đoàn Hòa Khánh", page_icon="logo.png", layout="wide")

# --- 2. HÀM ĐỌC DỮ LIỆU ---
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

# --- 3. CSS TỐI ƯU & FIX LOGO IPHONE ---
# Lưu ý: Phát nên thay cái link href bên dưới bằng link ảnh thật trên GitHub của Phát để iPhone hiện icon đẹp nhất
st.markdown("""
    <head>
        <link rel="apple-touch-icon" href="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/logo.png">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    </head>
    <style>
    .main { background-color: #ffffff; }
    /* Sidebar xanh đậm chuẩn Công đoàn */
    [data-testid="stSidebar"] { background-color: #004494 !important; }
    .sidebar-text { color: white; text-align: center; font-size: 0.9rem; margin-top: 15px; }
    
    /* Nút bấm bo góc */
    .stButton > button { 
        background-color: #004494 !important; 
        color: white !important; 
        border-radius: 25px !important; 
        width: 100% !important;
        font-weight: bold !important;
        height: 45px;
        border: none !important;
    }
    
    /* Giao diện chat */
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    
    /* Footer */
    .author-footer { text-align: center; color: #7f8c8d; font-size: 0.8rem; margin-top: 50px; padding: 20px; border-top: 1px solid #eee; }
    
    /* Căn giữa màn hình đăng nhập */
    .login-box { text-align: center; padding: 30px; border-radius: 20px; border: 1px solid #eee; background: #f9f9f9; }
    </style>
""", unsafe_allow_html=True)

# --- 4. KẾT NỐI API ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Chưa cấu hình GROQ_API_KEY trong Secrets!")
    st.stop()

internal_knowledge = load_internal_data()

# --- 5. QUẢN LÝ TRẠNG THÁI ĐĂNG NHẬP ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- MÀN HÌNH ĐĂNG NHẬP CHÍNH GIỮA ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.image("logo.png", width=120)
        st.markdown("<h2 style='color: #004494;'>TRỢ LÝ ẢO CÔNG ĐOÀN</h2>", unsafe_allow_html=True)
        st.markdown("<p>Chào mừng Anh/Chị đến với hệ thống hỗ trợ trực tuyến xã Hòa Khánh</p>", unsafe_allow_html=True)
        
        name_input = st.text_input("Nhập họ tên của Anh/Chị:", placeholder="Ví dụ: Nguyễn Thị Lan")
        if st.button("🚀 BẮT ĐẦU NGAY"):
            if name_input:
                st.session_state.user_name = name_input
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.warning("Anh/Chị vui lòng nhập tên để tiếp tục!")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- GIAO DIỆN CHAT (SAU KHI ĐĂNG NHẬP) ---
    with st.sidebar:
        st.image("logo.png", width=100)
        st.markdown(f"<div class='sidebar-text'>Xin chào anh/chị:<br><b style='font-size:1.1rem;'>{st.session_state.user_name}</b></div>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🗑️ XÓA HỘI THOẠI"):
            st.session_state.messages = []
            st.rerun()
        if st.button("🚪 ĐĂNG XUẤT"):
            st.session_state.logged_in = False
            st.rerun()
        st.markdown(f"<p class='sidebar-text' style='opacity:0.7;'>Thiết kế bởi:<br>Lương Tấn Phát</p>", unsafe_allow_html=True)

    st.markdown(f"<h4 style='color: #004494; text-align:center;'>Trợ lý Công đoàn xã Hòa Khánh</h4>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-size:0.9rem;'>Chào Anh/Chị <b>{st.session_state.user_name}</b>, tôi có thể giúp gì cho Anh/Chị?</p>", unsafe_allow_html=True)

    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("⚡ Đang tra cứu dữ liệu..."):
                try:
                    context = f"DỮ LIỆU NỘI BỘ XÃ HÒA KHÁNH:\n{internal_knowledge[:8000]}"
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": f"Bạn là Trợ lý AI Công đoàn xã Hòa Khánh. Luôn gọi người dùng là Anh/Chị {st.session_state.user_name}. Tuyệt đối không dùng từ Quý khách, Bác, Chú. Trả lời chuyên nghiệp, lịch sự."},
                            {"role": "user", "content": f"{context}\n\nCÂU HỎI: {prompt}"}
                        ],
                        model="llama-3.1-8b-instant",
                    )
                    ans = chat_completion.choices[0].message.content
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except:
                    st.error("Kết nối AI bị gián đoạn, vui lòng thử lại.")

# --- 6. CHÂN TRANG ---
st.markdown(f'<div class="author-footer">Xây dựng và vận hành bởi <b>Lương Tấn Phát</b><br>© 2026 Công đoàn xã Hòa Khánh, Tây Ninh</div>', unsafe_allow_html=True)
