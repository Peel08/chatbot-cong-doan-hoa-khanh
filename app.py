import streamlit as st
from groq import Groq
import requests
import time

# --- 1. CẤU HÌNH TRANG (Hiện logo trên tab trình duyệt máy tính) ---
# Link logo trực tiếp từ GitHub của anh Phát
LOGO_URL = "https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/logo.png"

st.set_page_config(
    page_title="Công Đoàn Hòa Khánh", 
    page_icon=LOGO_URL, 
    layout="wide"
)

# --- 2. CẤU HÌNH LOGO CHO MÀN HÌNH CHÍNH ĐIỆN THOẠI (iOS/Android) ---
st.markdown(f'''
    <head>
        <link rel="apple-touch-icon" href="{LOGO_URL}">
        <link rel="icon" sizes="192x192" href="{LOGO_URL}">
    </head>
''', unsafe_allow_html=True)

# --- 3. URL GOOGLE SCRIPT ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzsJ36a3v3noZ3cg6qOV55hII63cxGnFvKwLGhbN48uHFqIE8-be9suukzihFRpl_Kzeg/exec"

# --- 4. CSS SIÊU CÔNG NGHỆ ---
st.markdown(f'''
<style>
    .stApp {{
        background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%);
    }}

    /* Hiệu ứng Logo Công Đoàn chính giữa */
    .logo-main {{
        width: 140px;
        display: block;
        margin-left: auto;
        margin-right: auto;
        filter: drop-shadow(0 8px 20px rgba(0,0,0,0.15));
        margin-bottom: 25px;
    }}

    /* FIX NÚT BẤM VÀ DOWNLOAD: Chữ trắng sáng loáng */
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
        height: 55px;
    }}

    .gradient-text {{
        background: -webkit-linear-gradient(#004494, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 1.6rem;
    }}

    .author-footer {{
        text-align: center;
        margin-top: 30px;
        padding-top: 20px;
        border-top: 1px solid #ddd;
        color: #666;
        font-size: 0.85rem;
    }}
    .author-footer b {{ color: #0047AB; }}

    [data-testid="stSidebar"] {{ display: none; }}
    [data-testid="stSidebarCollapsedControl"] {{ display: none; }}
    #MainMenu, footer, header {{visibility: hidden;}}
</style>
''', unsafe_allow_html=True)

# --- 5. KHỞI TẠO CLIENT & SESSION ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Thiếu API Key!")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
if "logged" not in st.session_state: st.session_state.logged = False
if "form_type" not in st.session_state: st.session_state.form_type = None

# Mẫu đơn từ tài liệu của anh
MAU_DON_TEXT = """CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
---------------
ĐƠN GIA NHẬP CÔNG ĐOÀN

Kính gửi: Ban Chấp hành Công đoàn cơ sở xã Hòa Khánh.
... (Nội dung mẫu đơn 5a anh cung cấp) ...
"""

CHU_TICH_INFO = """
Thông tin về Chủ tịch Công đoàn cơ sở xã Hòa Khánh:
- Họ và tên: Nguyễn Thanh Toàn
- Chức vụ: Phó Chủ tịch Ủy ban MTTQ xã đồng thời Chủ tịch Công đoàn cơ sở xã Hòa Khánh.
- Địa điểm làm việc: số 779, Quốc lộ N2, xã Hòa Khánh, tỉnh Tây Ninh - UBND xã Hòa Khánh.
- Số điện thoại: 0797627616
"""

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- 6. GIAO DIỆN ĐĂNG NHẬP ---
if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f'<img src="{LOGO_URL}" class="logo-main">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="text-align:center; color:#004494; font-weight:800;">TRỢ LÝ ẢO CÔNG ĐOÀN</h2>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center; color:#666;">Xã Hòa Khánh - Số hóa bởi Lương Tấn Phát</p>', unsafe_allow_html=True)
        
        name = st.text_input("👤 Nhập họ tên để bắt đầu:", key="login_name")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()

# --- 7. GIAO DIỆN CHÍNH ---
else:
    # Logo nhỏ phía trên lời chào
    st.markdown(f'<div style="text-align:center;"><img src="{LOGO_URL}" width="70"></div>', unsafe_allow_html=True)
    st.markdown(f"### <span class='gradient-text'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)
    
    col_1, col_2 = st.columns(2)
    with col_1:
        if st.button("📩 GỬI PHẢN ÁNH"):
            st.session_state.form_type = "phan_anh"
            st.rerun()
        st.download_button(
            label="📝 TẢI MẪU ĐƠN ĐĂNG KÝ",
            data=MAU_DON_TEXT,
            file_name="Don_Gia_Nhap_Cong_Doan_Hoa_Khanh.txt",
            mime="text/plain"
        )
    with col_2:
        if st.button("🆘 HỖ TRỢ KHÓ KHĂN"):
            st.session_state.form_type = "ho_tro"
            st.rerun()
        if st.button("🗑️ LÀM MỚI CHAT"):
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")
    
    # Phần hiển thị lịch sử chat và xử lý AI (giữ nguyên logic cũ)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Nhập câu hỏi..."):
        add_message("user", prompt)
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            # Logic AI trả lời (đã tinh chỉnh bớt nhắc mẫu đơn)
            placeholder = st.empty()
            full_res = ""
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": f"Bạn là trợ lý ảo Công đoàn Hòa Khánh. Tác giả: Lương Tấn Phát. Chủ tịch: Nguyễn Thanh Toàn. Chỉ đưa mẫu đơn khi được hỏi."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                stream=True,
            )
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    full_res += chunk.choices[0].delta.content
                    placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
            add_message("assistant", full_res)
        st.rerun()
