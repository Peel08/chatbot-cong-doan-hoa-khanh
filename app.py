import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Công đoàn Hòa Khánh", layout="centered")
st.title("🇻🇳 CHATBOT CÔNG ĐOÀN HÒA KHÁNH")

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Chưa có API Key trong Secrets!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# TÍNH NĂNG XỊN: Tự động tìm model khả dụng
if "model_name" not in st.session_state:
    with st.spinner("Đang khởi động bộ não AI..."):
        try:
            # Liệt kê các model mà Key của bạn có quyền dùng
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            st.session_state.model_name = models[0] # Chọn cái đầu tiên tìm thấy
        except Exception as e:
            st.error(f"Không tìm thấy model nào: {e}")
            st.stop()

if prompt := st.chat_input("Hỏi tôi bất cứ điều gì..."):
    st.chat_message("user").markdown(prompt)
    
    model = genai.GenerativeModel(st.session_state.model_name)
    try:
        response = model.generate_content(prompt)
        st.chat_message("assistant").markdown(response.text)
    except Exception as e:
        st.error(f"Lỗi: {e}")
