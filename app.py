import streamlit as st
from groq import Groq
import os

# 1. Cấu hình
st.set_page_config(page_title="Công đoàn Hòa Khánh", page_icon="logo.png", layout="wide")

# 2. CSS (Đã bao đóng kỹ bằng thẻ style)
st.markdown('''
<style>
    [data-testid="stSidebar"] { background-color: #004494 !important; }
    .stButton > button { background-color: #004494 !important; color: white !important; border-radius: 20px; width: 100%; height: 45px; font-weight: bold; }
    .sidebar-text { color: white; text-align: center; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 3. Kết nối API
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Thiếu API Key trong Secrets!")
    st.stop()

# 4. Logic Đăng nhập
if "logged" not in st.session_state: st.session_state.logged = False

if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        st.image("logo.png", width=120)
        st.title("TRỢ LÝ ẢO CÔNG ĐOÀN")
        name = st.text_input("Nhập họ tên của Anh/Chị:")
        if st.button("🚀 BẮT ĐẦU"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
else:
    # Giao diện Chat
    with st.sidebar:
        st.image("logo.png", width=100)
        st.markdown(f"<p class='sidebar-text'>Chào Anh/Chị:<br><b>{st.session_state.user}</b></p>", unsafe_allow_html=True)
        if st.button("🗑️ Xóa Chat"):
            st.session_state.messages = []
            st.rerun()

    st.subheader(f"Chào Anh/Chị {st.session_state.user}, tôi có thể giúp gì ạ?")
    
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Nhập câu hỏi..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                res = client.chat.completions.create(
                    messages=[{"role": "system", "content": f"Bạn là trợ lý công đoàn xã Hòa Khánh. Gọi người dùng là Anh/Chị {st.session_state.user}."},
                              {"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant")
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except: st.error("Lỗi kết nối!")
