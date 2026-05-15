import streamlit as st
from groq import Groq
import requests
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Công Đoàn AI", 
    page_icon="🤖", 
    layout="wide"
)

# --- 2. CẤU HÌNH LOGO CHO MÀN HÌNH CHÍNH ĐIỆN THOẠI (iOS/Android) ---
st.markdown(f'''
    <head>
        <link rel="apple-touch-icon" href="logo.png">
        <link rel="icon" sizes="192x192" href="logo.png">
    </head>
''', unsafe_allow_html=True)

# --- 2. URL GOOGLE SCRIPT ---
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzsJ36a3v3noZ3cg6qOV55hII63cxGnFvKwLGhbN48uHFqIE8-be9suukzihFRpl_Kzeg/exec"

# --- 3. CSS SIÊU CÔNG NGHỆ ---
st.markdown('''
<style>
    .stApp {
        background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%);
    }

    div.stButton > button, div.stDownloadButton > button {
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

    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarCollapsedControl"] { display: none; }
    #MainMenu, footer, header {visibility: hidden;}
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

# Mẫu đơn từ file word anh Phát cung cấp
MAU_DON_TEXT = """CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
Độc lập - Tự do - Hạnh phúc
---------------
ĐƠN GIA NHẬP CÔNG ĐOÀN

Kính gửi: Ban Chấp hành Công đoàn cơ sở xã Hòa Khánh.

- Tên tôi là: .................................................. ; Nam/nữ :…..……...
- Sinh ngày: ………………………………. ; Dân tộc: …………..
- Quê quán: ……………………………………………………….
- Nơi ở hiện nay: ………………………………………………….
- Số CCCD: ………………………Số điện thoại: ……………….
- Nơi làm việc hiện nay: .....................................................
- Vị trí công việc đang làm: .................................................

Sau khi tìm hiểu Điều lệ Công đoàn Việt Nam, tôi tán thành và tự nguyện làm đơn gia nhập tổ chức Công đoàn Việt Nam.
Tôi xin hứa: Thực hiện tốt nhiệm vụ, quyền hạn của đoàn viên; chấp hành sự phân công của tổ chức, đóng đoàn phí đầy đủ.

Hòa Khánh, ngày 11 tháng 03 năm 2026
Người làm đơn (Ký, ghi rõ họ tên)
"""

CHU_TICH_INFO = """
Thông tin Chủ tịch Công đoàn xã Hòa Khánh:
- Họ và tên: Nguyễn Thanh Toàn
- Chức vụ: Chủ tịch Công đoàn cơ sở xã Hòa Khánh.
- SĐT: 0797627616 | Email: thanhtoan26091992@gmail.com
- Địa chỉ: số 779, Quốc lộ N2, xã Hòa Khánh, tỉnh Tây Ninh.
"""

AUTHOR_FOOTER_HTML = f'''
    <div class="author-footer">
        Hệ thống Công Đoàn số Xã Hòa Khánh - Tây Ninh © 2026<br>
        Thiết kế & Phát triển: <b>Lương Tấn Phát</b><br>
        <span style="font-size: 0.8rem;">Giải pháp số hóa nghiệp vụ Công đoàn cơ sở</span>
    </div>
'''

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- 5. GIAO DIỆN ĐĂNG NHẬP ---
if not st.session_state.logged:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.8, 1])
    with col2:
        st.markdown(f'''
            <div style="text-align:center;">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khánh/main/robot.png" width="160">
            </div>
            <h2 style="text-align:center; color:#004494; font-weight:800; margin-top:12px;">TRỢ LÝ ẢO CÔNG ĐOÀN XÃ HÒA KHÁNH</h2>
        ''', unsafe_allow_html=True)
        name = st.text_input("👤 Định danh:", key="login_name")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
        
        # CHÈN THÊM THÔNG TIN TÁC GIẢ Ở ĐÂY NHƯ ANH YÊU CẦU
        st.markdown(f'''
            <div class="author-footer">
                Thiết kế & Phát triển: <b>Lương Tấn Phát</b><br>
                Công Đoàn số Xã Hòa Khánh - Tây  © 2026
            </div>
        ''', unsafe_allow_html=True)

# --- 6. GIAO DIỆN CHÍNH ---
else:
    # CHÈN VÀO ĐÂY (Dòng 126) ĐỂ HIỆN LẠI CON ROBOT
    st.markdown(f'''
        <div style="text-align:center;">
            <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khánh/main/robot.png" width="250">
        </div>
    ''', unsafe_allow_html=True)
    st.markdown(f"### <span class='gradient-text'>Xin chào {st.session_state.user}! Tôi là trợ lý ảo Công đoàn xã Hòa Khánh, tôi có thể giúp gì cho anh/ chị</span>", unsafe_allow_html=True)
    
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
        if st.button("🗑️ LÀM MỚI CUỘC TRÒ CHUYỆN"):
            st.session_state.messages = []
            st.session_state.form_type = None
            st.rerun()

    st.markdown("---")

# --- 6.1 FORM TIẾP NHẬN PHẢN ÁNH KIẾN NGHỊ ---
    if st.session_state.form_type == "phan_anh":
        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown("<b style='color:#0047AB;'>🏛️ TIẾP NHẬN PHẢN ÁNH KIẾN NGHỊ</b>", unsafe_allow_html=True)
        with st.form("form_phan_anh", clear_on_submit=True):
            phone_input = st.text_input("📞 Số điện thoại liên hệ:", placeholder="Nhập số điện thoại...")
            content_input = st.text_area("📝 Nội dung phản ánh kiến nghị:", placeholder="Nhập chi tiết ý kiến muốn gửi lên Ban chấp hành...")
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

    # --- 6.2 FORM TIẾP NHẬN HỖ TRỢ KHÓ KHĂN ---
    if st.session_state.form_type == "ho_tro":
        st.markdown('<div class="danger-box">', unsafe_allow_html=True)
        st.markdown("<b style='color:#e53e3e;'>🆘 KHẢO SÁT TIẾP NHẬN ĐOÀN VIÊN CÓ HOÀN CẢNH KHÓ KHĂN</b>", unsafe_allow_html=True)
        with st.form("form_ho_tro_kho_khan", clear_on_submit=True):
            phone_input = st.text_input("📞 Số điện thoại người cần hỗ trợ:", placeholder="Nhập số điện thoại...")
            content_input = st.text_area("🏥 Trình bày hoàn cảnh khó khăn đề xuất hỗ trợ:", placeholder="Ví dụ: Đoàn viên bị tai nạn, đau ốm nằm viện, gia đình gặp sự cố...")
            submit_button = st.form_submit_button("🚨 GỬI YÊU CẦU CỨU TRỢ KHẨN CẤP")
            
            if submit_button:
                if not phone_input or not content_input:
                    st.error("⚠️ Vui lòng cung cấp số điện thoại và mô tả rõ hoàn cảnh khó khăn!")
                else:
                    with st.status("🚨 Hệ thống đang truyền phát thông tin khẩn cấp..."):
                        try:
                            requests.post(WEBHOOK_URL, json={
                                "user": st.session_state.user, "phone": phone_input, "content": content_input, "type": "Hỗ trợ khó khăn"
                            })
                            res_text = f"🚨 YÊU CẦU KHẨN CẤP ĐÃ GỬI ĐI! Thông tin khó khăn của Anh/Chị {st.session_state.user} (SĐT: {phone_input}) đã được chuyển tới Ban Thường vụ và Chủ tịch Công đoàn xã Hòa Khánh để lập phương án thăm hỏi, hỗ trợ sớm nhất. (Phát triển bởi Lương Tấn Phát)"
                        except:
                            res_text = "❌ Lỗi hệ thống kết nối. Anh Phát vui lòng cấu hình lại Web App."
                    add_message("assistant", res_text)
                    st.session_state.form_type = None
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

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
            system_instruction = (
                f"Bạn là trợ lý ảo chuyên nghiệp của Công đoàn xã Hòa Khánh. "
                f"Tác giả hệ thống: Lương Tấn Phát. Chủ tịch: Nguyễn Thanh Toàn. "
                f"Chỉ cung cấp chi tiết mẫu đơn khi người dùng hỏi về 'đăng ký', 'mẫu đơn' hoặc 'gia nhập'. "
                f"Các câu hỏi khác hãy trả lời ngắn gọn, thân thiện và đi thẳng vào vấn đề. "
                f"Người đang trò chuyện với bạn là Anh/Chị {st.session_state.user}."
            )
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_instruction},
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
