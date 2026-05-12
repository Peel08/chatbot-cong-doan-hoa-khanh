import streamlit as st
import google.generativeai as genai
import time

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Công đoàn Hòa Khánh", page_icon="🇻🇳", layout="wide")

# 2. CSS "SIÊU CẤP": Fix lỗi màu chữ, làm Sidebar sang trọng
st.markdown("""
    <style>
    /* Nền chính sáng sủa */
    .main { background-color: #f4f7f9; }
    
    /* Sidebar thiết kế hiện đại */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0056b3 0%, #003366 100%);
    }
    
    /* FIX lỗi khung chào bị xấu: Thay bằng Card trắng tinh tế */
    .user-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white !important;
        margin-bottom: 20px;
    }

    /* Đảm bảo ô nhập liệu luôn dễ nhìn */
    input {
        color: #1f1f1f !important;
        background-color: #ffffff !important;
        border-radius: 8px !important;
    }

    /* Chữ tiêu đề Sidebar */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Nút xóa lịch sử xịn hơn */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        border: none;
        transition: 0.3s;
    }
    
    /* Làm đẹp bong bóng chat */
    .stChatMessage {
        border-radius: 15px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 3. KẾT NỐI AI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-3-flash-preview")
else:
    st.error("⚠️ Thiếu API Key!")
    st.stop()

# 4. QUẢN LÝ PHIÊN
if "user_name" not in st.session_state: st.session_state.user_name = None
if "messages" not in st.session_state: st.session_state.messages = []

# 5. THANH BÊN (SIDEBAR) - THIẾT KẾ MỚI
with st.sidebar:
    st.image("logo.png", width=150)
    st.markdown("<h2 style='text-align: center;'>🏛️ CÔNG ĐOÀN HÒA KHÁNH</h2>", unsafe_allow_html=True)
    st.write("---")
    
    if not st.session_state.user_name:
        st.markdown("### 👤 Đăng nhập")
        name = st.text_input("Nhập Họ tên của bạn:", key="name_box", placeholder="VD: Lương Tấn Phát")
        if st.button("🚀 Bắt đầu"):
            if name:
                st.session_state.user_name = name
                st.rerun()
        st.stop()
    else:
        # Khung chào kiểu mới, không còn bị xanh lá xấu xí
        st.markdown(f"""
            <div class='user-card'>
                <p style='margin:0; font-size: 14px; opacity: 0.8;'>Chào mừng trở lại,</p>
                <p style='margin:0; font-size: 18px; font-weight: bold;'>{st.session_state.user_name}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("📍 **Địa chỉ:** Hòa Khánh, Tây Ninh")
        st.write(f"👨‍💻 **Dev:** Lương Tấn Phát")
        
        st.write("---")
        if st.button("🗑️ Xóa lịch sử hội thoại"):
            st.session_state.messages = []
            st.rerun()

# 6. GIAO DIỆN CHÍNH
st.markdown("<h1 style='text-align: center; color: #0056b3;'>🤖 TRỢ LÝ ẢO CÔNG ĐOÀN VIÊN</h1>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. Ô NHẬP LIỆU
if prompt := st.chat_input("Nhập câu hỏi của bạn tại đây..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Đang trích xuất dữ liệu..."):
            try:
                response = model.generate_content(prompt)
                ans = response.text
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except Exception as e:
                st.warning("Hệ thống đang bận, Phát vui lòng thử lại sau 30 giây!")
