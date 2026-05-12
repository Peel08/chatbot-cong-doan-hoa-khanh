import streamlit as st
from groq import Groq
from PyPDF2 import PdfReader
from docx import Document
import io
import os

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

# --- 2. HÀM ĐỌC DỮ LIỆU NỘI BỘ ---
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

# --- 3. GIAO DIỆN CSS (CHUẨN MOBILE XANH ĐẬM) ---
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

# --- 4. KẾT NỐI GROQ AI ---
try:
    if "GROQ_API_KEY" in st.secrets:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    else:
        st.error("❌ Chưa cấu hình GROQ_API_KEY trong Secrets!")
        st.stop()
except Exception as e:
    st.error(f"❌ Lỗi kết nối API: {e}")
    st.stop()

internal_knowledge = load_internal_data()

# --- 5. SIDEBAR (THANH BÊN) ---
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

# --- 6. GIAO DIỆN CHAT CHÍNH ---
st.markdown("<h2 style='text-align: center; color: #004494;'>TRỢ LÝ ẢO CÔNG ĐOÀN</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Hỏi tôi về chính sách, thủ tục..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Đang kết hợp dữ liệu và AI..."):
            # Lấy dữ liệu file (giới hạn để không quá tải)
            context = f"DỮ LIỆU NỘI BỘ XÃ HÒA KHÁNH:\n{internal_knowledge[:8000]}\n\n"
            
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": f"""Bạn là Trợ lý ảo AI của Công đoàn xã Hòa Khánh.
                            HƯỚNG DẪN TRẢ LỜI:
                            1. Ưu tiên sử dụng 'DỮ LIỆU NỘI BỘ XÃ HÒA KHÁNH' để trả lời chính xác các câu hỏi về quy định, thủ tục tại địa phương.
                            2. Nếu thông tin không có trong file nội bộ, hãy sử dụng KIẾN THỨC AI sâu rộng của bạn để tư vấn và giải thích thêm cho người dùng.
                            3. Luôn giữ thái độ thân thiện, lịch sự và xưng hô phù hợp với {st.session_state.user_name}. Trả lời bằng tiếng Việt chuyên nghiệp."""
                        },
                        {"role": "user", "content": f"{context} CÂU HỎI: {prompt}"}
                    ],
                    model="llama-3.1-8b-instant", # Model mới nhất, tốc độ tức thì
                )
                ans = chat_completion.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except Exception as e:
                st.error(f"❌ Lỗi xử lý AI: {str(e)}")

# --- 7. FOOTER (CHÂN TRANG) ---
st.markdown(f'<div class="author-footer">Xây dựng bởi <b>Lương Tấn Phát</b><br>© 2026 Công đoàn Hòa Khánh, Tây Ninh</div>', unsafe_allow_html=True)
