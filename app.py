import streamlit as st
import google.generativeai as genai
import time

# 1. Cấu hình trang (Bắt buộc dòng đầu)
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

# 2. TOÀN BỘ MA TRẬN CSS ĐỂ LỘT XÁC GIAO DIỆN
st.markdown("""
    <style>
    /* Nền tổng thể sành điệu */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Tùy chỉnh Sidebar thành khối màu xanh sang trọng */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #004a99 0%, #003366 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Biến ô nhập tên và các nút thành khối hiện đại */
    div.stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 10px 15px !important;
        color: #333 !important;
    }

    /* Card chào mừng người dùng (Glassmorphism) */
    .user-profile {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 10px 0;
        text-align: center;
    }

    /* Hiệu ứng cho các bong bóng chat */
    .stChatMessage {
        border-radius: 25px !important;
        padding: 15px 20px !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        border: 1px solid rgba(0,0,0,0.03) !important;
    }

    /* Tiêu đề chính rực rỡ */
    .hero-title {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(to right, #004a99, #0099ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 5px;
    }

    /* Footer nhỏ gọn, tinh tế */
    .dev-footer {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.8rem;
        margin-top: 50px;
        padding-bottom: 20px;
    }
    
    /* Nút bấm chuyển sang màu trắng/xanh sạch sẽ */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. LOGIC KẾT NỐI AI
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-3-flash-preview")
else:
    st.error("⚠️ Vui lòng cấu hình API Key!")
    st.stop()

# 4. QUẢN LÝ NGƯỜI DÙNG
if "user_name" not in st.session_state: st.session_state.user_name = None
if "messages" not in st.session_state: st.session_state.messages = []

# 5. SIDEBAR (THANH BÊN)
with st.sidebar:
    # Logo căn giữa đẹp mắt
    col_logo_1, col_logo_2, col_logo_3 = st.columns([1, 2, 1])
    with col_logo_2:
        st.image("logo.png", use_container_width=True)
    
    st.markdown("<h3 style='text-align: center; color: white;'>CÔNG ĐOÀN HÒA KHÁNH</h3>", unsafe_allow_html=True)
    st.write("---")

    if not st.session_state.user_name:
        st.markdown("<p style='color: white;'>Vui lòng đăng nhập để tiếp tục:</p>", unsafe_allow_html=True)
        name = st.text_input("", placeholder="Nhập họ tên của bạn...", key="main_name_input")
        if st.button("🚀 BẮT ĐẦU NGAY"):
            if name:
                st.session_state.user_name = name
                st.rerun()
        st.stop()
    else:
        # Card người dùng cực sang
        st.markdown(f"""
            <div class="user-profile">
                <span style="font-size: 0.9rem; color: #d1d1d1;">Phiên làm việc của</span><br>
                <span style="font-size: 1.3rem; font-weight: bold; color: white;">{st.session_state.user_name}</span>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='color: #bdc3c7; font-size: 0.85rem; text-align: center;'>📍 Hòa Khánh, Tây Ninh</p>", unsafe_allow_html=True)
        
        st.write("---")
        if st.button("🗑️ XÓA HỘI THOẠI"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown(f"<p style='color: #bdc3c7; text-align: center; font-size: 0.8rem; margin-top: 20px;'>Tác giả: <b>Lương Tấn Phát</b></p>", unsafe_allow_html=True)

# 6. GIAO DIỆN CHAT CHÍNH
st.markdown("<h1 class='hero-title'>TRỢ LÝ ẢO CÔNG ĐOÀN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Hệ thống hỗ trợ đoàn viên xã Hòa Khánh 24/7</p>", unsafe_allow_html=True)

# Hiển thị lịch sử chat với bong bóng bo tròn
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. Ô NHẬP LIỆU (CỐ ĐỊNH PHÍA DƯỚI)
if prompt := st.chat_input("Hỏi tôi bất cứ điều gì về chính sách..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang trích xuất dữ liệu..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Google đang bận, vui lòng thử lại sau giây lát!")

# 8. FOOTER BẢN QUYỀN GẮN TÊN PHÁT
st.markdown(f"""
    <div class="dev-footer">
        Được xây dựng và phát triển bởi <b>Lương Tấn Phát</b><br>
        © 2026 Công đoàn xã Hòa Khánh, Tây Ninh
    </div>
""", unsafe_allow_html=True)
