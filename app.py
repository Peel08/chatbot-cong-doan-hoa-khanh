import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang (Dòng này phải ở trên cùng)
st.set_page_config(page_title="Công đoàn Hòa Khánh", layout="centered")

st.title("🇻🇳 CHATBOT CÔNG ĐOÀN HÒA KHÁNH")
st.write("Trạng thái: Hệ thống đã kết nối.")

# 2. Kiểm tra API Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Phát ơi, bạn chưa dán mã API vào mục Secrets của Streamlit Cloud rồi!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 3. Khung chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

# 4. Xử lý câu hỏi (Dùng tên mô hình cơ bản nhất để tránh lỗi NotFound)
if prompt := st.chat_input("Hỏi tôi bất cứ điều gì..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    try:
        # Dùng 'gemini-pro' là bản ổn định nhất, ít khi bị lỗi NotFound
        model = genai.GenerativeModel("gemini-pro") 
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Lỗi kết nối AI: {e}")
