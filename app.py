import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import io
import os
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

# --- 2. HÀM TỰ ĐỘNG QUÉT VÀ ĐỌC DỮ LIỆU TỪ THƯ MỤC NỘI BỘ ---
@st.cache_resource # Chỉ đọc dữ liệu một lần để tiết kiệm tốc độ
def load_internal_data():
    combined_text = ""
    data_folder = "data" # Đây là thư mục Phát vừa tạo trên GitHub
    
    if os.path.exists(data_folder):
        for filename in os.listdir(data_folder):
            file_path = os.path.join(data_folder, filename)
            try:
                if filename.endswith(".pdf"):
                    reader = PdfReader(file_path)
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            combined_text += text + "\n"
                elif filename.endswith(".docx"):
                    doc = Document(file_path)
                    combined_text += "\n".join([para.text for para in doc.paragraphs]) + "\n"
            except Exception as e:
                print(f"Lỗi khi đọc file {filename}: {e}")
    return combined_text

# --- 3. GIAO DIỆN CSS CAO CẤP (GLASSMORPHISM) ---
st.markdown("""
    <style>
    /* Nền tổng thể */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Sidebar thiết kế hiện đại */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #004a99 0%, #003366 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* FIX lỗi màu chữ: Chữ đen, nền trắng cho các ô nhập liệu */
    input {
        color: #000000 !important;
        background-color: #ffffff !important;
        border-radius: 10px !important;
    }

    /* Card thông tin người dùng trong Sidebar */
    .user-profile {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 15px;
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

    /* Tiêu đề rực rỡ */
    .hero-title {
        background: linear-gradient(to right, #004a99, #0099ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        text-align: center;
    }

    /* Dòng chữ bản quyền mờ tinh tế */
    .dev-footer {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.8rem;
        margin-top: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. KẾT NỐI AI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-3-flash-preview")
else:
    st.error("⚠️ Phát ơi, hãy cấu hình API Key trong mục Secrets nhé!")
    st.stop()

# --- 5. NẠP DỮ LIỆU NỘI BỘ (CHẠY NGẦM) ---
internal_knowledge = load_internal_data()

# --- 6. QUẢN LÝ PHIÊN (SESSION) ---
if "user_name" not in st.session_state: st.session_state.user_name = None
if "messages" not in st.session_state: st.session_state.messages = []

# --- 7. THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.image("logo.png", width=130)
    st.markdown("<h3 style='text-align: center; color: white;'>CÔNG ĐOÀN HÒA KHÁNH</h3>", unsafe_allow_html=True)
    st.write("---")

    if not st.session_state.user_name:
        st.markdown("<p style='color: white;'>Đăng nhập để bắt đầu:</p>", unsafe_allow_html=True)
        name = st.text_input("", placeholder="Nhập họ tên của bạn...")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user_name = name
                st.rerun()
        st.stop()
    else:
        st.markdown(f"""
            <div class="user-profile">
                <span style="font-size: 0.8rem; opacity: 0.8;">Xin chào cán bộ/đoàn viên</span><br>
                <span style="font-size: 1.1rem; font-weight: bold;">{st.session_state.user_name}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.info("📚 Hệ thống đã sẵn sàng với dữ liệu nội bộ.")
        
        st.write("---")
        if st.button("🗑️ XÓA HỘI THOẠI"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown(f"<p style='text-align: center; color: #bdc3c7; font-size: 0.8rem; margin-top: 20px;'>Phát triển bởi: <br><b>Lương Tấn Phát</b></p>", unsafe_allow_html=True)

# --- 8. GIAO DIỆN CHAT CHÍNH ---
st.markdown("<h1 class='hero-title'>TRỢ LÝ ẢO CÔNG ĐOÀN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Hệ thống tra cứu thông tin chính thống xã Hòa Khánh</p>", unsafe_allow_html=True)

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Xử lý nhập câu hỏi
if prompt := st.chat_input("Hỏi tôi về chính sách, thủ tục công đoàn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Đang trích xuất dữ liệu nội bộ..."):
            
            # CẤU TRÚC PROMPT ÉP AI DÙNG KIẾN THỨC TỪ FOLDER /DATA
            context_prefix = ""
            if internal_knowledge:
                context_prefix = f"Dựa trên dữ liệu nội bộ của Công đoàn Hòa Khánh sau đây:\n{internal_knowledge[:12000]}\n\n"
            
            full_prompt = f"{context_prefix}Hãy trả lời câu hỏi của {st.session_state.user_name}: {prompt}. Trả lời một cách chuyên nghiệp, chính xác."

            try:
                response = model.generate_content(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ Google đang giới hạn. Phát hãy đợi 10 giây rồi thử lại nhé!")
                else:
                    st.error("Máy chủ bận, Phát vui lòng thử lại sau.")

# --- 9. FOOTER ---
st.markdown(f"""
    <div class="dev-footer">
        Được xây dựng và phát triển bởi <b>Lương Tấn Phát</b><br>
        © 2026 Công đoàn xã Hòa Khánh, Tây Ninh
    </div>
""", unsafe_allow_html=True)
