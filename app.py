import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import io
import os
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

# --- 2. HÀM TỰ ĐỘNG ĐỌC DỮ LIỆU TỪ THƯ MỤC DATA ---
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

# --- 3. CSS CHUẨN MOBILE & HIỆN THỊ TÁC GIẢ ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #004494 !important; text-align: center; }
    [data-testid="stSidebar"] [data-testid="stImage"] { display: flex; justify-content: center; margin-top: 20px; }
    
    .sidebar-title { color: white; text-align: center; font-size: 1.1rem; font-weight: bold; margin-top: 10px; text-transform: uppercase; }
    
    .user-card {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        text-align: center;
        margin: 20px 10px;
    }

    .stButton > button {
        background-color: #ffffff !important;
        color: #004494 !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 45px;
    }
    
    /* Tên tác giả trong Sidebar */
    .author-sidebar { color: rgba(255, 255, 255, 0.8); text-align: center; font-size: 0.85rem; margin-top: 40px; padding-bottom: 20px; }
    
    /* Tên tác giả dưới cùng trang chính */
    .author-footer { text-align: center; color: #7f8c8d; font-size: 0.8rem; margin-top: 50px; padding: 20px; border-top: 1px solid #eee; }
    
    input { color: #000000 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. KẾT NỐI AI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash-8b")
else:
    st.error("Thiếu API Key trong Secrets!")
    st.stop()

# --- 5. NẠP DỮ LIỆU NGUỒN ---
internal_knowledge = load_internal_data()

# --- 6. SIDEBAR ---
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
            
        # TÁC GIẢ XUẤT HIỆN TẠI ĐÂY (SIDEBAR)
        st.markdown(f"<p class='author-sidebar'>Thiết kế bởi:<br><b>Lương Tấn Phát</b></p>", unsafe_allow_html=True)

# --- 7. GIAO DIỆN CHAT CHÍNH (FIX LỖI 429 & TÁC GIẢ FOOTER) ---
st.markdown("<h2 style='text-align: center; color: #004494;'>TRỢ LÝ ẢO CÔNG ĐOÀN</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Hỏi tôi về chính sách..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        with st.spinner("Đang tra cứu..."):
            context = f"Dữ liệu nội bộ: {internal_knowledge[:10000]}\n" if internal_knowledge else ""
            full_prompt = f"{context}Trả lời thân thiện cho {st.session_state.user_name}: {prompt}"
            
            success = False
            retries = 0
            while not success and retries < 5:
                try:
                    response = model.generate_content(full_prompt)
                    ans = response.text
                    status_placeholder.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                    success = True
                except Exception as e:
                    if "429" in str(e):
                        retries += 1
                        for i in range(10, 0, -1):
                            status_placeholder.warning(f"⚠️ Google đang bận. Đang tự động thử lại sau {i} giây...")
                            time.sleep(1)
                    else:
                        status_placeholder.error("Lỗi kết nối. Vui lòng thử lại sau.")
                        break

# TÁC GIẢ XUẤT HIỆN TẠI ĐÂY (CHÂN TRANG CHÍNH)
st.markdown(f"""
    <div class="author-footer">
        Được xây dựng và phát triển bởi <b>Lương Tấn Phát</b><br>
        © 2026 Công đoàn xã Hòa Khánh, Tây Ninh
    </div>
""", unsafe_allow_html=True)
