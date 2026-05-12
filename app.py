import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document
import io
import os

# --- 1. CẤU HÌNH TRANG & LOGO APP ---
# Thay 'logo.png' bằng file ảnh logo của Phát trên GitHub để đổi icon App
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

# --- 3. CSS TỐI ƯU GIAO DIỆN MOBILE ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    /* Sidebar xanh đậm chuẩn Công đoàn */
    [data-testid="stSidebar"] { background-color: #004494 !important; }
    .sidebar-text { color: white; text-align: center; font-size: 0.9rem; margin-top: 20px; }
    /* Nút bấm bo góc chuyên nghiệp */
    .stButton > button { 
        background-color: #004494 !important; 
        color: white !important; 
        border-radius: 20px !important; 
        width: 100% !important;
        font-weight: bold !important;
    }
    /* Căn giữa màn hình chào */
    .welcome-container { text-align: center; padding-top: 50px; }
    .author-footer { text-align: center; color: #7f8c8d; font-size: 0.8rem; margin-top: 50px; padding: 20px; border-top: 1px solid #eee; }
    </style>
""", unsafe_allow_html=True)

# --- 4. KẾT NỐI API ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Chưa cấu hình API Key!")
    st.stop()

internal_knowledge = load_internal_data()

# --- 5. QUẢN LÝ ĐĂNG NHẬP & CHAT ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- MÀN HÌNH ĐĂNG NHẬP (CHÍNH GIỮA) ---
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='welcome-container'>", unsafe_allow_html=True)
        st.image("logo.png", width=150)
        st.markdown("<h2 style='text-align: center; color: #004494;'>TRỢ LÝ ẢO CÔNG ĐOÀN</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Chào mừng Anh/Chị đến với hệ thống hỗ trợ trực tuyến xã Hòa Khánh</p>", unsafe_allow_html=True)
        
        name_input = st.text_input("Nhập họ và tên của Anh/Chị để bắt đầu:", placeholder="Ví dụ: Nguyễn Văn A")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name_input:
                st.session_state.user_name = name_input
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Vui lòng nhập tên!")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # --- GIAO DIỆN CHAT (SAU KHI ĐĂNG NHẬP) ---
    with st.sidebar:
        st.image("logo.png", width=120)
        st.markdown(f"<div class='sidebar-text'>Đang phục vụ:<br><b>{st.session_state.user_name}</b></div>", unsafe_allow_html=True)
        if st.button("🗑️ XÓA CHAT"):
            st.session_state.messages = []
            st.rerun()
        st.markdown("<br><p class='sidebar-text'>Thiết kế: Lương Tấn Phát</p>", unsafe_allow_html=True)

    st.markdown(f"<h4 style='color: #004494;'>Chào Anh/Chị {st.session_state.user_name}, tôi có thể giúp gì ạ?</h4>", unsafe_allow_html=True)

    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Nhập câu hỏi..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Đang tra cứu..."):
                try:
                    context = f"DỮ LIỆU NỘI BỘ:\n{internal_knowledge[:8000]}"
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": f"Bạn là Trợ lý AI Công đoàn xã Hòa Khánh. Gọi người dùng là Anh/Chị {st.session_state.user_name}. Không dùng từ Quý khách, Bác, Chú. Trả lời chuyên nghiệp."},
                            {"role": "user", "content": f"{context}\n\nCÂU HỎI: {prompt}"}
                        ],
                        model="llama-3.1-8b-instant",
                    )
                    ans = chat_completion.choices[0].message.content
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except:
                    st.error("Lỗi kết nối!")

# --- 6. CHÂN TRANG ---
st.markdown(f'<div class="author-footer">Xây dựng bởi <b>Lương Tấn Phát</b><br>© 2026 Công đoàn Hòa Khánh, Tây Ninh</div>', unsafe_allow_html=True)
