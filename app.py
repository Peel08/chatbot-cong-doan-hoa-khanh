import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import io
import os
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

# --- 2. HÀM TỰ ĐỘNG ĐỌC DỮ LIỆU TỪ FOLDER /DATA ---
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

# --- 3. CSS TỐI ƯU GIAO DIỆN CHUẨN MOBILE (NHƯ HÌNH PHÁT GỬI) ---
st.markdown("""
    <style>
    /* Tổng thể */
    .main { background-color: #ffffff; }
    
    /* Sidebar Xanh đậm chuẩn Công đoàn */
    [data-testid="stSidebar"] {
        background-color: #004494 !important;
    }
    
    /* Căn giữa hình ảnh Logo */
    [data-testid="stSidebar"] [data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 0px;
    }

    /* Tiêu đề Công đoàn căn giữa */
    .sidebar-title {
        color: white;
        text-align: center;
        font-size: 1.1rem;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 30px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Card "Phiên làm việc" bo tròn cực đẹp */
    .user-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 25px 15px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        text-align: center;
        margin: 10px 10px 20px 10px;
    }

    /* Nút bấm Trắng - Chữ Xanh bo tròn */
    .stButton > button {
        background-color: #ffffff !important;
        color: #004494 !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100% !important;
        height: 45px;
        transition: 0.3s;
    }
    
    /* Dòng thông tin tác giả căn giữa dưới cùng */
    .author-info {
        color: rgba(255, 255, 255, 0.7);
        text-align: center;
        font-size: 0.8rem;
        margin-top: 60px;
    }

    /* Đảm bảo ô nhập liệu không bị lỗi màu chữ */
    input { color: #000000 !important; }
    
    /* Bong bóng chat bo tròn mềm mại */
    .stChatMessage { border-radius: 20px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. KẾT NỐI AI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-3-flash-preview")
else:
    st.error("Lỗi: Thiếu API Key trong Secrets!")
    st.stop()

# --- 5. NẠP DỮ LIỆU NỘI BỘ ---
internal_knowledge = load_internal_data()

# --- 6. THANH BÊN (SIDEBAR) - THIẾT KẾ THEO YÊU CẦU ---
with st.sidebar:
    # Logo căn giữa
    st.image("logo.png", width=180)
    
    # Tên đơn vị
    st.markdown("<p class='sidebar-title'>CÔNG ĐOÀN HÒA KHÁNH</p>", unsafe_allow_html=True)

    if "user_name" not in st.session_state or not st.session_state.user_name:
        name = st.text_input("Đăng nhập:", placeholder="Nhập tên của bạn...")
        if st.button("🚀 BẮT ĐẦU"):
            if name: 
                st.session_state.user_name = name
                st.rerun()
    else:
        # Card Phiên làm việc (Căn giữa hoàn toàn)
        st.markdown(f"""
            <div class="user-card">
                <span style="font-size: 0.9rem; opacity: 0.85;">Phiên làm việc của</span><br>
                <span style="font-size: 1.5rem; font-weight: bold;">{st.session_state.user_name}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='color: white; text-align: center; font-size: 0.9rem;'>📍 Hòa Khánh, Tây Ninh</p>", unsafe_allow_html=True)
        
        st.write("---") # Đường kẻ mờ
        
        if st.button("🗑️ XÓA HỘI THOẠI"):
            st.session_state.messages = []
            st.rerun()
        
        # Tác giả căn giữa phía dưới
        st.markdown(f"<p class='author-info'>Tác giả: <b>Lương Tấn Phát</b></p>", unsafe_allow_html=True)

# --- 7. GIAO DIỆN CHAT ---
st.markdown("<h2 style='text-align: center; color: #004494;'>TRỢ LÝ ẢO CÔNG ĐOÀN</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Hỏi tôi về các quy định công đoàn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang tìm dữ liệu chính thống..."):
            # Gộp dữ liệu từ /data vào prompt ngầm
            context = f"Dữ liệu nội bộ: {internal_knowledge[:10000]}\n" if internal_knowledge else ""
            try:
                response = model.generate_content(f"{context}Trả lời thân thiện cho {st.session_state.user_name}: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.warning("⚠️ Hiện tại hệ thống đang bận, Phát thử lại sau 10 giây nhé!")
