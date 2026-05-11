import streamlit as st
import google.generativeai as genai
import time

# =========================================================
# 1. CẤU HÌNH TRANG (DÒNG ĐẦU TIÊN)
# =========================================================
st.set_page_config(page_title="Công đoàn Hòa Khánh AI", page_icon="🇻🇳", layout="wide")

# =========================================================
# 2. CSS LÀM ĐẸP GIAO DIỆN
# =========================================================
st.markdown("""
    <style>
    .main { background-color: #f0f5ff; }
    .stChatMessage { border-radius: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    h1 { color: #0056b3; font-family: 'Segoe UI', sans-serif; text-align: center; }
    
    /* Giao diện Thanh bên (Sidebar) */
    [data-testid="stSidebar"] { background-color: #0056b3; }
    [data-testid="stSidebar"] * { color: white !important; }
    
    /* Ô NHẬP TÊN: Chữ đen, nền trắng để nhìn rõ */
    [data-testid="stSidebar"] input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Làm đẹp ảnh Logo */
    [data-testid="stSidebar"] img {
        border-radius: 50%;
        background: white;
        padding: 5px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 3. KẾT NỐI AI & QUẢN LÝ PHIÊN
# =========================================================
if "GOOGLE_API_KEY" not in st.secrets:
    st.error("⚠️ Bạn chưa dán API Key vào mục Secrets của Streamlit!")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Thử dùng bản Flash, nếu lỗi 429 sẽ hiện thông báo nhẹ nhàng
model = genai.GenerativeModel("gemini-3-flash-preview")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_name" not in st.session_state:
    st.session_state.user_name = None

# =========================================================
# 4. THANH BÊN (SIDEBAR) VỚI LOGO.PNG
# =========================================================
with st.sidebar:
    # Sử dụng file logo.png bạn đã upload lên GitHub
    try:
        st.image("logo.png", width=150)
    except:
        # Nếu file logo.png lỗi, dùng tạm link dự phòng để web không sập
        st.image("https://upload.wikimedia.org/wikipedia/vi/thumb/c/cb/Logo_Cong_doan_Viet_Nam.svg/1200px-Logo_Cong_doan_Viet_Nam.svg.png", width=120)
    
    st.markdown("## CÔNG ĐOÀN HÒA KHÁNH")
    st.write("---")

    if not st.session_state.user_name:
        st.subheader("👤 Đăng nhập")
        name = st.text_input("Nhập Họ tên của bạn:", placeholder="VD: Lương Tấn Phát")
        if st.button("Bắt đầu"):
            if name:
                st.session_state.user_name = name
                st.rerun()
        st.info("Vui lòng nhập tên để bắt đầu")
        st.stop()
    else:
        st.success(f"Chào bạn: {st.session_state.user_name}")
        st.write("📍 Hòa Khánh, Tây Ninh")
        if st.button("🗑️ Xóa lịch sử"):
            st.session_state.messages = []
            st.rerun()

# =========================================================
# 5. GIAO DIỆN CHÁNH & XỬ LÝ CHAT
# =========================================================
st.markdown("<h1>🤖 TRỢ LÝ ẢO CÔNG ĐOÀN VIÊN</h1>", unsafe_allow_html=True)

# Hiển thị lại lịch sử trò chuyện
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ô nhập câu hỏi chính
if prompt := st.chat_input(f"Mời {st.session_state.user_name} đặt câu hỏi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang suy nghĩ..."):
            try:
                # Gửi yêu cầu cho AI
                context = f"Bạn là cán bộ Công đoàn xã Hòa Khánh. Người đang hỏi tên là {st.session_state.user_name}. Hãy trả lời thân thiện, chính xác."
                response = model.generate_content(f"{context}\n\nCâu hỏi: {prompt}")
                ans_text = response.text
                
                st.markdown(ans_text)
                st.session_state.messages.append({"role": "assistant", "content": ans_text})
            
            except Exception as e:
                # Xử lý lỗi 429 (Hết lượt dùng) một cách lịch sự
                if "429" in str(e):
                    st.warning("⚠️ Hệ thống đang bận vì có nhiều người hỏi cùng lúc. Phát hãy đợi khoảng 30-60 giây rồi nhấn gửi lại nhé!")
                else:
                    st.error(f"Lỗi hệ thống: {str(e)}")
