import streamlit as st
import google.generativeai as genai
import time

# 1. CẤU HÌNH TRANG CHUẨN
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

# 2. CSS CAO CẤP: Phối màu Gradient xanh Công đoàn và tạo khối (Card)
st.markdown("""
    <style>
    /* Tổng thể nền */
    .main { background-color: #f0f7ff; }
    
    /* Tùy chỉnh Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0056b3 0%, #003d80 100%);
        box-shadow: 2px 0px 10px rgba(0,0,0,0.1);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] input { color: black !important; border-radius: 10px; }

    /* Bong bóng chat */
    .stChatMessage {
        background-color: white !important;
        border-radius: 20px !important;
        padding: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        margin-bottom: 10px !important;
    }
    
    /* Tiêu đề chính */
    .main-title {
        background: linear-gradient(90deg, #0056b3, #00b4db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 40px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Làm đẹp các khung hướng dẫn */
    .guide-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #0056b3;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. KẾT NỐI AI (Dùng Gemini 3 Flash)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-3-flash-preview")
else:
    st.error("⚠️ Thiếu API Key!")
    st.stop()

# 4. QUẢN LÝ PHIÊN
if "user_name" not in st.session_state: st.session_state.user_name = None
if "messages" not in st.session_state: st.session_state.messages = []

# 5. THANH BÊN (SIDEBAR) XỊN
with st.sidebar:
    st.image("logo.png", width=150)
    st.markdown("### 🏛️ CÔNG ĐOÀN HÒA KHÁNH")
    st.write("---")
    
    if not st.session_state.user_name:
        st.subheader("👤 Đăng nhập hệ thống")
        name = st.text_input("Nhập Họ tên để bắt đầu:", placeholder="VD: Lương Tấn Phát")
        if st.button("🚀 Kích hoạt Trợ lý"):
            if name: 
                st.session_state.user_name = name
                st.rerun()
        st.stop()
    else:
        st.success(f"Chào bạn, **{st.session_state.user_name}**")
        st.info("📍 Trụ sở: Hòa Khánh, Tây Ninh")
        if st.button("🗑️ Làm mới hội thoại"):
            st.session_state.messages = []
            st.rerun()

# 6. GIAO DIỆN CHÁNH (MAIN UI)
st.markdown("<div class='main-title'>🇻🇳 TRỢ LÝ ẢO CÔNG ĐOÀN VIÊN</div>", unsafe_allow_html=True)

# Khung hướng dẫn giống VNPT nhưng đẹp hơn
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class='guide-box'>
        <b>📋 Tra cứu thủ tục</b><br>
        Hỗ trợ giải đáp các bước thực hiện hồ sơ hành chính, bảo hiểm, thai sản...
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class='guide-box'>
        <b>📜 Chính sách mới</b><br>
        Cập nhật các quy định mới nhất từ Tổng Liên đoàn Lao động Việt Nam.
    </div>
    """, unsafe_allow_html=True)

# Hiển thị hội thoại
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Xử lý nhập liệu
if prompt := st.chat_input(f"Chào {st.session_state.user_name}, tôi có thể giúp gì cho bạn?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Đang phân tích dữ liệu..."):
            for attempt in range(3):
                try:
                    # Gợi ý AI trả lời chuyên nghiệp
                    context = f"Bạn là cán bộ Công đoàn xã Hòa Khánh. Trả lời chu đáo cho {st.session_state.user_name}: "
                    response = model.generate_content(context + prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    break
                except Exception as e:
                    if "429" in str(e) and attempt < 2:
                        time.sleep(3)
                        continue
                    else:
                        st.warning("⚠️ Máy chủ đang bận xử lý dữ liệu lớn. Phát vui lòng thử lại sau 30 giây.")
                        break
