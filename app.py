import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
import io
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

# --- 2. HÀM XỬ LÝ FILE (PDF & WORD) ---
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_docx(file):
    doc = Document(io.BytesIO(file.read()))
    return "\n".join([para.text for para in doc.paragraphs])

# --- 3. GIAO DIỆN CSS CAO CẤP (GLASSMORPHISM) ---
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    /* Sidebar hiện đại */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #004a99 0%, #003366 100%);
        color: white;
    }
    
    /* FIX lỗi màu chữ: Chữ nhập vào luôn màu đen, nền trắng */
    input { color: #000000 !important; background-color: #ffffff !important; }
    
    /* Card thông tin người dùng */
    .user-profile {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 15px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 20px;
        text-align: center;
    }

    /* Bong bóng Chat */
    .stChatMessage {
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        margin-bottom: 15px !important;
    }

    .hero-title {
        background: linear-gradient(to right, #004a99, #0099ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        text-align: center;
    }

    .dev-footer {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.8rem;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. KẾT NỐI AI ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Sử dụng bản Gemini 3 Flash mới nhất để đạt tốc độ cao
    model = genai.GenerativeModel("gemini-3-flash-preview")
else:
    st.error("⚠️ Vui lòng cấu hình GOOGLE_API_KEY trong Secrets!")
    st.stop()

# --- 5. QUẢN LÝ SESSION ---
if "user_name" not in st.session_state: st.session_state.user_name = None
if "messages" not in st.session_state: st.session_state.messages = []
if "file_content" not in st.session_state: st.session_state.file_content = ""

# --- 6. THANH BÊN (SIDEBAR) ---
with st.sidebar:
    st.image("logo.png", width=120)
    st.markdown("<h3 style='text-align: center;'>CÔNG ĐOÀN HÒA KHÁNH</h3>", unsafe_allow_html=True)
    st.write("---")

    if not st.session_state.user_name:
        st.subheader("👤 Đăng nhập")
        name = st.text_input("Nhập Họ tên của bạn:", placeholder="VD: Lương Tấn Phát")
        if st.button("🚀 KÍCH HOẠT"):
            if name:
                st.session_state.user_name = name
                st.rerun()
        st.stop()
    else:
        st.markdown(f"""<div class="user-profile">
            <span style="font-size: 0.8rem; opacity: 0.8;">Xin chào,</span><br>
            <span style="font-size: 1.1rem; font-weight: bold;">{st.session_state.user_name}</span>
        </div>""", unsafe_allow_html=True)

        # MỤC TẢI FILE DỮ LIỆU CHÍNH THỐNG
        st.subheader("📚 Nạp dữ liệu nguồn")
        uploaded_file = st.file_uploader("Tải PDF hoặc Word (Quy định, chính sách...)", type=["pdf", "docx"])
        
        if uploaded_file:
            with st.spinner("Đang đọc dữ liệu..."):
                if uploaded_file.type == "application/pdf":
                    st.session_state.file_content = read_pdf(uploaded_file)
                else:
                    st.session_state.file_content = read_docx(uploaded_file)
            st.success("✅ Đã nạp tài liệu thành công!")

        st.write("---")
        # Nút xóa lịch sử triệt để
        if st.button("🗑️ Xóa hội thoại"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown(f"<p style='text-align: center; font-size: 0.8rem; opacity: 0.7;'>👨‍💻 Dev: <b>Lương Tấn Phát</b></p>", unsafe_allow_html=True)

# --- 7. GIAO DIỆN CHAT CHÍNH ---
st.markdown("<h1 class='hero-title'>TRỢ LÝ ẢO CÔNG ĐOÀN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Hệ thống trả lời tự động dựa trên trí tuệ nhân tạo và dữ liệu chính thống</p>", unsafe_allow_html=True)

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 8. XỬ LÝ NHẬP LIỆU VÀ AI ---
if prompt := st.chat_input("Hỏi tôi về chính sách, thủ tục..."):
    # Lưu tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI trả lời
    with st.chat_message("assistant"):
        with st.spinner("⚡ Đang trích xuất thông tin..."):
            
            # Xây dựng câu hỏi gửi đi (Gộp cả nội dung file nếu có)
            if st.session_state.file_content:
                # Chỉ lấy 10k ký tự đầu để tránh quá tải cho bản Free
                context = st.session_state.file_content[:10000]
                final_prompt = f"""Bạn là cán bộ Công đoàn xã Hòa Khánh. 
                Dựa vào nội dung tài liệu sau đây:
                ---
                {context}
                ---
                Hãy trả lời câu hỏi của {st.session_state.user_name}: {prompt}
                Lưu ý: Nếu thông tin không có trong tài liệu, hãy trả lời dựa trên kiến thức chung nhưng phải báo rõ là tài liệu không đề cập."""
            else:
                final_prompt = f"Bạn là cán bộ Công đoàn xã Hòa Khánh. Trả lời chu đáo cho {st.session_state.user_name}: {prompt}"

            try:
                response = model.generate_content(final_prompt)
                full_res = response.text
                st.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except Exception as e:
                if "429" in str(e):
                    st.warning("⚠️ Google đang giới hạn lượt dùng. Phát đợi 10 giây rồi nhấn gửi lại nhé!")
                else:
                    st.error("Lỗi kết nối. Vui lòng thử lại sau!")

# --- 9. FOOTER ---
st.markdown(f"""<div class="dev-footer">
    Xây dựng và phát triển bởi <b>Lương Tấn Phát</b><br>
    © 2026 Công đoàn xã Hòa Khánh, Tây Ninh
</div>""", unsafe_allow_html=True)
