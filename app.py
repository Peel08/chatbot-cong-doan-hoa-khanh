import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64

# 1. CẤU HÌNH GIAO DIỆN (Dòng này phải luôn ở ĐẦU TIÊN)
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

# 2. KIỂM TRA ĐĂNG NHẬP (Session State)
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. CSS LÀM ĐẸP
st.markdown("""
    <style>
    .main { background-color: #f0f5ff; }
    .stChatMessage { border-radius: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    h1 { color: #0056b3; font-family: 'Segoe UI', sans-serif; text-align: center; }
    /* Màu nền thanh bên */
    [data-testid="stSidebar"] { background-color: #0056b3; }
    [data-testid="stSidebar"] * { color: white !important; }
    img {
        filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
        border-radius: 50%;
        background: white;
        padding: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 4. CẤU HÌNH AI
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-3-flash-preview")

# 5. HÀM PHÁT ÂM THANH
def speak(text):
    try:
        tts = gTTS(text=text, lang='vi')
        tts.save("speech.mp3")
        with open("speech.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f'<audio src="data:audio/mp3;base64,{b64}" controls autoplay style="width: 100%;"></audio>'
            st.markdown(md, unsafe_allow_html=True)
    except:
        pass

# 6. THANH BÊN (SIDEBAR)
with st.sidebar:
    # Hiển thị logo (Đảm bảo đã up file logo.png lên GitHub)
    try:
        st.image("logo.png", width=150)
    except:
        st.image("https://upload.wikimedia.org/wikipedia/vi/thumb/c/cb/Logo_Cong_doan_Viet_Nam.svg/1200px-Logo_Cong_doan_Viet_Nam.svg.png", width=150)
    
    st.title("CÔNG ĐOÀN HÒA KHÁNH")
    st.write("---")

    if not st.session_state.user_name:
        st.subheader("👤 Đăng nhập")
        name = st.text_input("Nhập Họ tên của bạn:", key="name_input")
        if name:
            st.session_state.user_name = name
            st.rerun()
        st.stop() # Dừng lại cho đến khi nhập tên
    else:
        st.success(f"Chào bạn: {st.session_state.user_name}")
        st.write("📍 Hòa Khánh, Tây Ninh")
        if st.button("🗑️ Xóa lịch sử"):
            st.session_state.messages = []
            st.rerun()

# 7. GIAO DIỆN CHÍNH
st.markdown("<h1>🤖 TRỢ LÝ ẢO CÔNG ĐOÀN VIÊN</h1>", unsafe_allow_html=True)

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 8. NHẬP CÂU HỎI
if prompt := st.chat_input(f"Chào {st.session_state.user_name}, tôi có thể giúp gì cho bạn?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang soạn câu trả lời..."):
            # Gửi kèm tên để AI trả lời thân thiện hơn
            response = model.generate_content(f"Người dùng tên là {st.session_state.user_name}. Hãy giải đáp thân thiện câu hỏi: {prompt}")
            full_response = response.text
            st.markdown(full_response)
            speak(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
