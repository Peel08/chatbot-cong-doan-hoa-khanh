import streamlit as st
import google.generativeai as genai

# 1. Cấu hình giao diện chuẩn
st.set_page_config(page_title="Công đoàn Hòa Khánh", layout="centered")
st.title("🇻🇳 CHATBOT CÔNG ĐOÀN HÒA KHÁNH")
st.write("Trạng thái: Hệ thống đã kết nối.")

# 2. Kiểm tra API Key an toàn
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Phát ơi, kiểm tra lại mục Secrets trên Streamlit nhé!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. Lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# 4. Xử lý câu hỏi với mã nguồn ép phiên bản
if prompt := st.chat_input("Hỏi tôi bất cứ điều gì..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    try:
        # Ép sử dụng mô hình gemini-1.5-flash (không có chữ models/)
        model = genai.GenerativeModel("gemini-1.5-flash") 
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # Nếu vẫn lỗi 404, dùng bản dự phòng này
        st.warning("Đang chuyển sang chế độ dự phòng...")
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
