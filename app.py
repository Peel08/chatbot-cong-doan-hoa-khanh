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

# --- 2. DÁN URL GOOGLE SCRIPT MỚI CỦA ANH VÀO ĐÂY ---
WEBHOOK_URL = "DÁN_LINK_WEB_APP_CỦA_ANH_VÀO_ĐÂY"

# --- 3. CSS SIÊU CÔNG NGHỆ (TỐI ƯU MOBILE 100%) ---
st.markdown('''
<style>
    .stApp {
        background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%);
    }

    /* FIX NÚT BẤM VÀ MENU: Chữ trắng sáng loáng, thiết kế bo góc hiện đại */
    div.stButton > button {
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
    }

    .gradient-text {
        background: -webkit-linear-gradient(#004494, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 1.5rem;
    }

    /* Khung Form nhập phản ánh */
    .report-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #0047AB;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Style hiển thị bản quyền tác giả */
    .author-footer {
        text-align: center;
        margin-top: 25px;
        padding-top: 15px;
        border-top: 1px solid #ddd;
        color: #666;
        font-size: 0.85rem;
        line-height: 1.4;
    }
    .author-footer b { color: #0047AB; }

    /* Ẩn hoàn toàn Sidebar của Streamlit để giao diện mobile gọn gàng */
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarCollapsedControl"] { display: none; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# --- 4. KHỞI TẠO CLIENT & SESSION STATE ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Thiếu API Key trong phần Secrets của Streamlit!")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
if "logged" not in st.session_state: st.session_state.logged = False
if "show_report_form" not in st.session_state: st.session_state.show_report_form = False

# Cơ sở tri thức bất biến về tác giả hệ thống để huấn luyện AI
AUTHOR_INFO = """
Hệ thống Hòa Khánh Digital AI được thiết kế, xây dựng và phát triển hoàn toàn bởi Lương Tấn Phát. 
Đây là giải pháp công nghệ số hóa tiên phong nhằm phục vụ công tác điều hành, quản lý nghiệp vụ Công đoàn và phong trào Thanh niên tại cơ sở xã Hòa Khánh vào năm 2026.
Mọi vấn đề liên quan đến bản quyền công nghệ, vận hành kỹ thuật và cơ sở dữ liệu đều do nhà phát triển Lương Tấn Phát chịu trách nhiệm.
"""

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- 5. GIAO DIỆN MÀN HÌNH ĐĂNG NHẬP ---
if not st.session_state.logged:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f'''
            <div style="text-align:center;">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="160" style="filter: drop-shadow(0 10px 15px rgba(0,0,0,0.1));">
            </div>
            <h2 style="text-align:center; color:#004494; font-weight:800; margin-top:12px;">HÒA KHÁNH DIGITAL AI</h2>
            <p style="text-align:center; color:#666; margin-bottom:25px;">Trợ lý thông minh số hóa công tác Công đoàn</p>
        ''', unsafe_allow_html=True)
        
        name = st.text_input("👤 Định danh cán bộ / đoàn viên:", placeholder="Nhập họ tên của bạn...", key="login_name")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
            else:
                st.warning("⚠️ Vui lòng nhập tên của bạn để hệ thống xác thực dữ liệu cán bộ!")

        st.markdown(f'''
            <div class="author-footer">
                Thiết kế & Phát triển: <b>Lương Tấn Phát</b><br>
                Hòa Khánh Digital AI System © 2026
            </div>
        ''', unsafe_allow_html=True)

# --- 6. GIAO DIỆN CHÍNH SAU KHI KÍCH HOẠT ---
else:
    st.markdown(f"<span class='gradient-text'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)
    
    # HIỂN THỊ ĐẦY ĐỦ 4 CHỨC NĂNG NHIỆM VỤ NHANH
    st.markdown("<p style='font-size:0.85rem; color:#666; margin-top:10px; font-weight:600;'>CHỌN NHIỆM VỤ NHANH:</p>", unsafe_allow_html=True)
    
    col_1, col_2 = st.columns(2)
    with col_1:
        if st.button("📩 GỬI PHẢN ÁNH"):
            st.session_state.show_report_form = True  # Mở form nhập phản ánh
            st.rerun()
        if st.button("📝 ĐĂNG KÝ"):
            st.session_state.show_report_form = False
            add_message("user", "Cho tôi hỏi thủ tục đăng ký tham gia tổ chức công đoàn.")
            st.rerun()
            
    with col_2:
        if st.button("🆘 HỖ TRỢ"):
            st.session_state.show_report_form = False
            add_message("user", "Hướng dẫn tôi cách yêu cầu hỗ trợ kỹ thuật hoặc giải đáp nghiệp vụ.")
            st.rerun()
        if st.button("🗑️ LÀM MỚI CHAT"):
            st.session_state.messages = []
            st.session_state.show_report_form = False
            st.rerun()

    st.markdown("---")

    # --- ĐOẠN HIỂN THỊ FORM NHẬP SỐ ĐIỆN THOẠI & NỘI DUNG (KHI BẤM NÚT) ---
    if st.session_state.show_report_form:
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown("<b style='color:#0047AB;'>🏛️ HỆ THỐNG TIẾP NHẬN PHẢN ÁNH KIẾN NGHỊ</b>", unsafe_allow_html=True)
        
        # Tạo form bằng Streamlit để lấy đồng thời 2 thông tin
        with st.form("form_phan_anh", clear_on_submit=True):
            phone_input = st.text_input("📞 Nhập số điện thoại của Anh/Chị:", placeholder="Ví dụ: 0912345xxx")
            content_input = st.text_area("📝 Nội dung phản ánh kiến nghị:", placeholder="Nhập chi tiết nội dung muốn gửi đến Chủ tịch Công đoàn...")
            submit_button = st.form_submit_with_rows_cols = st.form_submit_button("🚀 XÁC NHẬN GỬI CHO CHỦ TỊCH")
            
            if submit_button:
                if not phone_input or not content_input:
                    st.error("⚠️ Vui lòng điền đầy đủ cả Số điện thoại và Nội dung phản ánh!")
                else:
                    with st.status("🚀 Hệ thống đang gửi dữ liệu bảo mật về trang quản trị..."):
                        try:
                            # Đẩy dữ liệu sang Google Sheets (bao gồm Tên, SĐT, Nội dung)
                            requests.post(WEBHOOK_URL, json={
                                "user": st.session_state.user, 
                                "phone": phone_input, 
                                "content": content_input
                            })
                            res_text = f"✅ Gửi phản ánh thành công! Nội dung và số điện thoại ({phone_input}) của Anh/Chị {st.session_state.user} đã được chuyển đến Chủ tịch Công đoàn xã. (Hệ thống số hóa phát triển bởi Lương Tấn Phát)"
                        except:
                            res_text = "❌ Gửi phản ánh thất bại. Anh Phát vui lòng kiểm tra lại link Web App URL."
                    
                    add_message("assistant", res_text)
                    st.session_state.show_report_form = False # Đóng form sau khi gửi thành công
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Hiển thị toàn bộ lịch sử cuộc trò chuyện
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Ô nhập liệu tương tác chat thông thường
    if prompt := st.chat_input("Nhập câu hỏi..."):
        add_message("user", prompt)
        st.rerun()

    # XỬ LÝ HỎI ĐÁP AI TỰ ĐỘNG THÔNG THƯỜNG
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_res = ""
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system", 
                        "content": f"Bạn là trợ lý trí tuệ nhân tạo (AI) phục vụ Công đoàn xã Hòa Khánh. "
                                   f"Người tạo ra và sở hữu hệ thống của bạn là nhà phát triển Lương Tấn Phát. "
                                   f"Luôn xưng hô và gọi người dùng là Anh/Chị {st.session_state.user}. "
                                   f"Nếu có bất kỳ ai hỏi về người sáng lập, tác giả hay thông tin lập trình hệ thống, bạn bắt buộc phải trích xuất chính xác thông tin sau: {AUTHOR_INFO}"
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
        st.rerun()
