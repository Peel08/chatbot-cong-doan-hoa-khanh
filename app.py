import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import io
import os
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

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

# --- 3. CSS TỐI ƯU GIAO DIỆN GIỐNG HÌNH (MOBILE FIRST) ---
st.markdown("""
    <style>
    /* Nền chính */
    .main { background-color: #ffffff; }
    
    /* Sidebar xanh đậm chuẩn Công đoàn */
    [data-testid="stSidebar"] {
        background-color: #004494 !important;
        text-align: center;
    }
    
    /* Căn giữa hình ảnh trong Sidebar */
    [data-testid="stSidebar"] [data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin-bottom: -20px;
    }

    /* Tiêu đề trắng căn giữa */
    .sidebar-title {
        color: white;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 20px;
        text-transform: uppercase;
    }

    /* Card thông tin "Phiên làm việc" giống hình */
    .user-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        text-align: center;
        margin: 20px 10px;
    }

    /* Nút Xóa lịch sử màu trắng bo tròn */
    .stButton > button {
        background-color: #ffffff !important;
        color: #004494 !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
        padding: 10px !important;
    }
    
    /* Tác giả căn giữa phía dưới */
    .author-text {
        color: rgba(255, 255, 255, 0.7);
        text-align: center;
        font-size: 0.8rem;
        margin-top: 50px;
    }

    /* Sửa màu chữ Input để không bị lỗi */
    input { color: #000000 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. KẾT NỐI AI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-3-flash-preview")
else:
    st.error("Cấu hình API Key trong Secrets!")
    st.stop()

# --- 5. NẠP DỮ LIỆU ---
internal_knowledge = load_internal_data()

# --- 6. SIDEBAR - THIẾT KẾ GIỐNG HÌNH ---
with st.sidebar:
    # Logo
    st.image("logo.png", width=180)
    
    # Tên công đoàn căn giữa
    st.markdown("<p class='sidebar-title'>CÔNG ĐOÀN HÒA KHÁNH</p>", unsafe_allow_html=True)

    if "user_name" not in st.session_state or not st.session_state.user_name:
        name = st.text_input("Họ tên:", placeholder="Nhập tên...")
        if st.button("🚀 KÍCH HOẠT"):
            if name: 
                st.session_state.user_name = name
                st.rerun()
    else:
        # Card Phiên làm việc giống hình Phát gửi
        st.markdown(f"""
            <div class="user-card">
                <span style="font-size: 0.85rem; opacity: 0.9;">Phiên làm việc của</span><br>
                <span style="font-size: 1.4rem; font-weight: bold;">{st.session_state.user_name}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='color: white; text-align: center; font-size: 0.9rem;'>📍 Hòa Khánh, Tây Ninh</p>", unsafe_allow_html=True)
        
        st.write("") # Tạo khoảng cách
        if st.button("🗑️ XÓA HỘI THOẠI"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown(f"<p class='author-text'>Tác giả: <b>Lương Tấn Phát</b></p>", unsafe_allow_html=True)

# --- 7. GIAO DIỆN CHAT ---
if "messages" not in st.session_state: st.session_state.messages = []

# Hiển thị tiêu đề trang chính (nếu cần)
st.markdown("<h2 style='text-align: center; color: #004494;'>TRỢ LÝ ẢO CÔNG ĐOÀN</h2>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Hỏi tôi về chính sách..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        context = f"Dữ liệu: {internal_knowledge[:10000]}\n" if internal_knowledge else ""
        try:
            response = model.generate_content(f"{context}Trả lời {st.session_state.user_name}: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except: st.warning("Bận rồi, đợi xíu nha!")
