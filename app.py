import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime

# 1. Cấu hình giao diện
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳")

# 2. Quản lý File Lịch sử (Lưu vào thư mục hiện tại)
HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(messages):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

# 3. Khởi tạo dữ liệu
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

# 4. Cấu hình AI
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    system_instruction="Bạn là Trợ lý ảo Công đoàn xã Hòa Khánh. Hãy trả lời lịch sự, chính xác."
)

# 5. Giao diện Sidebar (Thanh bên cạnh)
with st.sidebar:
    st.title("⚙️ Tùy chọn")
    if st.button("🗑️ Xóa toàn bộ lịch sử"):
        st.session_state.messages = []
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        st.rerun()
    st.write("---")
    st.info("Lịch sử trò chuyện được lưu tự động để bạn có thể xem lại sau.")

# 6. Hiển thị lịch sử chat
st.title("🇻🇳 TRỢ LÝ CÔNG ĐOÀN HÒA KHÁNH")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Xử lý câu hỏi mới
if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
    # Hiển thị tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI phản hồi
    with st.chat_message("assistant"):
        with st.spinner("Đang tra cứu..."):
            response = model.generate_content(prompt)
            full_response = response.text
            st.markdown(full_response)
            
    # Lưu vào danh sách và file
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_history(st.session_state.messages)
