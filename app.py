import streamlit as st
import google.generativeai as genai
import time

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

# 2. CSS CAO CẤP (Thêm style cho dòng chữ bản quyền)
st.markdown("""
    <style>
    .main { background-color: #f0f7ff; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0056b3 0%, #003d80 100%);
        box-shadow: 2px 0px 10px rgba(0,0,0,0.1);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* Hiệu ứng bong bóng chat */
    .stChatMessage {
        border-radius: 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
    }
    
    /* Dòng chữ bản quyền ở cuối trang */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #888;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        font-style: italic;
    }
    
    .main-title {
        background: linear-gradient(90deg, #0056b3, #00b4db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 40px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. KẾT NỐI AI
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-3-flash-preview")

# 4. THANH BÊN (SIDEBAR)
with st.sidebar:
    st.image("logo.png", width=150)
    st.markdown("### 🏛️ CÔNG ĐOÀN HÒA KHÁNH")
    st.write("---")
    
    if "user_name" not in st.session_state or not st.session_state.user_name:
        st.subheader("👤 Đăng nhập")
        name = st.text_input("Nhập Họ tên của bạn:")
        if st.button("🚀 Bắt đầu"):
            if name: 
                st.session_state.user_name = name
                st.rerun()
        st.stop()
    else:
        st.success(f"Chào bạn, **{st.session_state.user_name}**")
        st.info("📍 Trụ sở: Hòa Khánh, Tây Ninh")
        
        # Dòng ghi chú bản quyền trong Sidebar
        st.write("---")
        st.caption("🛠️ **Phiên bản:** 2.0 (AI Edition)")
        st.caption("👨‍💻 **Phát triển bởi:** Lương Tấn Phát")
        
        if st.button("🗑️ Làm mới hội thoại"):
            st.session_state.messages = []
            st.rerun()

# 5. GIAO DIỆN CHÍNH
st.markdown("<div class='main-title'>🇻🇳 TRỢ LÝ ẢO CÔNG ĐOÀN VIÊN</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555;'>Hệ thống trả lời tự động hỗ trợ cán bộ và công đoàn viên</p>", unsafe_allow_html=True)

# Hiển thị hội thoại
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. NHẬP LIỆU VÀ XỬ LÝ
if prompt := st.chat_input("Tôi có thể giúp gì cho bạn?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("⚡ Đang phân tích..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.warning("Hệ thống đang bận, Phát hãy thử lại sau vài giây.")

# 7. FOOTER (Dòng chữ bản quyền chạy dưới chân trang)
st.markdown("""
    <div class="footer">
        © 2026 Xây dựng và phát triển bởi Lương Tấn Phát - Công đoàn xã Hòa Khánh
    </div>
""", unsafe_allow_html=True)
