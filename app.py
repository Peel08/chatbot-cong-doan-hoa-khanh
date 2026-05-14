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
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzsJ36a3v3noZ3cg6qOV55hII63cxGnFvKwLGhbN48uHFqIE8-be9suukzihFRpl_Kzeg/exec"

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

    /* Khung Form nhập dữ liệu */
    .report-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #0047AB;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    .danger-box {
        background-color: #fff5f5;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #e53e3e;
        box-shadow: 0 4px 12px rgba(229,62,62,0.05);
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
if "form_type" not in st.session_state: st.session_state.form_type = None  # None, "phan_anh", hoặc "ho_tro"

# --- THÔNG TIN CHỦ TỊCH CÔNG ĐOÀN XÃ HÒA KHÁNH ---
CHU_TICH_INFO = """
Thông tin về Chủ tịch Công đoàn cơ sở xã Hòa Khánh:
- Họ và tên: [Điền tên Chủ tịch vào đây]
- Chức vụ: Chủ tịch Công đoàn cơ sở xã Hòa Khánh.
- Địa điểm làm việc: Phòng làm việc khối Đoàn thể - UBND xã Hòa Khánh.
- Số điện thoại liên hệ: [Điền SĐT Chủ tịch vào đây]
- Email: [Điền Email Chủ tịch vào đây]
- Nhiệm vụ: Chịu trách nhiệm chỉ đạo điều hành toàn bộ hoạt động bảo vệ quyền, lợi ích hợp pháp chính đáng của đoàn viên và người lao động trên địa bàn xã.
"""

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
            st.session_state.form_type = "phan_anh"  # Mở form phản ánh
            st.rerun()
        if st.button("📝 ĐĂNG KÝ"):
            st.session_state.form_type = None
            add_message("user", "Cho tôi hỏi thủ tục đăng ký tham gia tổ chức công đoàn.")
            st.rerun()
            
    with col_2:
        if st.button("🆘 HỖ TRỢ KHÓ KHĂN"):
            st.session_state.form_type = "ho_tro"  # Mở form hỗ trợ khó khăn (MỚI)
            st.rerun()
        if st.button("🗑️ LÀM MỚI CHAT"):
            st.session_state.messages = []
            st.session_state.form_type = None
            st.rerun()

    st.markdown("---")

    # --- 6.1 FORM NHẬP PHẢN ÁNH KIẾN NGHỊ ---
    if st.session_state.form_type == "phan_anh":
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown("<b style='color:#0047AB;'>🏛️ TIẾP NHẬN PHẢN ÁNH KIẾN NGHỊ Đoàn viên</b>", unsafe_allow_html=True)
        with st.form("form_phan_anh", clear_on_submit=True):
            phone_input = st.text_input("📞 Số điện thoại liên hệ:", placeholder="Nhập số điện thoại...")
            content_input = st.text_area("📝 Nội dung phản ánh kiến nghị:", placeholder="Nhập chi tiết ý kiến ý kiến muốn gửi lên Ban chấp hành...")
            submit_button = st.form_submit_button("🚀 GỬI BÁO CÁO PHẢN ÁNH")
            
            if submit_button:
                if not phone_input or not content_input:
                    st.error("⚠️ Vui lòng điền đầy đủ thông tin yêu cầu!")
                else:
                    with st.status("🚀 Đang chuyển dữ liệu về trang quản trị..."):
                        try:
                            requests.post(WEBHOOK_URL, json={
                                "user": st.session_state.user, "phone": phone_input, "content": content_input, "type": "Phản ánh kiến nghị"
                            })
                            res_text = f"✅ Đã ghi nhận thành công! Ý kiến phản ánh của Anh/Chị {st.session_state.user} (SĐT: {phone_input}) đã được chuyển thẳng tới Chủ tịch Công đoàn xã. (Phát triển bởi Lương Tấn Phát)"
                        except:
                            res_text = "❌ Gửi thất bại. Anh Phát kiểm tra lại link Web App URL."
                    add_message("assistant", res_text)
                    st.session_state.form_type = None
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 6.2 FORM TIẾP NHẬN HỖ TRỢ KHÓ KHĂN (TÍNH NĂNG MỚI ĐƯỢC PHÁT TRIỂN) ---
    if st.session_state.form_type == "ho_tro":
        st.markdown('<div class="danger-box">', unsafe_allow_html=True)
        st.markdown("<b style='color:#e53e3e;'>🆘 KHẢO SÁT TIẾP NHẬN ĐOÀN VIÊN CÓ HOÀN CẢNH KHÓ KHĂN</b>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:0.85rem; color:#666;'>Hệ thống hỗ trợ Công đoàn xã tiếp nhận thông tin trường hợp bị tai nạn lao động, bệnh hiểm nghèo, thiên tai hoặc hoạn nạn khẩn cấp.</p>", unsafe_allow_html=True)
        with st.form("form_ho_tro_kho_khan", clear_on_submit=True):
            phone_input = st.text_input("📞 Số điện thoại người cần hỗ trợ:", placeholder="Nhập số điện thoại để Công đoàn liên hệ...")
            content_input = st.text_area("🏥 Trình bày hoàn cảnh khó khăn đề xuất hỗ trợ:", placeholder="Ví dụ: Đoàn viên bị tai nạn, đau ốm nằm viện, gia đình gặp sự cố, cần hỗ trợ nhu yếu phẩm khẩn cấp...")
            submit_button = st.form_submit_button("🚨 GỬI YÊU CẦU CỨU TRỢ KHẨN CẤP")
            
            if submit_button:
                if not phone_input or not content_input:
                    st.error("⚠️ Vui lòng cung cấp số điện thoại và mô tả rõ hoàn cảnh khó khăn để Công đoàn xét duyệt!")
                else:
                    with st.status("🚨 Hệ thống đang truyền phát thông tin khẩn cấp..."):
                        try:
                            requests.post(WEBHOOK_URL, json={
                                "user": st.session_state.user, "phone": phone_input, "content": content_input, "type": "Hỗ trợ khó khăn"
                            })
                            res_text = f"🚨 YÊU CẦU KHẨN CẤP ĐÃ GỬI ĐI! Thông tin khó khăn của Anh/Chị {st.session_state.user} đã được chuyển tới Ban Thường vụ và Chủ tịch Công đoàn xã Hòa Khánh để lập phương án thăm hỏi, hỗ trợ sớm nhất. (Phát triển bởi Lương Tấn Phát)"
                        except:
                            res_text = "❌ Lỗi hệ thống kết nối. Anh Phát vui lòng cấu hình lại Web App."
                    add_message("assistant", res_text)
                    st.session_state.form_type = None
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
                                   f"Khi người dùng hỏi về Chủ tịch công đoàn, thông tin liên hệ của chủ tịch hoặc ai điều hành công đoàn xã, hãy trả lời chính xác thông tin sau: {CHU_TICH_INFO} "
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
