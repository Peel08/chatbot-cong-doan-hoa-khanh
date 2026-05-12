import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document
import io
import os

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

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

# --- 2. CSS CHUẨN MOBILE CỦA PHÁT ---
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

# --- 3. KẾT NỐI GROQ AI (XỊN HƠN GEMINI FREE) ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Thiếu GROQ_API_KEY trong Secrets!")
    st.stop()

internal_knowledge = load_internal_data()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("logo.png", width=180)
    st.markdown("<p class='sidebar-title'>CÔNG ĐOÀN HÒA KHÁNH</p>", unsafe_allow_html=True)
    if "user_name" not in st.session_state or not st.session_state.user_name:
        name = st.text_input("Đăng nhập:", placeholder="Nhập tên...")
        if st.button("🚀 KÍCH HOẠT"):
            if name: st.session_state.user_name = name; st.rerun()
    else:
        st.markdown(f'<div class="user-card"><span style="font-size: 0.85rem; opacity: 0.9;">Phiên làm việc của</span><br><span style="font-size: 1.4rem; font-weight: bold;">{st.session_state.user_name}</span></div>', unsafe_allow_html=True)
        st.markdown("<p style='color: white; text-align: center; font-size: 0.9rem;'>📍 Hòa Khánh, Tây Ninh</p>", unsafe_allow_html=True)
        if st.button("🗑️ XÓA HỘI THOẠI"):
            st.session_state.messages = []; st.rerun()
        st.markdown(f"<p class='author-info'>Thiết kế bởi:<br><b>Lương Tấn Phát</b></p>", unsafe_allow_html=True)

# --- 5. GIAO DIỆN CHAT ---
st.markdown("<h2 style='text-align: center; color: #004494;'>TRỢ LÝ ẢO CÔNG ĐOÀN</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Hỏi tôi về chính sách..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Đang phản hồi tức thì..."):
            context = f"Dữ liệu nội bộ của Công đoàn Hòa Khánh:\n{internal_knowledge[:10000]}\n\n"
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Bạn là trợ lý AI chuyên nghiệp của Công đoàn Hòa Khánh. Trả lời ngắn gọn, chuẩn xác dựa trên dữ liệu cung cấp."},
                        {"role": "user", "content": f"{context} Câu hỏi của {st.session_state.user_name}: {prompt}"}
                    ],
                    model="llama-3-8b-8192", # Model cực nhanh và khôn
                )
                ans = chat_completion.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except:
                st.error("Lỗi kết nối. Phát kiểm tra lại Key nhé!")

st.markdown(f'<div class="author-footer">Xây dựng bởi <b>Lương Tấn Phát</b><br>© 2026 Công đoàn Hòa Khánh</div>', unsafe_allow_html=True)
