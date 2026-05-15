import streamlit as st
from groq import Groq
import requests
import time

# --- 1. CẤU HÌNH ĐƯỜNG DẪN LOGO CHUẨN ---
# Anh kiểm tra kỹ link này, phải có chữ 'raw' thì máy tính mới đọc được ảnh
LOGO_URL = "https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/logo.png"

# Cấu hình hiện logo trên Tab máy tính (Favicon)
st.set_page_config(
    page_title="Công Đoàn Hòa Khánh", 
    page_icon=LOGO_URL, 
    layout="wide"
)

# --- 2. CẤU HÌNH LOGO CHO MÀN HÌNH ĐIỆN THOẠI (App Icon) ---
st.markdown(f'''
    <head>
        <link rel="apple-touch-icon" href="{LOGO_URL}">
        <link rel="icon" sizes="192x192" href="{LOGO_URL}">
    </head>
''', unsafe_allow_html=True)

# --- 3. CSS GIAO DIỆN SANG TRỌNG ---
st.markdown(f'''
<style>
    .stApp {{
        background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%);
    }}

    /* Hiển thị logo chính giữa màn hình */
    .logo-container {{
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }}
    .logo-main {{
        width: 150px;
        filter: drop-shadow(0 8px 20px rgba(0,0,0,0.15));
    }}

    /* Nút bấm đồng bộ màu xanh Công đoàn */
    div.stButton > button, div.stDownloadButton > button {{
        background: linear-gradient(90deg, #0047AB 0%, #0072ff 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        height: 55px;
        box-shadow: 0 4px 15px rgba(0, 71, 171, 0.2) !important;
    }}

    .gradient-text {{
        background: -webkit-linear-gradient(#004494, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 1.6rem;
    }}

    #MainMenu, footer, header {{visibility: hidden;}}
</style>
''', unsafe_allow_html=True)

# --- 4. NỘI DUNG MẪU ĐƠN TỪ FILE ANH CUNG CẤP ---
# Nội dung được trích xuất chính xác từ file word anh gửi [cite: 3, 4, 5, 7, 14, 17]
MAU_DON_TEXT = """CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc [cite: 3]
---------------
ĐƠN GIA NHẬP CÔNG ĐOÀN [cite: 4]

Kính gửi: Ban Vận động thành lập CĐCS Xã Hòa Khánh. [cite: 5]

- Tên tôi là: .................................................. [cite: 7]
- Sinh ngày: ………………………………. [cite: 8]
- Số CCCD: ………………………Số điện thoại: ………………. [cite: 11]

Sau khi tìm hiểu Điều lệ Công đoàn Việt Nam, tôi tán thành và tự nguyện làm đơn gia nhập tổ chức Công đoàn Việt Nam. [cite: 14]

Hòa Khánh, ngày 11 tháng 3 năm 2026 [cite: 17]
Người làm đơn (Ký, ghi rõ họ tên) [cite: 17]
"""

# --- 5. LOGIC ĐĂNG NHẬP ---
if "logged" not in st.session_state: st.session_state.logged = False

if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        # Ép hiện logo bằng HTML để chắc chắn nó hiện ra
        st.markdown(f'<div class="logo-container"><img src="{LOGO_URL}" class="logo-main"></div>', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align:center; color:#004494; font-weight:800;">TRỢ LÝ ẢO CÔNG ĐOÀN</h2>', unsafe_allow_html=True)
        
        name = st.text_input("👤 Nhập họ tên:", key="login_name")
        if st.button("🚀 KÍCH HOẠT"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
else:
    # --- 6. GIAO DIỆN CHÍNH ---
    st.markdown(f'<div style="text-align:center;"><img src="{LOGO_URL}" width="80"></div>', unsafe_allow_html=True)
    st.markdown(f"### <span class='gradient-text'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)
    
    col_1, col_2 = st.columns(2)
    with col_1:
        st.button("📩 GỬI PHẢN ÁNH")
        # Nút tải file đơn gia nhập lấy thông tin từ file anh gửi [cite: 1, 2]
        st.download_button(
            label="📝 TẢI MẪU ĐƠN ĐĂNG KÝ",
            data=MAU_DON_TEXT,
            file_name="Don_Gia_Nhap_Cong_Doan.txt",
            mime="text/plain"
        )
    with col_2:
        st.button("🆘 HỖ TRỢ KHÓ KHĂN")
        if st.button("🗑️ LÀM MỚI"):
            st.session_state.messages = []
            st.rerun()
    
    # (Phần xử lý AI và Chat tiếp theo phía dưới...)
