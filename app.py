import streamlit as st

# 1. Cấu hình trang
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="🤖", layout="centered")

# 2. CSS "QUYỀN LỰC" - DIỆT TẬN GỐC Ô TRẮNG THỪA
st.markdown('''
<style>
    /* ÉP BIẾN MẤT cái ô trắng thừa (thường là do st.write hoặc khoảng cách mặc định) */
    .element-container:has(iframe), 
    .stMarkdown:empty, 
    .element-container:empty {
        display: none !important;
    }

    /* Xóa khoảng trắng thừa giữa các component */
    div.block-container {
        padding-top: 2rem !important;
        vertical-align: top !important;
    }

    /* Nền ứng dụng */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%);
    }

    /* THIẾT KẾ CARD TẬP TRUNG (LÀM GIAO DIỆN SANG HẲN LÊN) */
    .main-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 40px;
        box-shadow: 0 15px 35px rgba(0, 51, 102, 0.1);
        border: 1px solid #ffffff;
        text-align: center;
        width: 100%;
        max-width: 500px;
        margin: -40px auto 0 auto; /* Đẩy card lên sát robot */
    }

    /* Robot bay */
    .robot-box {
        text-align: center;
        animation: float 3s ease-in-out infinite;
        z-index: 10;
        position: relative;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
    }

    /* Nút bấm */
    div.stButton > button {
        background: #004494 !important;
        color: white !important;
        border-radius: 12px !important;
        height: 50px !important;
        width: 100% !important;
        font-weight: bold !important;
        border: none !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background: #002d62 !important;
        transform: scale(1.02);
    }
</style>
''', unsafe_allow_html=True)

# 3. GIAO DIỆN ĐĂNG NHẬP (KHÔNG CÒN Ô TRẮNG THỪA)
if "logged" not in st.session_state:
    st.session_state.logged = False

if not st.session_state.logged:
    # Phần Robot
    st.markdown('<div class="robot-box">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=160)
    st.markdown('</div>', unsafe_allow_html=True)

    # Toàn bộ nội dung chữ và input nằm GỌN trong CARD này
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    st.markdown("<h2 style='color: #004494; margin-bottom: 0;'>HÒA KHÁNH AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; font-size: 0.9rem; margin-bottom: 25px;'>Hệ thống Trợ lý số Công đoàn</p>", unsafe_allow_html=True)
    
    name = st.text_input("Username", placeholder="Nhập tên Anh/Chị...", label_visibility="collapsed")
    
    if st.button("KÍCH HOẠT HỆ THỐNG"):
        if name:
            st.session_state.user = name
            st.session_state.logged = True
            st.rerun()
        else:
            st.error("Vui lòng nhập tên!")

    st.markdown("<p style='font-size: 0.75rem; color: #999; margin-top: 30px; border-top: 1px solid #eee; padding-top: 15px;'>Phát triển bởi: <b>Lương Tấn Phát</b></p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.success(f"Đã đăng nhập: {st.session_state.user}")
    if st.button("Đăng xuất"):
        st.session_state.logged = False
        st.rerun()
