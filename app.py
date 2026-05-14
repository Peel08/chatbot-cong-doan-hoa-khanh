import streamlit as st
from groq import Groq
import requests
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Hòa Khánh Digital AI - Lương Tấn Phát", 
    page_icon="🤖", 
    layout="wide"
)

# --- 2. DÁN URL GOOGLE SCRIPT CỦA ANH VÀO ĐÂY ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzK8E15i3qrT5P8Xm0iJruhvb6pMhuYs7EuvmYbbYvb5EmmDp8b_eybi_NJ7ltG9FHUTQ/exec"

# --- 3. CSS SIÊU CÔNG NGHỆ (TỐI ƯU MOBILE 100%) ---
st.markdown('''
<style>
    .stApp {
        background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%);
    }

    /* NÚT KÍCH HOẠT: Chữ trắng sáng loáng */
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
        box-shadow: 0 4px 15px rgba(0, 71, 171, 0.3) !important;
        height: 50px;
    }

    .gradient-text {
        background: -webkit-linear-gradient(#004494, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 1.5rem;
    }

    /* Thông tin tác giả */
    .author-footer {
        text-align: center;
        margin-top: 20px;
        padding-top: 15px;
        border-top: 1px solid #ddd;
        color: #666;
        font-size: 0.85rem;
    }
    .author-footer b { color: #0047AB; }

    /* Ẩn các thành phần thừa của Streamlit */
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarCollapsedControl"] { display: none; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# --- 4. KHỞI TẠO CLIENT & SESSION ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Thiếu API Key trong phần Secrets của Streamlit!")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
if "logged" not in st.session_state: st.session_state.logged = False
if "is_reporting" not in st.session_state: st.session_state.is_reporting = False

# Dữ liệu tri thức về tác giả
AUTHOR_INFO = """
Hệ thống Hòa Khánh Digital AI được thiết kế và phát triển bởi Lương Tấn Phát. 
Đây là giải pháp số hóa phục vụ công tác Công đoàn và Thanh niên tại xã Hòa Khánh năm 2026.
Tác giả Lương Tấn Phát chịu trách nhiệm toàn bộ về kỹ thuật và nội dung số của hệ thống này.
"""

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- 5. MÀN HÌNH ĐĂNG NHẬP ---
if not st.session_state.logged:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f'''
            <div style="text-align:center;">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="160" style="filter: drop-shadow(0 10px 15px rgba(0,0,0,0.1));">
            </div>
            <h2 style="text-align:center; color:#004494; font-weight:800; margin-top:10px;">HÒA KHÁNH DIGITAL AI</h2>
            <p style="text-align:center; color:#666; margin-bottom:20px;">Trợ lý thông minh công tác Công đoàn</p>
        ''', unsafe_allow_html=True)
        
        name = st.text_input("👤 Danh tính của bạn:", placeholder="Nhập tên Anh/Chị...", key="login_name")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
            else:
                st.warning("⚠️ Vui lòng nhập tên để định danh cán bộ!")

        st.markdown(f'''
            <div class="author-footer">
                Kiến tạo bởi: <b>Lương Tấn Phát</b><br>
                Hòa Khánh Digital AI © 2026
            </div>
        ''', unsafe_allow_html=True)

# --- 6. GIAO DIỆN CHÍNH (SAU KHI ĐĂNG NHẬP) ---
else:
    st.markdown(f"<span class='gradient-text'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)
    
    # Khu vực nút chức năng nhanh
    st.markdown("<p style='font-size:0.85rem; color:#666; margin-top:10px;'>NHIỆM VỤ NHANH:</p>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📩 GỬI PHẢN ÁNH"):
            st.session_state.is_reporting = True
            add_message("assistant", f"Chào Anh/Chị {st.session_state.user}, mời Anh/Chị nhập nội dung phản ánh kiến nghị. Tôi sẽ chuyển trực tiếp đến Chủ tịch Công đoàn xã.")
            st.rerun()
    with col_b:
        if st.button("🗑️ LÀM MỚI CHAT"):
            st.session_state.messages = []
            st.session_state.is_reporting = False
            st.rerun()

    st.markdown("---")

    # Hiển thị lịch sử hội thoại
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Ô nhập liệu của người dùng
    if prompt := st.chat_input("Hỏi tôi hoặc nhập nội dung phản ánh..."):
        add_message("user", prompt)
        
        # KIỂM TRA NẾU ĐANG TRONG LUỒNG GỬI PHẢN ÁNH
        if st.session_state.is_reporting:
            with st.status("🚀 Đang gửi dữ liệu tới Chủ tịch..."):
                try:
                    # Gửi dữ liệu về Google Sheets qua Webhook URL
                    requests.post(WEBHOOK_URL, json={"user": st.session_state.user, "content": prompt})
                    res_text = f"✅ Đã ghi nhận! Phản ánh của Anh/Chị {st.session_state.user} đã được gửi thành công đến hệ thống quản trị của Chủ tịch xã Hòa Khánh. Cảm ơn Anh/Chị đã đóng góp ý kiến. (Sản phẩm bởi Lương Tấn Phát)"
                    st.session_state.is_reporting = False
                except:
                    res_text = "❌ Lỗi kết nối hệ thống. Anh Phát vui lòng kiểm tra lại URL Web App trong code."
            add_message("assistant", res_text)
            st.rerun()
        else:
            # XỬ LÝ AI TRẢ LỜI BÌNH THƯỜNG
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_res = ""
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system", 
                            "content": f"Bạn là trợ lý AI công đoàn xã Hòa Khánh. Người tạo ra bạn là Lương Tấn Phát. "
                                       f"Gọi người dùng là Anh/Chị {st.session_state.user}. "
                                       f"Nếu được hỏi về tác giả hoặc thông tin hệ thống, hãy trả lời: {AUTHOR_INFO}"
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
