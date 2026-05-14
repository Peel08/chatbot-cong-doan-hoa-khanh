import streamlit as st
from groq import Groq
import os

# 1. THIẾT LẬP CẤU HÌNH TRANG CHUẨN PREMIUM
st.set_page_config(
    page_title="Hòa Khánh Digital AI - Lương Tấn Phát", 
    page_icon="🏛️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. HỆ THỐNG GIAO DIỆN LUXURY (SỬ TRÍ CHI TIẾT TỪNG PIXEL)
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;800&display=swap');

    /* Nền tảng và Font chữ chủ đạo */
    html, body, [class*="st-emotion-cache"] {
        font-family: 'Montserrat', sans-serif;
    }
    .stApp {
        background: linear-gradient(160deg, #f0f4f8 0%, #d9e2ec 100%);
    }

    /* Sidebar thiết kế kiểu Business Dark */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001e3c 0%, #003366 100%) !important;
        border-right: 2px solid #ffd700 !important;
    }

    /* Glassmorphism cho khung Login */
    .login-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 40px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 20px 40px rgba(0, 30, 60, 0.15);
        text-align: center;
        margin: auto;
    }

    /* Hiệu ứng Nút bấm Gold-Gradient */
    div.stButton > button {
        background: linear-gradient(90deg, #003366 0%, #0056b3 100%) !important;
        color: #ffffff !important;
        border: 1px solid #ffd700 !important;
        border-radius: 12px !important;
        height: 50px !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
        transition: 0.3s all ease;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3);
        border-color: #ffffff !important;
    }

    /* Khung chat mượt mà */
    [data-testid="stChatMessage"] {
        border-radius: 15px !important;
        border: 1px solid #e1e8ed !important;
        background: white !important;
        padding: 20px !important;
    }

    /* Footer cố định phong cách chuyên nghiệp */
    .premium-footer {
        text-align: center;
        padding: 25px;
        color: #486581;
        font-size: 0.85rem;
        border-top: 1px solid #bcccdc;
        margin-top: 50px;
    }
    .premium-footer b { color: #003366; }

    /* Ẩn các menu mặc định để tăng tính thương hiệu riêng */
    header, footer, #MainMenu {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 3. KHO DỮ LIỆU CHÍNH XÁC (NGUỒN TRI THỨC CỦA CHATBOT)
# Anh Phát hãy dán các văn bản quy định của xã/đoàn vào đây
KNOWLEDGE_BASE = """
DANH MỤC DỮ LIỆU CÔNG ĐOÀN XÃ HÒA KHÁNH (CẬP NHẬT 2026):
1. VỀ TỔ CHỨC: Công đoàn xã Hòa Khánh trực thuộc Liên đoàn Lao động huyện.
2. CHẾ ĐỘ PHÚC LỢI: Thăm hỏi đoàn viên ốm đau, hiếu hỷ theo quy chế chi tiêu nội bộ năm 2026.
3. CHUYỂN ĐỔI SỐ: Dự án "Hòa Khánh Digital AI" do Lương Tấn Phát phát triển nhằm số hóa thủ tục hành chính.
4. ĐIỀU LỆ ĐOÀN: Tuân thủ theo các hướng dẫn mới nhất về đại hội công đoàn các cấp nhiệm kỳ 2023-2028.
(Ghi chú: Anh dán càng chi tiết văn bản vào đây, AI càng trả lời chính xác)
"""

# 4. KẾT NỐI API GROQ
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("🔑 Vui lòng kiểm tra lại GROQ_API_KEY trong file secrets.toml!")
    st.stop()

# 5. QUẢN LÝ TRẠNG THÁI HỆ THỐNG
if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

# --- GIAO DIỆN ĐĂNG NHẬP (LOGIN) ---
if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_login, _ = st.columns([1, 1.5, 1])
    
    with col_login:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        # Sử dụng logo robot của anh Phát
        st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=160)
        st.markdown("<h1 style='color: #003366; margin-bottom: 5px;'>HÒA KHÁNH AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #0056b3; font-weight: 600; letter-spacing: 2px;'>KỶ NGUYÊN SỐ CÔNG ĐOÀN V4.0</p>", unsafe_allow_html=True)
        
        name = st.text_input("ĐỊNH DANH CÁN BỘ", placeholder="Nhập họ tên...", label_visibility="collapsed")
        
        if st.button("KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
            else:
                st.warning("⚠️ Vui lòng cung cấp danh tính cán bộ!")
        
        st.markdown(f'''
            <div style="margin-top: 30px; border-top: 1px solid #d1d5db; padding-top: 20px;">
                <p style="font-size: 0.75rem; color: #6b7280;">Sản phẩm tâm huyết của:<br>
                <b style="color:#003366; font-size: 1rem;">LƯƠNG TẤN PHÁT</b><br>Hòa Khánh Digital AI</p>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- GIAO DIỆN LÀM VIỆC CHÍNH ---
else:
    with st.sidebar:
        st.markdown(f'''
            <div style="text-align: center; padding: 20px;">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="100">
                <p style="color: #ffd700; margin-top: 10px; font-weight: 600;">CÁN BỘ ĐANG TRỰC</p>
                <h3 style="color: white; margin: 0;">{st.session_state.user}</h3>
            </div>
        ''', unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        if st.button("🗑️ LÀM MỚI HỘI THOẠI"):
            st.session_state.messages = []
            st.rerun()
            
        if st.button("🚪 ĐĂNG XUẤT HỆ THỐNG"):
            st.session_state.logged = False
            st.rerun()
            
        st.markdown('''
            <div style="position: fixed; bottom: 20px; width: 220px; padding: 15px; background: rgba(255,255,255,0.05); border-radius: 10px;">
                <p style="color: #87ceeb; font-size: 0.7rem; margin: 0;">
                <i class="fas fa-user-shield"></i> Tác giả: <b>Lương Tấn Phát</b><br>Hệ thống bảo mật bởi AI 2026</p>
            </div>
        ''', unsafe_allow_html=True)

    # Tiêu đề trang chính
    st.markdown(f'''
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 3px solid #003366; padding-bottom: 10px; margin-bottom: 25px;">
            <h2 style='color: #003366; margin: 0;'>
                <i class="fas fa-landmark"></i> TRỢ LÝ SỐ CÔNG ĐOÀN HÒA KHÁNH
            </h2>
            <div style="background: #003366; color: #ffd700; padding: 5px 15px; border-radius: 10px; font-weight: 800; font-size: 0.9rem;">
                V4.0 PREMIUM
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Hiển thị tin nhắn
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Xử lý tin nhắn và Truy vấn tri thức
    if prompt := st.chat_input("Hỏi về nghiệp vụ, văn bản, hướng dẫn công đoàn..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Đang truy vấn kho dữ liệu Hòa Khánh..."):
                try:
                    res = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system", 
                                "content": f"Bạn là Trợ lý AI chuyên sâu của Công đoàn xã Hòa Khánh. "
                                           f"Chỉ trả lời dựa trên dữ liệu này: {KNOWLEDGE_BASE}. "
                                           f"Xưng hô: Anh/Chị {st.session_state.user}. "
                                           f"Cuối câu trả lời thỉnh thoảng nhắc lại đây là hệ thống số hóa của Lương Tấn Phát."
                            },
                            {"role": "user", "content": prompt}
                        ],
                        model="llama-3.3-70b-versatile"
                    )
                    ans = res.choices[0].message.content
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except:
                    st.error("🛑 Kết nối gián đoạn. Anh Phát vui lòng kiểm tra lại API Key!")

# --- CHÂN TRANG BẢN QUYỀN (LUÔN HIỂN THỊ) ---
st.markdown(f'''
    <div class="premium-footer">
        <i class="fas fa-shield-alt"></i> Hệ thống Trợ lý AI phục vụ Chuyển đổi số Cơ sở<br>
        Bản quyền thiết kế & phát triển: <b>Lương Tấn Phát</b> | Hòa Khánh Digital AI © 2026
    </div>
''', unsafe_allow_html=True)
