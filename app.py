import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="🤖", layout="centered")

# 2. CSS Tối giản (Tránh gây lỗi trắng trang)
st.markdown('''
<style>
    .stApp { background-color: #f0f2f6; }
    .main-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
    }
    header, footer, #MainMenu {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 3. Kết nối API
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Lỗi: Kiểm tra lại Secrets GROQ_API_KEY trên Streamlit Cloud!")
    st.stop()

# 4. Logic Đăng nhập
if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

if not st.session_state.logged:
    st.markdown('<div style="text-align:center; margin-top:50px;">', unsafe_allow_html=True)
    # Thử comment dòng image này nếu vẫn trắng trang để kiểm tra file ảnh có lỗi không
    st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=150)
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("<h1 style='color: #003366;'>HÒA KHÁNH AI</h1>", unsafe_allow_html=True)
    
    name = st.text_input("Username", placeholder="Nhập tên Anh/Chị...", label_visibility="collapsed")
    
    if st.button("KÍCH HOẠT HỆ THỐNG"):
        if name:
            st.session_state.user = name
            st.session_state.logged = True
            st.rerun()
    st.markdown('</div></div>', unsafe_allow_html=True)

else:
    # Giao diện Chat
    st.sidebar.title(f"Chào {st.session_state.user}")
    
    # Khu vực Mic (Đảm bảo đã cài streamlit-mic-recorder)
    st.write("🎤 Ghi âm câu hỏi:")
    audio = mic_recorder(start_prompt="Bắt đầu nói", stop_prompt="Dừng và Gửi", key='recorder')

    if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            res = client.chat.completions.create(
                messages=[{"role": "user", "content": st.session_state.messages[-1]["content"]}],
                model="llama-3.1-8b-instant"
            )
            ans = res.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
