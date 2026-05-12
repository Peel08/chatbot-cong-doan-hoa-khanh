import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import io
import os
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

# --- 2. HÀM TỰ ĐỘNG QUÉT VÀ ĐỌC DỮ LIỆU TỪ THƯ MỤC DATA ---
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
            except:
                pass
    return combined_text

# --- 3. CSS CAO CẤP: GLASSMORPHISM & GRADIENT ---
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    /* Sidebar thiết kế hiện đại */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #004a99 0%, #003366 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* FIX màu chữ ô nhập liệu */
    input {
        color: #000000 !important;
        background-color: #ffffff !important;
        border-radius: 10px !important;
    }

    /* Card thông tin người dùng trong Sidebar */
    .user-profile {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 10px 0;
        text-align: center;
        color: white;
    }

    /* Bong bóng chat bo tròn hiện đại */
    .stChatMessage {
        border-radius: 25px !important;
        padding: 15px 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
    }

    /* Tiêu đề chính rực rỡ */
    .hero-title {
        background: linear-gradient(to right, #004a99, #0099ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        text-align: center;
    }

    .dev-footer {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.8rem;
        margin-top: 50px;
    }
    
    /* Làm đẹp nút bấm */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. KẾT NỐI AI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-3-flash-preview")
else:
    st.error("⚠️ Hãy cấu hình API Key trong Secrets!")
    st.stop()

# --- 5. NẠP DỮ LIỆU ---
internal_knowledge = load_internal_data()

# --- 6. QUẢN LÝ PHIÊN ---
if "user_name" not in st.session_state: st.session_state.user_name = None
if "messages" not in st.session_state: st.session_state.messages = []

# --- 7. THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.image("logo.png", width=140)
    st.markdown("<h3 style='text-align: center; color: white;'>CÔNG ĐOÀN HÒA KHÁNH</h3>", unsafe_allow_html=True)
    st.write("---")

    if not st.session_state.user_name:
        st.markdown("<p style='color: white;'>Đăng nhập hệ thống:</p>", unsafe_allow_html=True)
        name = st.text_input("", placeholder="Nhập họ tên...", key="login_name")
        if st.button("🚀 KÍCH HOẠT"):
            if name:
                st.session_state.user_name = name
                st.rerun()
        st.stop()
    else:
        st.markdown(f"""
            <div class="user-profile">
                <span style="font-size: 0.85rem; opacity: 0.8;">Xin chào cán bộ/đoàn viên</span><br>
                <span style="font-size: 1.25rem; font-weight: bold;">{st.session_state.user_name}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        if st.button("🗑️ XÓA HỘI THOẠI"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown(f"<p style='text-align: center; color: #bdc3c7; font-size: 0.85rem; margin-top: 30px;'>Phát triển bởi:<br><b style='color: white;'>Lương Tấn Phát</b></p>", unsafe_allow_html=True)

# --- 8. GIAO DIỆN CHAT CHÍNH ---
st.markdown("<h1 class='hero-title'>TRỢ LÝ ẢO CÔNG ĐOÀN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Hỗ trợ đoàn viên tra cứu quy định chính thống 24/7</p>", unsafe_allow_html=True)

# Hiển thị lịch sử
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Xử lý nhập liệu
if prompt := st.chat_input("Hỏi tôi bất cứ điều gì về chính sách..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Đang trích xuất dữ liệu..."):
            
            # Gộp dữ liệu nội bộ vào Prompt (ẩn với người dùng)
            context = ""
            if internal_knowledge:
                context = f"Dựa trên tài liệu nội bộ sau: \n{internal_knowledge[:12000]}\n\n"
            
            full_prompt = f"{context}Trả lời câu hỏi của {st.session_state.user_name}: {prompt}"

            try:
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.warning("Hệ thống bận, Phát thử lại sau 10 giây nhé!")

# --- 9. FOOTER ---
st.markdown(f"""
    <div class="dev-footer">
        Được xây dựng và phát triển bởi <b>Lương Tấn Phát</b><br>
        © 2026 Công đoàn xã Hòa Khánh, Tây Ninh
    </div>
""", unsafe_allow_html=True)
