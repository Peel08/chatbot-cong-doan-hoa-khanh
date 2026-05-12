import streamlit as st
from groq import Groq
import os

# 1. Cấu hình trang - Sử dụng icon robot mặc định nếu chưa có file logo.png
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="🤖", layout="wide")

# 2. HỆ THỐNG GIAO DIỆN PREMIUM (Custom CSS)
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;600;800&display=swap');

    /* Font chữ và Nền tổng thể */
    html, body, [class*="st-emotion-cache"] {
        font-family: 'Urbanist', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #f8fafd 0%, #e2e8f0 100%);
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #003366 0%, #001f3f 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
        box-shadow: 10px 0 30px rgba(0,0,0,0.1);
    }
    
    /* Ép Sidebar ra giữa */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        align-items: center !important;
        text-align: center !important;
    }

    /* Vô hiệu hóa các thành phần mặc định của Streamlit */
    header, footer, #MainMenu {visibility: hidden;}

    /* LOGIN WRAPPER & CARD (Sửa lỗi ô trắng thừa) */
    .login-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        margin-top: -20px;
    }

    .login-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 45px;
        border-radius: 30px;
        box-shadow: 0 25px 50px rgba(0, 51, 102, 0.15);
        width: 100%;
        max-width: 500px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .login-card:hover { transform: translateY(-5px); }

    /* Hiệu ứng Robot bay */
    .robot-container {
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 15px 25px rgba(0, 68, 148, 0.3));
        margin-bottom: -15px;
        z-index: 99;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-25px); }
    }

    /* Nút bấm Premium Navy-Gold */
    div.stButton > button {
        background: linear-gradient(90deg, #003366 0%, #0056b3 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        border: 2px solid transparent !important;
        height: 55px !important;
        width: 100% !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 10px 20px rgba(0, 51, 102, 0.2);
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 25px rgba(0, 51, 102, 0.3);
        border-color: #ffd700 !important; /* Viền vàng khi hover */
    }

    /* Khung Chat mượt mà */
    [data-testid="stChatMessage"] {
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.03) !important;
        margin-bottom: 1rem !important;
        background-color: white !important;
    }

    /* Footer Số hóa */
    .digital-footer {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 5rem;
        padding: 2rem;
        border-top: 1px solid #e2e8f0;
    }
    .digital-footer b { color: #003366; }
</style>
''', unsafe_allow_html=True)

# 3. Kết nối API Groq
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Chưa tìm thấy GROQ_API_KEY trong cấu hình!")
    st.stop()

# 4. Quản lý trạng thái đăng nhập
if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

# --- GIAO DIỆN ĐĂNG NHẬP ---
if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
    with col2:
        st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
        
        # Robot Mascot
        st.markdown('<div class="robot-container">', unsafe_allow_html=True)
        # Sử dụng URL ảnh từ Github của bạn để đảm bảo hiển thị
        st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=200)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Bảng Đăng nhập
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown("<h1 style='color: #003366; font-weight: 800; font-size: 2.2rem; margin-bottom:0;'>HÒA KHÁNH AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #0056b3; font-weight: 600; margin-bottom: 30px; letter-spacing: 1px;'>KỶ NGUYÊN SỐ CÔNG ĐOÀN V3.5</p>", unsafe_allow_html=True)
        
        # Input định danh
        name = st.text_input("Username", placeholder="Họ tên Anh/Chị cán bộ...", label_visibility="collapsed")
        
        if st.button("KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
            else:
                st.warning("⚠️ Vui lòng nhập định danh để tiếp tục!")
        
        st.markdown(f'''
            <div style="margin-top: 35px; border-top: 1px solid #e5e7eb; padding-top: 20px;">
                <p style="font-size: 0.8rem; color: #94a3b8;">Sản phẩm của: <br><b style="color:#003366">Lương Tấn Phát</b> | Xã Hòa Khánh</p>
            </div>
        </div>''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- GIAO DIỆN CHÍNH (SAU KHI LOGGED) ---
else:
    with st.sidebar:
        st.markdown('<div style="text-align: center; margin-bottom: 20px;">', unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=120)
        st.markdown(f'''
            <div style="margin-top: 15px;">
                <span style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase;">Cán bộ trực máy</span>
                <h3 style="color: #00d4ff; margin:0; font-weight: 800;">{st.session_state.user}</h3>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        # Các nút chức năng
        if st.button("🗑️ LÀM MỚI HỘI THOẠI"):
            st.session_state.messages = []
            st.rerun()
            
        if st.button("🚪 ĐĂNG XUẤT"):
            st.session_state.logged = False
            st.rerun()
        
        st.markdown(f'''
            <div style="margin-top: 60px; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 15px;">
                <p style='color: #87ceeb; font-size:0.75rem; line-height: 1.4;'>
                    <i class="fas fa-shield-halved"></i> <b>Bảo mật:</b> Dữ liệu hội thoại được mã hóa đầu cuối bởi Hòa Khánh AI.
                </p>
            </div>
        ''', unsafe_allow_html=True)

    # Khung Chat chính
    st.markdown(f'''
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid #003366; padding-bottom: 15px; margin-bottom: 30px;">
            <h2 style='color: #003366; margin: 0; font-weight: 800;'>
                <i class='fas fa-microchip'></i> TRỢ LÝ SỐ HÒA KHÁNH
            </h2>
            <span style="background: #003366; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">ACTIVE</span>
        </div>
    ''', unsafe_allow_html=True)

    # Hiển thị tin nhắn
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Hỏi tôi về nghiệp vụ công đoàn, văn bản hành chính..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Đang truy vấn trí tuệ nhân tạo..."):
                try:
                    res = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": f"Bạn là trợ lý AI công đoàn xã Hòa Khánh. Trả lời chuyên nghiệp, súc tích. Gọi người dùng là Anh/Chị {st.session_state.user}."},
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.1-8b-instant"
                    )
                    ans = res.choices[0].message.content
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except:
                    st.error("🛑 Hệ thống AI đang bảo trì, vui lòng quay lại sau!")

# --- CHÂN TRANG (LUÔN HIỂN THỊ) ---
st.markdown(f'''
    <div class="digital-footer">
        <i class="fas fa-satellite-dish"></i> Hệ thống Trợ lý số phục vụ Chuyển đổi số cơ sở<br>
        Tác giả: <b>Lương Tấn Phát</b> | Hòa Khánh Digital AI © 2026
    </div>
''', unsafe_allow_html=True)
