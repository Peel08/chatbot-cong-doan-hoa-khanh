import streamlit as st
import google.generativeai as genai
import time

# 1. CẤU HÌNH GIAO DIỆN XỊN (UI/UX)
st.set_page_config(
    page_title="Công đoàn Hòa Khánh AI",
    page_icon="🇻🇳",
    layout="centered"
)

# Tùy chỉnh màu sắc xanh Công đoàn và hiệu ứng bo góc
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInputContainer { padding-bottom: 20px; }
    h1 { color: #0056b3; font-family: 'Helvetica Neue', sans-serif; }
    .stAlert { border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# 2. CẤU HÌNH BỘ NÃO AI (THÔNG MINH HƠN)
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Thiếu API Key! Hãy kiểm tra lại mục Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Thiết lập System Instruction để AI đóng vai chuẩn cán bộ
instruction = (
    "Bạn là 'Trợ lý ảo Công đoàn xã Hòa Khánh'. "
    "Phong cách: Lịch sự, tận tâm, am hiểu pháp luật lao động và các hoạt động của xã. "
    "Nhiệm vụ: Giải đáp thắc mắc về BHXH, BHYT, chế độ thai sản, ốm đau và các hoạt động phong trào tại địa phương. "
    "Nếu không biết rõ thông tin địa phương cụ thể, hãy hướng dẫn người dân đến trực tiếp văn phòng UBND xã Hòa Khánh để được hỗ trợ."
)

model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    system_instruction=instruction
)

# 3. GIAO DIỆN CHÍNH
st.markdown("<h1 style='text-align: center;'>🇻🇳 TRỢ LÝ CÔNG ĐOÀN HÒA KHÁNH</h1>", unsafe_allow_html=True)
st.info("👋 Chào mừng bạn! Tôi là trí tuệ nhân tạo hỗ trợ Đoàn viên và nhân dân xã Hòa Khánh.")

# Khởi tạo lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lại các tin nhắn cũ
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. XỬ LÝ NHẬP LIỆU & HIỆU ỨNG CHỮ CHẠY (STREAMING)
if prompt := st.chat_input("Nhập câu hỏi của bạn tại đây..."):
    # Hiển thị tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Phản hồi của AI
    with st.chat_message("assistant"):
        response_placeholder = st.empty() # Tạo chỗ trống để chữ chạy ra
        full_response = ""
        
        try:
            # Gọi AI với chế độ stream để trả lời nhanh hơn
            responses = model.generate_content(prompt, stream=True)
            
            for chunk in responses:
                full_response += chunk.text
                # Tạo hiệu ứng đánh máy
                response_placeholder.markdown(full_response + "▌")
                time.sleep(0.01) # Chỉnh tốc độ chạy chữ
            
            response_placeholder.markdown(full_response) # Hiển thị bản cuối cùng sạch sẽ
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"❌ Có lỗi xảy ra: {str(e)}")
