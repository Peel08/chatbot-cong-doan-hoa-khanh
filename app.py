import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang (Phải ở dòng 1)
st.set_page_config(page_title="Công đoàn Hòa Khánh", page_icon="🇻🇳", layout="centered")

# 2. CSS làm đẹp giao diện và sửa lỗi màu chữ
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    [data-testid="stSidebar"] { background-color: #0056b3; }
    [data-testid="stSidebar"] * { color: white !important; }
    /* Ô nhập liệu trong Sidebar màu đen */
    [data-testid="stSidebar"] input { color: black !important; }
    .stChatMessage { border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

# 3. Kết nối AI (Sửa lỗi NotFound bằng cách dùng tên chuẩn)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # Sử dụng tên model chuẩn xác nhất
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
else:
    st.error("Chưa cấu hình API Key trong Secrets!")
    st.stop()

# 4. Quản lý Đăng nhập và Tin nhắn
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Giao diện Sidebar
with st.sidebar:
    # Dự phòng logo
    try:
        st.image("logo.png", width=120)
    except:
        st.image("https://upload.wikimedia.org/wikipedia/vi/thumb/c/cb/Logo_Cong_doan_Viet_Nam.svg/1200px-Logo_Cong_doan_Viet_Nam.svg.png", width=120)
    
    st.title("CÔNG ĐOÀN HÒA KHÁNH")
    
    if not st.session_state.user_name:
        st.subheader("👤 Đăng nhập")
        name = st.text_input("Nhập tên của bạn:", key="login_name", placeholder="Họ và tên")
        if st.button("Bắt đầu"):
            if name:
                st.session_state.user_name = name
                st.rerun()
        st.stop()
    else:
        st.success(f"Chào bạn, {st.session_state.user_name}")
        st.write("📍 Hòa Khánh, Tây Ninh")
        if st.button("🗑️ Xóa lịch sử"):
            st.session_state.messages = []
            st.rerun()

# 5. Giao diện Chat chính
st.markdown("<h2 style='text-align: center; color: #0056b3;'>🤖 TRỢ LÝ CÔNG ĐOÀN</h2>", unsafe_allow_html=True)

# Hiển thị tin nhắn cũ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. Xử lý câu hỏi
if prompt := st.chat_input("Hỏi tôi về chính sách công đoàn..."):
    # Hiển thị tin user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI phản hồi
    with st.chat_message("assistant"):
        with st.spinner("Đang suy nghĩ..."):
            try:
                # Gửi prompt kèm vai trò cán bộ xã
                response = model.generate_content(f"Bạn là trợ lý công đoàn xã Hòa Khánh. Hãy trả lời thân thiện cho {st.session_state.user_name}: {prompt}")
                ans_text = response.text
                st.markdown(ans_text)
                st.session_state.messages.append({"role": "assistant", "content": ans_text})
            except Exception as e:
                # Nếu vẫn lỗi NotFound, thử dùng bản dự phòng cực mạnh
                try:
                    model_backup = genai.GenerativeModel("gemini-pro")
                    response = model_backup.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except:
                    st.error("Lỗi kết nối AI. Phát hãy kiểm tra lại API Key nhé!")
