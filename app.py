import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document
import io
import os

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Công đoàn Hòa Khánh", page_icon="logo.png", layout="wide")

# --- 2. HÀM ĐỌC DỮ LIỆU NỘI BỘ (CHẠY NGẦM) ---
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

# --- 3. GIAO DIỆN CSS CHUẨN MOBILE (XANH ĐẬM CÔNG ĐOÀN) ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #004494 !important; text-align: center; }
    [data-testid="stSidebar"] [data-testid="stImage"] { display: flex; justify-content: center; margin-top: 20px; }
    .sidebar-title { color: white; text-align: center; font-size: 1.1rem; font-weight: bold; margin-top: 10px; text-transform: uppercase; }
    .user-card { background-color: rgba(255, 255, 255, 0.1); padding: 20px; border-radius: 25px; border: 1px solid rgba(255, 255, 255, 0.2); color: white; text-align: center; margin: 20px 10px; }
    .stButton > button { background-color: #ffffff !important; color: #004494 !important; border-radius: 15px !important; font-weight: bold !important; width: 100% !important; height: 45px; }
    .author-info { color: rgba(255, 255, 255, 0.7); text-align: center; font-size: 0.8rem; margin-top: 40px; }
    .author-footer { text-align: center; color: #7f8c8d; font-size: 0.8rem; margin-top: 50px; padding: 20px; border-top: 1px solid #eee; }
    input { color: #000000 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. KẾT NỐI API GROQ ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Lỗi: Chưa tìm thấy GROQ_API_KEY trong Secrets!")
    st.stop()

internal_knowledge = load_internal_data()

# --- 5. SIDEBAR (THANH ĐIỀU HƯỚNG) ---
with st.sidebar:
    st.image("logo.png", width=180)
    st.markdown("<p class='sidebar-title'>CÔNG ĐOÀN HÒA KHÁNH</p>", unsafe_allow_html=True)
    
    if "user_name" not in st.session_state:
        name_input = st.text_input("Đăng nhập:", placeholder="Nhập họ tên của bạn...")
        if st.button("🚀 KÍCH HOẠT"):
            if name_input:
                st.session_state.user_name = name_input
                st.rerun()
    else:
        st.markdown(f'''
            <div class="user-card">
                <span style="font-size: 0.85rem; opacity: 0.9;">Xin chào</span><br>
                <span style="font-size: 1.2rem; font-weight: bold;">{st.session_state.user_name}</span>
            </div>
        ''', unsafe_allow_html=True)
        if st.button("🗑️ XÓA HỘI THOẠI"):
            st.session_state.messages = []
            st.rerun()
        st.markdown(f"<p class='author-info'>Thiết kế bởi:<br><b>Lương Tấn Phát</b></p>", unsafe_allow_html=True)

# --- 6. LOGIC PHÂN CHIA MÀN HÌNH ---

# Kiểm tra xem người dùng đã đăng nhập chưa
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # --- GIAO DIỆN MÀN HÌNH CHÀO / ĐĂNG NHẬP ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("logo.png", width=120) # Đảm bảo file logo.png có trên GitHub
    st.markdown("<h2 style='text-align: center; color: #004494;'>CHÀO MỪNG ANH/CHỊ</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Vui lòng xác nhận danh tính để bắt đầu</p>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            name_input = st.text_input("Họ và tên của Anh/Chị:", placeholder="Nhập tên tại đây...")
            if st.button("🚀 BẮT ĐẦU SỬ DỤNG"):
                if name_input:
                    st.session_state.user_name = name_input
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.warning("Anh/Chị vui lòng nhập tên để tiếp tục!")
else:
    # --- GIAO DIỆN TRÒ CHUYỆN (SAU KHI ĐĂNG NHẬP) ---
    st.markdown(f"<h3 style='text-align: center; color: #004494;'>TRỢ LÝ CÔNG ĐOÀN HÒA KHÁNH</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; font-size: 0.9rem;'>Chào Anh/Chị: <b>{st.session_state.user_name}</b></p>", unsafe_allow_html=True)
    st.markdown("---")

    if "messages" not in st.session_state: st.session_state.messages = []
    
    # Hiển thị lịch sử chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): 
            st.markdown(msg["content"])

    # Ô nhập nội dung chat
    if prompt := st.chat_input("Hỏi tôi về chính sách, thủ tục..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("⚡ Đang tra cứu..."):
                user_name = st.session_state.user_name
                context = f"DỮ LIỆU NỘI BỘ XÃ HÒA KHÁNH:\n{internal_knowledge[:8000]}\n\n"
                
                try:
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": f"Bạn là Trợ lý AI Công đoàn xã Hòa Khánh. Luôn gọi người dùng là Anh/Chị {user_name}. Không dùng từ Quý khách, Bác, Chú. Trả lời lịch sự, đúng trọng tâm."},
                            {"role": "user", "content": f"{context} CÂU HỎI: {prompt}"}
                        ],
                        model="llama-3.1-8b-instant",
                    )
                    ans = chat_completion.choices[0].message.content
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except Exception as e:
                    st.error("Hệ thống bận, Anh/Chị vui lòng thử lại sau.")

# --- 7. CHÂN TRANG ---
st.markdown(f'<div class="author-footer">Xây dựng bởi <b>Lương Tấn Phát</b><br>© 2026 Công đoàn Hòa Khánh, Tây Ninh</div>', unsafe_allow_html=True)
st.markdown(f'<div class="author-footer">Xây dựng và vận hành bởi <b>Lương Tấn Phát</b><br>© 2026 Công đoàn xã Hòa Khánh, Tây Ninh</div>', unsafe_allow_html=True)
