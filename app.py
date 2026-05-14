import streamlit as st
from groq import Groq
import requests
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Hòa Khánh Digital AI", 
    page_icon="🤖", 
    layout="wide"
)

# --- 2. DÁN URL GOOGLE SCRIPT CỦA ANH VÀO ĐÂY ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzK8E15i3qrT5P8Xm0iJruhvb6pMhuYs7EuvmYbbYvb5EmmDp8b_eybi_NJ7ltG9FHUTQ/exec"

# --- 3. CSS SIÊU CÔNG NGHỆ ---
st.markdown('''
<style>
    .stApp { background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%); }
    div.stButton > button {
        background: linear-gradient(90deg, #0047AB 0%, #0072ff 100%) !important;
        color: white !important; font-weight: 800 !important; border-radius: 12px !important;
        width: 100% !important; box-shadow: 0 4px 15px rgba(0, 71, 171, 0.2) !important;
        height: 52px; border: none !important;
    }
    .gradient-text {
        background: -webkit-linear-gradient(#004494, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 1.5rem;
    }
    .author-footer { text-align: center; margin-top: 25px; padding-top: 15px; border-top: 1px solid #ddd; color: #666; font-size: 0.85rem; }
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# --- 4. KHỞI TẠO ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Thiếu API Key trong Secrets!")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
if "logged" not in st.session_state: st.session_state.logged = False
if "is_reporting" not in st.session_state: st.session_state.is_reporting = False

AUTHOR_INFO = "Hệ thống Hòa Khánh Digital AI được phát triển bởi Lương Tấn Phát phục vụ công tác Công đoàn xã Hòa Khánh năm 2026."

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- 5. MÀN HÌNH ĐĂNG NHẬP ---
if not st.session_state.logged:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f'<div style="text-align:center;"><img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="160"></div>', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#004494; font-weight:800;'>HÒA KHÁNH DIGITAL AI</h2>", unsafe_allow_html=True)
        name = st.text_input("👤 Định danh:", placeholder="Nhập tên...", key="login_name")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
        st.markdown(f'<div class="author-footer">Thiết kế bởi: <b>Lương Tấn Phát</b><br>Hòa Khánh Digital AI © 2026</div>', unsafe_allow_html=True)

# --- 6. GIAO DIỆN CHÍNH ---
else:
    st.markdown(f"<span class='gradient-text'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.85rem; color:#666; margin-top:10px;'>NHIỆM VỤ NHANH:</p>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📩 GỬI PHẢN ÁNH"):
            st.session_state.is_reporting = True
            add_message("assistant", f"Mời Anh/Chị {st.session_state.user} nhập nội dung phản ánh. Tôi sẽ gửi tới Chủ tịch xã.")
            st.rerun()
        if st.button("📝 ĐĂNG KÝ"):
            add_message("user", "Cho tôi hỏi thủ tục đăng ký tham gia công đoàn.")
            st.rerun()
    with c2:
        if st.button("🆘 HỖ TRỢ"):
            add_message("user", "Hướng dẫn tôi cách yêu cầu hỗ trợ kỹ thuật.")
            st.rerun()
        if st.button("🗑️ LÀM MỚI CHAT"):
            st.session_state.messages = []
            st.session_state.is_reporting = False
            st.rerun()

    st.markdown("---")

    # Hiển thị hội thoại
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Ô nhập liệu thủ công
    prompt = st.chat_input("Hỏi tôi hoặc nhập nội dung phản ánh...")
    if prompt:
        add_message("user", prompt)
        st.rerun()

    # --- LOGIC TỰ ĐỘNG PHẢN HỒI KHI CÓ TIN NHẮN MỚI TỪ USER ---
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        last_user_msg = st.session_state.messages[-1]["content"]
        
        # 1. Nếu là phản ánh -> Gửi tới Google Sheet
        if st.session_state.is_reporting:
            with st.chat_message("assistant"):
                with st.status("🚀 Đang gửi dữ liệu tới Chủ tịch..."):
                    try:
                        requests.post(WEBHOOK_URL, json={"user": st.session_state.user, "content": last_user_msg})
                        res_text = f"✅ Đã gửi thành công! Nội dung của Anh/Chị {st.session_state.user} đã được chuyển tới Chủ tịch xã. (Tác giả: Lương Tấn Phát)"
                        st.session_state.is_reporting = False
                    except:
                        res_text = "❌ Lỗi kết nối. Anh Phát kiểm tra lại Webhook URL nhé."
                st.markdown(res_text)
                add_message("assistant", res_text)
        
        # 2. Nếu là câu hỏi thường -> Gọi AI trả lời
        else:
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_res = ""
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": f"Bạn là trợ lý AI công đoàn Hòa Khánh của Lương Tấn Phát. Gọi người dùng là Anh/Chị {st.session_state.user}. Tác giả: {AUTHOR_INFO}"},
                        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    ],
                    stream=True
                )
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_res += chunk.choices[0].delta.content
                        placeholder.markdown(full_res + "▌")
                placeholder.markdown(full_res)
                add_message("assistant", full_res)
