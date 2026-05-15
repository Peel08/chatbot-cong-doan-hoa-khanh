import streamlit as st
from groq import Groq
import requests
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Công Đoàn AI - Hòa Khánh", 
    page_icon="🇻🇳", 
    layout="wide"
)

# --- 2. URL GOOGLE SCRIPT ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzsJ36a3v3noZ3cg6qOV55hII63cxGnFvKwLGhbN48uHFqIE8-be9suukzihFRpl_Kzeg/exec"

# Link Logo Công Đoàn Việt Nam (PNG không nền)
LOGO_CONG_DOAN = "https://upload.wikimedia.org/wikipedia/vi/thumb/c/ca/Logo_Cong_doan_Viet_Nam.svg/1200px-Logo_Cong_doan_Viet_Nam.svg.png"

# --- 3. CSS SIÊU CÔNG NGHỆ ---
st.markdown(f'''
<style>
    .stApp {{
        background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%);
    }}

    /* Hiệu ứng Logo Công Đoàn */
    .logo-img {{
        width: 120px;
        display: block;
        margin-left: auto;
        margin-right: auto;
        filter: drop-shadow(0 5px 15px rgba(0,0,0,0.1));
        margin-bottom: 20px;
    }}

    div.stButton > button, div.stDownloadButton > button {{
        background: linear-gradient(90deg, #0047AB 0%, #0072ff 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 20px !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(0, 71, 171, 0.2) !important;
        height: 52px;
    }}

    .gradient-text {{
        background: -webkit-linear-gradient(#004494, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 1.5rem;
    }}

    .author-footer {{
        text-align: center;
        margin-top: 25px;
        padding-top: 15px;
        border-top: 1px solid #ddd;
        color: #666;
        font-size: 0.85rem;
    }}

    [data-testid="stSidebar"] {{ display: none; }}
    [data-testid="stSidebarCollapsedControl"] {{ display: none; }}
    #MainMenu, footer, header {{visibility: hidden;}}
</style>
''', unsafe_allow_html=True)

# --- 4. KHỞI TẠO CLIENT & SESSION ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Thiếu API Key!")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
if "logged" not in st.session_state: st.session_state.logged = False
if "form_type" not in st.session_state: st.session_state.form_type = None

# Mẫu đơn lấy từ tài liệu của anh [cite: 2, 4]
MAU_DON_TEXT = """CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
---------------
ĐƠN GIA NHẬP CÔNG ĐOÀN 

Kính gửi: Ban Chấp hành Công đoàn cơ sở xã Hòa Khánh. [cite: 5, 6]

- Tên tôi là: .................................................. [cite: 7]
- Sinh ngày: ………………………………. ; Dân tộc: ………….. [cite: 8]
- Quê quán: ………………………………………………………. [cite: 9]
- Nơi ở hiện nay: …………………………………………………. [cite: 10]
- Số CCCD: ………………………Số điện thoại: ………………. [cite: 11]
- Vị trí công việc đang làm: ................................................. [cite: 13]

Tôi tự nguyện làm đơn gia nhập tổ chức Công đoàn Việt Nam. [cite: 14]
Tôi xin hứa: Thực hiện tốt nhiệm vụ, quyền hạn của đoàn viên; chấp hành Điều lệ và đóng đoàn phí đầy đủ. [cite: 15, 16]

Hòa Khánh, ngày 11 tháng 03 năm 2026 [cite: 17]
Người làm đơn (Ký, ghi rõ họ tên) [cite: 17]
"""

# --- 5. GIAO DIỆN ĐĂNG NHẬP ---
if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        # Hiện Logo Công Đoàn thay cho robot
        st.markdown(f'<img src="{LOGO_CONG_DOAN}" class="logo-img">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="text-align:center; color:#004494; font-weight:800;">TRỢ LÝ ẢO CÔNG ĐOÀN</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center; color:#666;">Xã Hòa Khánh, huyện Đức Hòa, tỉnh Long An</p>', unsafe_allow_html=True)
        
        name = st.text_input("👤 Nhập họ tên để bắt đầu:", key="login_name")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()

# --- 6. GIAO DIỆN CHÍNH ---
else:
    # Logo nhỏ phía trên lời chào
    st.markdown(f'<div style="text-align:center;"><img src="{LOGO_CONG_DOAN}" width="60"></div>', unsafe_allow_html=True)
    st.markdown(f"### <span class='gradient-text'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)
    
    col_1, col_2 = st.columns(2)
    with col_1:
        if st.button("📩 GỬI PHẢN ÁNH"):
            st.session_state.form_type = "phan_anh"
            st.rerun()
        
        st.download_button(
            label="📝 TẢI MẪU ĐƠN ĐĂNG KÝ",
            data=MAU_DON_TEXT,
            file_name="Don_Gia_Nhap_Cong_Doan.txt",
            mime="text/plain"
        )
            
    with col_2:
        if st.button("🆘 HỖ TRỢ KHÓ KHĂN"):
            st.session_state.form_type = "ho_tro"
            st.rerun()
        if st.button("🗑️ LÀM MỚI CHAT"):
            st.session_state.messages = []
            st.rerun()

    # (Các phần xử lý Form và AI giữ nguyên như bản trước để đảm bảo tính năng)
