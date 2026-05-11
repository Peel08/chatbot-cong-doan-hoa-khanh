import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64

# =========================================================
# 1. CẤU HÌNH GIAO DIỆN (PHẢI Ở DÒNG ĐẦU TIÊN)
# =========================================================
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

# =========================================================
# 2. CSS LÀM ĐẸP VÀ FIX LỖI MÀU CHỮ
# =========================================================
st.markdown("""
    <style>
    .main { background-color: #f0f5ff; }
    .stChatMessage { border-radius: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    h1 { color: #0056b3; font-family: 'Segoe UI', sans-serif; text-align: center; }
    
    /* Cấu hình Thanh bên (Sidebar) */
    [data-testid="stSidebar"] { background-color: #0056b3; }
    
    /* Chữ tiêu đề trong Sidebar màu trắng */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }

    /* Ô NHẬP LIỆU: Chữ màu đen, nền trắng rõ ràng */
    [data-testid="stSidebar"] input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Làm đẹp ảnh Logo */
    .sidebar-img {
        filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
        border-radius: 50%;
        background: white;
        padding: 5px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 3. CẤU HÌNH AI VÀ QUẢN LÝ PHIÊN
# =========================================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Phát ơi, bạn chưa dán API Key vào mục Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-3-flash-preview")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_name" not in st.session_state:
    st.session_state.user_name = None

# =========================================================
# 4. THANH BÊN (SIDEBAR)
# =========================================================
with st.sidebar:
    # Hiển thị Logo
    logo_url = "https://upload.wikimedia.org/wikipedia/vi/thumb/c/cb/Logo_Cong_doan_Viet_Nam.svg/1200px-Logo_Cong_doan_Viet_Nam.svg.png"
    st.image(logo_url, width=150)
    
    st.markdown("## CÔNG ĐOÀN HÒA KHÁNH")
    st.write("---")

    # Kiểm tra đăng nhập tên
    if not st.session_state.user_name:
        st.subheader("👤 Đăng nhập")
        name = st.text_input("Nhập Họ tên của bạn:", placeholder="VD: Nguyễn Văn A")
        if name:
            st.session_state.user_name = name
            st.rerun()
        st.info("Vui lòng nhập tên để bắt đầu trò chuyện.")
        st.stop()
    else:
        st.success(f"Chào bạn: {st.session_state.user_name}")
        st.write("📍 Hòa Khánh, Tây Ninh")
        if st.button("🗑️ Xóa lịch sử"):
            st.session_state.messages = []
            st.rerun()

# =========================================================
# 5. HÀM PHÁT ÂM THANH (TTS)
# =========================================================
def speak(text):
    try:
        # Giới hạn độ dài để gTTS không bị treo
        short_text = text[:300] 
        tts = gTTS(text=short_text, lang='vi')
        tts.save("speech.mp3")
        with open("speech.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay style="width: 100%; margin-top: 10px;"></audio>'
            st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        pass

# =========================================================
# 6. GIAO DIỆN CHÁNH VÀ XỬ LÝ CHAT
# =========================================================
st.markdown("<h1>🤖 TRỢ LÝ ẢO CÔNG ĐOÀN VIÊN</h1>", unsafe_allow_html=True)

# Hiển thị tin nhắn lịch sử
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ô nhập câu hỏi chính
if prompt := st.chat_input(f"Mời {st.session_state.user_name} đặt câu hỏi..."):
    # Lưu và hiển thị tin nhắn user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Xử lý phản hồi AI
    with st.chat_message("assistant"):
        with st.spinner("Đang tra cứu hồ sơ..."):
            try:
                # Gửi prompt kèm ngữ cảnh tên người dùng
                context = f"Bạn là cán bộ Công đoàn xã Hòa Khánh. Người đang hỏi tên là {st.session_state.user_name}. Hãy trả lời thân thiện, chính xác."
                response = model.generate_content(f"{context}\n\nCâu hỏi: {prompt}")
                ans_text = response.text
                
                st.markdown(ans_text)
                speak(ans_text) # Phát giọng nói
                
                st.session_state.messages.append({"role": "assistant", "content": ans_text})
            except Exception as e:
                st.error(f"Lỗi AI: {str(e)}")
