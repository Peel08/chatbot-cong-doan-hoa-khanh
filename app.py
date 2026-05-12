import streamlit as st
from groq import Groq
from docx import Document # Thư viện để đọc file .docx
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="robot.png", layout="wide")

# 2. Hàm đọc toàn bộ dữ liệu từ thư mục data của Phát
@st.cache_resource
def load_knowledge_base():
    combined_text = ""
    data_folder = "data" 
    
    if os.path.exists(data_folder):
        for filename in os.listdir(data_folder):
            file_path = os.path.join(data_folder, filename)
            try:
                # Xử lý file .docx và .doc
                if filename.endswith(".docx") or filename.endswith(".doc"):
                    doc = Document(file_path)
                    full_text = []
                    for para in doc.paragraphs:
                        full_text.append(para.text)
                    combined_text += f"\n--- NỘI DUNG TỪ FILE {filename} ---\n"
                    combined_text += "\n".join(full_text) + "\n"
            except Exception as e:
                print(f"Không thể đọc file {filename}: {e}")
    
    return combined_text

# 3. CSS Giao diện Công nghệ (Giữ nguyên phong cách của Phát)
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #004494 0%, #001a35 100%) !important; }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { align-items: center !important; text-align: center !important; }
    .sidebar-text { color: #e0e0e0 !important; }
    .stButton > button {
        background: linear-gradient(90deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%) !important;
        color: white !important;
        border-radius: 20px !important;
        width: 100% !important;
        font-size: 0.85rem !important;
    }
    .robot-box { animation: float 3s ease-in-out infinite; display: flex; justify-content: center; width: 100%; }
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-15px); } 100% { transform: translateY(0px); } }
</style>
''', unsafe_allow_html=True)

# 4. Khởi tạo dữ liệu và API
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Lỗi: Bạn chưa cấu hình GROQ_API_KEY trong Secrets!")
    st.stop()

# Nạp dữ liệu từ thư mục data
knowledge_context = load_knowledge_base()

if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

# 5. Màn hình Đăng nhập
if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
    with col2:
        st.markdown('<div class="robot-box"><img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="200"></div>', unsafe_allow_html=True)
        name = st.text_input("Định danh Cán bộ/Đoàn viên:", placeholder="Nhập tên của bạn...")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()

# 6. Giao diện Chat chính sau khi đăng nhập
else:
    with st.sidebar:
        st.markdown('<div class="robot-box"><img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="110"></div>', unsafe_allow_html=True)
        st.markdown(f"<p class='sidebar-text'>Cán bộ truy cập: <b style='color:#00d4ff;'>{st.session_state.user}</b></p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        
        st.markdown("<p class='sidebar-text' style='font-size:0.8rem; opacity:0.7;'>TRA CỨU NHANH:</p>", unsafe_allow_html=True)
        
        # Các nút đề xuất lấy dữ liệu từ file trong thư mục data
        if st.button("📩 Phản ánh kiến nghị"):
            st.session_state.messages.append({"role": "user", "content": "Quy trình tiếp nhận phản ánh kiến nghị"})
            st.rerun()
        if st.button("🆘 Yêu cầu hỗ trợ"):
            st.session_state.messages.append({"role": "user", "content": "Hướng dẫn các bước yêu cầu hỗ trợ công đoàn"})
            st.rerun()
        if st.button("📝 Đăng ký Công đoàn"):
            st.session_state.messages.append({"role": "user", "content": "Cho tôi xem mẫu đơn gia nhập công đoàn"})
            st.rerun()

        if st.button("🗑️ XÓA PHIÊN CHAT"):
            st.session_state.messages = []
            st.rerun()

    st.markdown(f"<h4 style='color:#004494;'>Hệ thống Trợ lý số Hòa Khánh sẵn sàng!</h4>", unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Hỏi tôi về hồ sơ, thủ tục công đoàn..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # AI xử lý dựa trên "Não bộ" là thư mục data
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("AI đang tra cứu hồ sơ..."):
                try:
                    user_query = st.session_state.messages[-1]["content"]
                    
                    # Hệ thống Prompt hướng dẫn AI sử dụng dữ liệu từ file
                    system_prompt = f"""
                    Bạn là Trợ lý AI phục vụ Công đoàn xã Hòa Khánh. 
                    Dưới đây là nội dung kiến thức được trích xuất từ các file nghiệp vụ (Đơn mẫu, Quy trình, Tờ trình):
                    {knowledge_context[:15000]} 
                    
                    Hãy sử dụng thông tin trên để trả lời Anh/Chị {st.session_state.user}. 
                    Nếu người dùng hỏi về mẫu đơn, hãy trích dẫn các trường thông tin cần điền.
                    Nếu hỏi về quy trình, hãy nêu rõ các bước 1, 2, 3.
                    """

                    res = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_query}
                        ],
                        model="llama-3.1-8b-instant"
                    )
                    ans = res.choices[0].message.content
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                except Exception as e:
                    st.error(f"Lỗi kết nối AI: {e}")
