import streamlit as st
import google.generativeai as genai
import time

# 1. Cấu hình trang (Luôn ở dòng 1)
st.set_page_config(page_title="Công đoàn Hòa Khánh", page_icon="🇻🇳", layout="wide")

# 2. CSS làm đẹp (Màu xanh Công đoàn)
st.markdown("""
    <style>
    .main { background-color: #f0f5ff; }
    [data-testid="stSidebar"] { background-color: #0056b3; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] input { color: black !important; background-color: white !important; }
    .stChatMessage { border-radius: 15px; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# 3. Kết nối AI (Gemini 3 Flash)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Sử dụng đúng tên model bạn đang dùng
    model = genai.GenerativeModel("gemini-3-flash-preview")
else:
    st.error("Chưa cấu hình API Key!")
    st.stop()

# 4. Quản lý Session
if "user_name" not in st.session_state: st.session_state.user_name = None
if "messages" not in st.session_state: st.session_state.messages = []

# 5. Thanh bên Sidebar
with st.sidebar:
    try:
        st.image("logo.png", width=150)
    except:
        st.image("https://upload.wikimedia.org/wikipedia/vi/thumb/c/cb/Logo_Cong_doan_Viet_Nam.svg/1200px-Logo_Cong_doan_Viet_Nam.svg.png", width=120)
    
    st.title("CÔNG ĐOÀN HÒA KHÁNH")
    if not st.session_state.user_name:
        name = st.text_input("Nhập tên của bạn:")
        if st.button("Vào Chat"):
            if name: st.session_state.user_name = name; st.rerun()
        st.stop()
    else:
        st.success(f"Chào bạn: {st.session_state.user_name}")
        if st.button("🗑️ Xóa lịch sử"):
            st.session_state.messages = []
            st.rerun()

# 6. Giao diện Chat chính
st.markdown("<h1 style='text-align: center;'>🤖 TRỢ LÝ CÔNG ĐOÀN</h1>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Xử lý nhập câu hỏi với cơ chế "Kiên nhẫn" (Retry Logic)
if prompt := st.chat_input("Mời đặt câu hỏi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang tra cứu dữ liệu..."):
            success = False
            # Tự động thử lại tối đa 3 lần nếu Google báo bận (Lỗi 429)
            for attempt in range(3):
                try:
                    # Gợi ý AI trả lời súc tích để tiết kiệm lượt dùng
                    response = model.generate_content(f"Bạn là cán bộ Công đoàn xã Hòa Khánh. Trả lời súc tích cho {st.session_state.user_name}: {prompt}")
                    ans_text = response.text
                    st.markdown(ans_text)
                    st.session_state.messages.append({"role": "assistant", "content": ans_text})
                    success = True
                    break # Thành công thì thoát vòng lặp
                except Exception as e:
                    if "429" in str(e) and attempt < 2:
                        time.sleep(5) # Đợi 5 giây rồi thử lại tự động
                        continue
                    else:
                        st.warning("⚠️ Google đang giới hạn lượt dùng miễn phí. Phát hãy đợi 30 giây rồi hỏi tiếp nhé!")
                        break
