import streamlit as st
from groq import Groq
from docx import Document
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="robot.png", layout="wide")

# 2. CSS Tùy chỉnh (Giữ nguyên phong cách của Phát)
st.markdown('''
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #004494 0%, #001a35 100%) !important; }
    .stButton > button {
        background: linear-gradient(90deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%) !important;
        color: white !important;
        border-radius: 20px !important;
        width: 100% !important;
    }
    .download-box {
        background-color: #ffffff;
        padding: 15px;
        border-left: 5px solid #0052D4;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
''', unsafe_allow_html=True)

# 3. Hàm nạp kiến thức và chuẩn bị file tải về
@st.cache_resource
def get_knowledge_and_files():
    data = {}
    knowledge_text = ""
    folder = "data"
    
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)
            # Lưu đường dẫn file để làm nút download
            data[filename] = path
            
            # Đọc nội dung cho AI học (chỉ file docx)
            try:
                if filename.endswith(".docx") or filename.endswith(".doc"):
                    doc = Document(path)
                    text = "\n".join([p.text for p in doc.paragraphs])
                    knowledge_text += f"\n--- TÀI LIỆU: {filename} ---\n{text}\n"
            except:
                pass
    return knowledge_text, data

knowledge_base, file_paths = get_knowledge_and_files()

# 4. Kết nối API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state: st.session_state.messages = []
if "user" not in st.session_state: st.session_state.user = "Cán bộ"

# 5. Giao diện Sidebar
with st.sidebar:
    st.markdown(f"<h3 style='color:white; text-align:center;'>🤖 TRỢ LÝ SỐ</h3>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Nút bấm đề xuất
    if st.button("📝 Đăng ký gia nhập Công đoàn"):
        st.session_state.messages.append({"role": "user", "content": "Tôi muốn xin mẫu đơn gia nhập công đoàn và hướng dẫn điền"})
        st.rerun()

# 6. Khu vực hiển thị nội dung Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Nếu AI trả lời về đơn gia nhập, hiện nút tải ngay dưới tin nhắn đó
        if "đơn gia nhập" in msg["content"].lower() and msg["role"] == "assistant":
            file_name = "MAU 02- MẪU 5a+5b ĐƠN XIN GIA NHẬP CÔNG ĐOÀN.docx"
            if file_name in file_paths:
                with open(file_paths[file_name], "rb") as f:
                    st.download_button(
                        label="📥 Tải xuống Mẫu đơn 02 (File Word)",
                        data=f,
                        file_name=file_name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

# 7. Xử lý nhập liệu
if prompt := st.chat_input("Nhập yêu cầu tại đây..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        # AI tra cứu trong kiến thức file của Phát
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": f"Bạn là trợ lý AI Công đoàn xã Hòa Khánh. Dựa vào dữ liệu: {knowledge_base[:10000]}, hãy trả lời chi tiết. Nếu người dùng hỏi về đơn, hãy báo là bạn đã đính kèm file tải về bên dưới."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant"
        )
        full_res = response.choices[0].message.content
        st.markdown(full_res)
        st.session_state.messages.append({"role": "assistant", "content": full_res})
        
        # Nếu câu trả lời có liên quan đến đơn gia nhập, hiện nút tải
        if "đơn gia nhập" in full_res.lower():
            file_name = "MAU 02- MẪU 5a+5b ĐƠN XIN GIA NHẬP CÔNG ĐOÀN.docx"
            if file_name in file_paths:
                with open(file_paths[file_name], "rb") as f:
                    st.download_button(
                        label="📥 Tải xuống Mẫu đơn 02 (File Word)",
                        data=f,
                        file_name=file_name,
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
