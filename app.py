import streamlit as st
import google.generativeai as genai

# DÒNG NÀY PHẢI ĐỨNG ĐẦU TIÊN
st.set_page_config(page_title="Công đoàn Hòa Khánh", layout="centered")

st.title("🇻🇳 CHATBOT CÔNG ĐOÀN HÒA KHÁNH")
st.write("Chào Phát! Nếu bạn thấy dòng này thì hệ thống đã sống!")

# Kiểm tra Key
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Lỗi: Bạn chưa điền GOOGLE_API_KEY vào mục Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

if prompt := st.chat_input("Hỏi tôi bất cứ điều gì..."):
    st.chat_message("user").markdown(prompt)
    # Hai dòng dưới đây phải thụt vào chính xác 4 dấu cách (hoặc 1 phím Tab)
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    response = model.generate_content(prompt)
    st.chat_message("assistant").markdown(response.text)
