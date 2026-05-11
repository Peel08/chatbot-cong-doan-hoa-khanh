import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang (Phải ở dòng 1)
st.set_page_config(page_title="Công đoàn Hòa Khánh", layout="centered")

# 2. CSS làm đẹp giao diện
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    [data-testid="stSidebar"] { background-color: #0056b3; }
    [data-testid="stSidebar"] * { color: white !important; }
    input { color: black !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Kết nối AI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    st.error("Chưa cấu hình API Key trong Secrets!")
    st.stop()

# 4. Quản lý Đăng nhập
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Giao diện đăng nhập ở Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/vi/thumb/c/cb/Logo_Cong_doan_Viet_Nam.svg/1200px-Logo_Cong_doan_Viet_Nam.svg.png", width=100)
    st.title("CÔNG ĐOÀN HÒA KHÁNH")
    
    if not st.session_state.user_name:
        st.subheader("👤 Đăng nhập")
        name = st.text_input("Nhập tên của bạn:", key="login_name")
        if st.button("Bắt đầu"):
            if name:
                st.session_state.user_name = name
                st.rerun()
        st.stop() # Dừng tại đây nếu chưa có tên
    else:
        st.success(f"Chào bạn, {st.session_state.user_name}")
        if st.button("Xóa lịch sử"):
            st.session_state.messages = []
            st.rerun()

# 5. Giao diện Chat chính
st.title("🤖 TRỢ LÝ CÔNG ĐOÀN")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Hỏi tôi về chính sách..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang trả lời..."):
            response = model.generate_content(f"Bạn là trợ lý công đoàn xã Hòa Khánh. Hãy trả lời người tên {st.session_state.user_name}: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
