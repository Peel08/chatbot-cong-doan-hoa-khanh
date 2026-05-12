import streamlit as st
import google.generativeai as genai
import time

# 1. Cấu hình trang (Luôn ở dòng đầu)
st.set_page_config(page_title="Công đoàn Hòa Khánh", page_icon="🇻🇳", layout="wide")

# 2. CSS FIX LỖI MÀU CHỮ VÀ GIAO DIỆN
st.markdown("""
    <style>
    .main { background-color: #f0f5ff; }
    
    /* FIX: Đảm bảo chữ trong TẤT CẢ các ô nhập liệu luôn là màu đen */
    input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Màu nền Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0056b3;
    }
    
    /* Chữ hướng dẫn trong Sidebar màu trắng */
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {
        color: white !important;
    }

    /* Bong bóng chat */
    .stChatMessage { border-radius: 15px; }
    
    .footer {
        position: fixed;
        left: 0; bottom: 0; width: 100%;
        text-align: center; color: #888; font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Kết nối AI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-3-flash-preview")
else:
    st.error("Thiếu API Key!")
    st.stop()

# 4. Quản lý Session (Fix lỗi xóa lịch sử)
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. THANH BÊN (SIDEBAR)
with st.sidebar:
    st.image("logo.png", width=150)
    st.markdown("### 🏛️ CÔNG ĐOÀN HÒA KHÁNH")
    
    if not st.session_state.user_name:
        st.subheader("👤 Đăng nhập")
        name = st.text_input("Nhập Họ tên của bạn:", key="input_name")
        if st.button("🚀 Bắt đầu"):
            if name:
                st.session_state.user_name = name
                st.rerun()
        st.stop()
    else:
        st.success(f"Chào bạn: {st.session_state.user_name}")
        st.write("---")
        st.caption("👨‍💻 Phát triển bởi: Lương Tấn Phát")
        
        # HÀM XÓA LỊCH SỬ CHUẨN
        if st.button("🗑️ Xóa lịch sử"):
            st.session_state.messages = [] # Xóa danh sách tin nhắn
            # Xóa sạch các key liên quan đến hội thoại trong session
            for key in st.session_state.keys():
                if key not in ["user_name", "GOOGLE_API_KEY"]:
                    del st.session_state[key]
            st.rerun()

# 6. GIAO DIỆN CHÁNH
st.markdown("<h1 style='text-align: center; color: #0056b3;'>🤖 TRỢ LÝ ẢO CÔNG ĐOÀN</h1>", unsafe_allow_html=True)

# Hiển thị tin nhắn
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. Ô NHẬP LIỆU CHÍNH
if prompt := st.chat_input("Hỏi tôi về chính sách công đoàn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang tra cứu..."):
            try:
                response = model.generate_content(prompt)
                ans = response.text
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except Exception as e:
                st.warning("Hệ thống bận, Phát đợi xíu rồi bấm gửi lại nhé!")

st.markdown(f'<div class="footer">© 2026 Xây dựng và phát triển bởi Lương Tấn Phát</div>', unsafe_allow_html=True)
