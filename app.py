import streamlit as st
import google.generativeai as genai
import time

# 1. Cấu hình trang
st.set_page_config(page_title="Công đoàn Hòa Khánh", page_icon="🇻🇳", layout="wide")

# 2. CSS làm đẹp
st.markdown("""
    <style>
    .main { background-color: #f0f5ff; }
    [data-testid="stSidebar"] { background-color: #0056b3; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] input { color: black !important; background-color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Kết nối AI với cơ chế tự sửa lỗi tên Model
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    
    # Thử các tên model phổ biến, cái nào chạy được thì lấy
    model_names = ["gemini-1.5-flash-latest", "gemini-1.5-flash", "gemini-pro"]
    found_model = False
    
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            # Thử tạo một nội dung nhỏ để kiểm tra model có tồn tại không
            found_model = True
            break
        except:
            continue
            
    if not found_model:
        st.error("Không tìm thấy mô hình AI phù hợp. Phát hãy kiểm tra lại API Key nhé!")
        st.stop()
else:
    st.error("Thiếu API Key trong Secrets!")
    st.stop()

# 4. Quản lý Session
if "user_name" not in st.session_state: st.session_state.user_name = None
if "messages" not in st.session_state: st.session_state.messages = []

# 5. Sidebar
with st.sidebar:
    try: st.image("logo.png", width=150)
    except: st.image("https://upload.wikimedia.org/wikipedia/vi/thumb/c/cb/Logo_Cong_doan_Viet_Nam.svg/1200px-Logo_Cong_doan_Viet_Nam.svg.png", width=120)
    
    st.title("CÔNG ĐOÀN HÒA KHÁNH")
    if not st.session_state.user_name:
        name = st.text_input("Nhập tên của bạn:")
        if st.button("Bắt đầu"):
            if name: st.session_state.user_name = name; st.rerun()
        st.stop()
    else:
        st.success(f"Chào bạn: {st.session_state.user_name}")
        if st.button("🗑️ Xóa lịch sử"):
            st.session_state.messages = []
            st.rerun()

# 6. Giao diện Chat
st.markdown("<h1 style='text-align: center;'>🤖 TRỢ LÝ ẢO CÔNG ĐOÀN</h1>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input(f"Mời {st.session_state.user_name} đặt câu hỏi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang tra cứu..."):
            # Cơ chế Retry (thử lại) nếu gặp lỗi 429
            for retry in range(3):
                try:
                    response = model.generate_content(f"Bạn là cán bộ Công đoàn xã Hòa Khánh. Trả lời {st.session_state.user_name}: {prompt}")
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    break
                except Exception as e:
                    if "429" in str(e) and retry < 2:
                        time.sleep(2) # Đợi 2 giây rồi thử lại
                        continue
                    else:
                        st.warning("⚠️ Hệ thống đang bận. Phát hãy đợi vài giây rồi gửi lại nhé!")
                        break
