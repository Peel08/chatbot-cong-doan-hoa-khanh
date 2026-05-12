import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document
import io
import os

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

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

# --- 4. KẾT NỐI API ---
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

# --- 6. GIAO DIỆN CHAT CHÍNH ---
st.markdown("<h2 style='text-align: center; color: #004494;'>TRỢ LÝ ẢO CÔNG ĐOÀN</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Đang tra cứu..."):
            user_name = st.session_state.get("user_name", "")
            context = f"DỮ LIỆU NỘI BỘ XÃ HÒA KHÁNH:\n{internal_knowledge[:8000]}\n\n"
            
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            # Tìm và thay thế đoạn content của system như sau:
"content": f"""Bạn là Trợ lý AI chính thức của Công đoàn xã Hòa Khánh.
QUY TẮC PHẠM VI HỖ TRỢ:
1. Bạn đại diện cho CÔNG ĐOÀN XÃ HÒA KHÁNH, không phải một chi bộ hay ấp riêng lẻ nào.
2. Tuyệt đối không tự giới hạn mình vào 'Chi bộ Ấp Hóc Thơm 1' hay bất kỳ đơn vị nhỏ nào khác, trừ khi người dùng hỏi đích danh về đơn vị đó.
3. Luôn gọi người dùng là 'Anh/Chị' hoặc 'Anh/Chị {user_name}'. Không dùng các từ xưng hô khác.
4. Trả lời ngắn gọn, đúng trọng tâm. Nếu người dùng chào, hãy chào lại: 'Trợ lý Công đoàn xã Hòa Khánh xin chào Anh/Chị {user_name}, tôi có thể giúp gì cho Anh/Chị?'."""
                            5. Chỉ dùng dữ liệu nội bộ để trả lời khi câu hỏi liên quan trực tiếp đến tài liệu đó."""
                        },
                        {"role": "user", "content": f"{context} Câu hỏi từ Anh/Chị {user_name}: {prompt}"}
                    ],
                    model="llama-3.1-8b-instant",
                )
                ans = chat_completion.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except Exception as e:
                st.error("Hệ thống bận, vui lòng hỏi lại sau.")

# --- 7. CHÂN TRANG ---
st.markdown(f'<div class="author-footer">Xây dựng và vận hành bởi <b>Lương Tấn Phát</b><br>© 2026 Công đoàn Hòa Khánh, Tây Ninh</div>', unsafe_allow_html=True)
