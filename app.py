import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
import base64

# 1. CẤU HÌNH GIAO DIỆN CHUẨN
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

# CSS để đổi màu xanh Công đoàn và làm đẹp khung chat
st.markdown("""
    <style>
    .main { background-color: #f0f5ff; }
    .stChatMessage { border-radius: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    h1 { color: #0056b3; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .sidebar .sidebar-content { background-image: linear-gradient(#0056b3, #007bff); color: white; }
    </style>
""", unsafe_allow_html=True)

# 2. THANH BÊN (SIDEBAR) CÓ LOGO
with st.sidebar:
    # Link logo Công đoàn Việt Nam
    st.image(logo.png)
    st.title("CÔNG ĐOÀN XÃ HÒA KHÁNH")
    st.markdown("---")
    st.write("📍 **Địa chỉ:** Hòa Khánh, Tây Ninh")
    st.info("Trợ lý AI hỗ trợ giải đáp thủ tục và chính sách 24/7.")
    if st.button("🗑️ Xóa lịch sử"):
        st.session_state.messages = []
        st.rerun()

# 3. CẤU HÌNH AI
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-3-flash-preview")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. HIỂN THỊ CHAT
st.markdown("<h1 style='text-align: center;'>🤖 TRỢ LÝ ẢO CÔNG ĐOÀN VIÊN</h1>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. XỬ LÝ PHÁT ÂM THANH (TTS)
def speak(text):
    tts = gTTS(text=text, lang='vi')
    tts.save("speech.mp3")
    with open("speech.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f'<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(md, unsafe_allow_html=True)

# 6. NHẬP CÂU HỎI
if prompt := st.chat_input("Mời bạn nhập câu hỏi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang tra cứu và soạn câu trả lời..."):
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            
            # Tự động phát giọng nói câu trả lời
            speak(full_response)
            
    st.session_state.messages.append({"role": "assistant", "content": full_response})
