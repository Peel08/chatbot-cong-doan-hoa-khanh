import streamlit as st
from groq import Groq
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Hòa Khánh Digital AI", 
    page_icon="🤖", 
    layout="wide"
)

# --- 2. CSS SIÊU CÔNG NGHỆ (TỐI ƯU MOBILE 100% + THÔNG TIN TÁC GIẢ) ---
st.markdown('''
<style>
    .stApp {
        background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%);
    }

    /* FIX NÚT KÍCH HOẠT: Chữ trắng sáng loáng */
    div.stButton > button {
        background: linear-gradient(90deg, #0047AB 0%, #0072ff 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 20px !important;
        width: 100% !important;
        opacity: 1 !important;
        box-shadow: 0 4px 15px rgba(0, 71, 171, 0.3) !important;
    }

    /* Style cho thông tin tác giả dưới nút đăng nhập */
    .author-footer {
        text-align: center;
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid #ddd;
        color: #666;
        font-size: 0.85rem;
    }
    .author-footer b { color: #0047AB; }

    .gradient-text {
        background: -webkit-linear-gradient(#004494, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }

    /* Ẩn Sidebar hoàn toàn */
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarCollapsedControl"] { display: none; }

    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# --- 3. KHỞI TẠO CLIENT & SESSION ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Thiếu API Key!")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
if "logged" not in st.session_state: st.session_state.logged = False

# DỮ LIỆU TÁC GIẢ ĐỂ AI TRẢ LỜI
AUTHOR_INFO = """
Thông tin tác giả hệ thống:
- Họ tên: Lương Tấn Phát
- Quê quán: Ấp Hóc Thơm 1, xã Hòa Khánh, tỉnh Tây Ninh
- SĐT liên hệ: 0826674788
- Đơn vị: Công đoàn / Youth Union xã Hòa Khánh.
- Dự án: Hòa Khánh Digital AI - Số hóa công tác Công đoàn & Thanh niên.
- Năm phát triển: 2026.
- Vai trò: Nhà phát triển hệ thống và thiết kế trải nghiệm người dùng (Developer & UI/UX Designer).
"""
AUTHOR_INFO = """
Thông tin Chủ tịch Công đoàn xã Hòa Khánh:
- Họ tên: Nguyễn Thanh Toàn
- Quê quán: xã Hòa Khánh, tỉnh Tây Ninh
- SĐT liên hệ: 0797627616
- Chức vụ: Chủ tịch Công đoàn xã Hòa Khánh.
- Trụ sở làm việc : số 779, QUốc lộ N2, xã hòa khánh, tỉnh Tây Ninh
"""
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- 4. MÀN HÌNH ĐĂNG NHẬP ---
if not st.session_state.logged:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f'''
            <div style="text-align:center;">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="160" style="animation: float 3s ease-in-out infinite;">
            </div>
            <h2 style="text-align:center; color:#004494; font-weight:800;">HÒA KHÁNH DIGITAL AI</h2>
            <p style="text-align:center; color:#666;">Trợ lý thông minh công tác Công đoàn</p>
        ''', unsafe_allow_html=True)
        
        name = st.text_input("👤 Định danh của bạn:", placeholder="Nhập tên...", key="login_name")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()

        # Hiển thị thông tin tác giả ngay màn hình chính
        st.markdown(f'''
            <div class="author-footer">
                Tác giả & Thiết kế: <b>Lương Tấn Phát</b><br>
                Hòa Khánh Digital AI © 2026
            </div>
        ''', unsafe_allow_html=True)

# --- 5. GIAO DIỆN CHÍNH ---
else:
    st.markdown(f"### <span class='gradient-text'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size:0.8rem; color:#666; margin-bottom:5px;'>CHỌN NHIỆM VỤ NHANH:</p>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📩 PHẢN ÁNH"):
            add_message("user", "Tôi muốn gửi một phản ánh kiến nghị công việc.")
            st.rerun()
        if st.button("📝 ĐĂNG KÝ"):
            add_message("user", "Cho tôi hỏi thủ tục đăng ký tham gia công đoàn.")
            st.rerun()
    with col_b:
        if st.button("🆘 HỖ TRỢ"):
            add_message("user", "Hướng dẫn tôi cách yêu cầu hỗ trợ kỹ thuật.")
            st.rerun()
        if st.button("🗑️ LÀM MỚI"):
            st.session_state.messages = []
            st.rerun()

    st.markdown("---")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Nhập câu hỏi..."):
        add_message("user", prompt)
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_res = ""
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system", 
                        "content": f"Bạn là trợ lý AI công đoàn xã Hòa Khánh. Gọi người dùng là Anh/Chị {st.session_state.user}. "
                                   f"KHI NGƯỜI DÙNG HỎI VỀ TÁC GIẢ, NGƯỜI TẠO RA BẠN, HOẶC THÔNG TIN NHÀ PHÁT TRIỂN, "
                                   f"hãy trả lời đầy đủ nội dung sau: {AUTHOR_INFO}"
                    },
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
