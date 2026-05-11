import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Công đoàn Hòa Khánh", layout="wide")

# CSS tối giản
st.markdown("<style>[data-testid='stSidebar'] {background-color: #0056b3; color: white;} .stChatMessage {border-radius: 15px;}</style>", unsafe_allow_html=True)

# Kết nối AI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Sử dụng bản Flash 1.5 - Bản này cực kỳ ít khi bị báo "Bận"
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("Thiếu API Key!")
    st.stop()

# Quản lý tên và tin nhắn
if "user_name" not in st.session_state: st.session_state.user_name = None
if "messages" not in st.session_state: st.session_state.messages = []

with st.sidebar:
    st.image("logo.png", width=150)
    if not st.session_state.user_name:
        name = st.text_input("Nhập tên:")
        if st.button("Vào Chat"):
            if name: st.session_state.user_name = name; st.rerun()
        st.stop()
    else:
        st.success(f"Chào: {st.session_state.user_name}")
        if st.button("Xóa lịch sử"):
            st.session_state.messages = []
            st.rerun()

st.title("🤖 TRỢ LÝ CÔNG ĐOÀN")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Hỏi tôi về chính sách..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Gửi tin nhắn ngắn gọn để tránh lỗi Quota
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.warning("⚠️ Google đang giới hạn lượt dùng miễn phí. Phát hãy đợi 1-2 phút hoặc đổi API Key mới nhé!")
