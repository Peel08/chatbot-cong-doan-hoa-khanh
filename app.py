import streamlit as st
from groq import Groq
from docx import Document
import os

# 1. Cấu hình trang
st.set_page_config(page_title="Hòa Khánh Digital AI", page_icon="robot.png", layout="wide")

# 2. CSS Siêu Công Nghệ & Căn giữa (GIỮ NGUYÊN)
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #004494 0%, #001a35 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] { align-items: center !important; text-align: center !important; }
    .login-wrapper { display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; margin-top: 20px; }
    .login-card { background: rgba(255, 255, 255, 0.95); padding: 35px; border-radius: 30px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); width: 100%; max-width: 550px; border: 1px solid #ffffff; text-align: center; }
    .robot-box { animation: float 3s ease-in-out infinite; display: flex; justify-content: center; width: 100%; margin-bottom: 20px; }
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-15px); } 100% { transform: translateY(0px); } }
    div.stButton > button {
        background: linear-gradient(90deg, #0052D4 0%, #4364F7 50%, #6FB1FC 100%) !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        height: 45px !important;
        width: 100% !important;
        font-weight: bold !important;
        margin-bottom: 10px;
    }
    .sidebar-text { color: #e0e0e0 !important; text-align: center; }
    .digital-footer { text-align: center; color: #5d6d7e; font-size: 0.85rem; margin-top: 50px; padding: 20px; border-top: 1px solid rgba(0,0,0,0.05); }
    #MainMenu, footer, header {visibility: hidden;}
</style>
''', unsafe_allow_html=True)

# 3. Hàm nạp dữ liệu (Tránh lỗi nếu thư mục data chưa có file)
@st.cache_resource
def load_data():
    knowledge = ""
    file_map = {}
    if os.path.exists("data"):
        for fn in os.listdir("data"):
            path = os.path.join("data", fn)
            file_map[fn] = path
            if fn.endswith((".docx", ".doc")):
                try:
                    doc = Document(path)
                    knowledge += f"\nFILE: {fn}\n" + "\n".join([p.text for p in doc.paragraphs])
                except: pass
    return knowledge, file_map

knowledge_context, all_files = load_data()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 4. Quản lý trạng thái
if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

# 5. MÀN HÌNH ĐĂNG NHẬP
if not st.session_state.logged:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
        st.markdown('<div class="robot-box"><img src="robot.png" width="200"></div>', unsafe_allow_html=True)
        st.markdown('''<div class="login-card">
            <h1 style='color: #004494; margin-bottom:5px;'>HÒA KHÁNH DIGITAL AI</h1>
            <p style="color: #666; font-weight: bold; margin-bottom: 20px;">Hệ thống Trợ lý số phục vụ Công đoàn & Chuyển đổi số</p>''', unsafe_allow_html=True)
        name = st.text_input("Định danh:", placeholder="Nhập họ tên tại đây...", label_visibility="collapsed")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()
        st.markdown(f'<p style="font-size: 0.85rem; color: #888; margin-top: 20px;">Phát triển bởi: <b>Lương Tấn Phát</b></p></div></div>', unsafe_allow_html=True)

else:
    # 6. SIDEBAR
    with st.sidebar:
        st.markdown('<div style="text-align: center;">', unsafe_allow_html=True)
        st.markdown('<div class="robot-box"><img src="robot.png" width="110"></div>', unsafe_allow_html=True)
        st.markdown(f"<p class='sidebar-text'>Cán bộ: <b style='color:#00d4ff;'>{st.session_state.user}</b></p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 20px 0;'>", unsafe_allow_html=True)
        
        st.markdown("<p class='sidebar-text' style='font-size:0.8rem; opacity:0.7;'>ĐỀ XUẤT NHANH:</p>", unsafe_allow_html=True)
        if st.button("📩 Phản ánh kiến nghị"):
            st.session_state.messages.append({"role": "user", "content": "Quy trình tiếp nhận phản ánh kiến nghị"})
            st.rerun()
        if st.button("🆘 Yêu cầu hỗ trợ"):
            st.session_state.messages.append({"role": "user", "content": "Các bước yêu cầu hỗ trợ công đoàn"})
            st.rerun()
        if st.button("📝 Đăng ký Công đoàn"):
            st.session_state.messages.append({"role": "user", "content": "Cho tôi mẫu đơn gia nhập công đoàn và hướng dẫn"})
            st.rerun()
            
        if st.button("🗑️ XÓA PHIÊN CHAT"):
            st.session_state.messages = []
            st.rerun()
        st.markdown(f'<div style="margin-top: 80px; opacity: 0.8;"><p class="sidebar-text" style="font-size:0.75rem;">Tác giả: <b>Lương Tấn Phát</b></p></div></div>', unsafe_allow_html=True)

    # 7. GIAO DIỆN CHAT & FIX LỖI DUPLICATE ID
    st.markdown(f"<h3 style='color: #004494;'><i class='fas fa-robot'></i> Chào Anh/Chị {st.session_state.user}, AI đã sẵn sàng!</h3>", unsafe_allow_html=True)
    
    # Duyệt qua lịch sử chat bằng enumerate để lấy chỉ số (idx) làm key cho nút
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            # Tự động hiện nút tải nếu nội dung nhắc đến đơn gia nhập
            if msg["role"] == "assistant" and "đơn gia nhập" in msg["content"].lower():
                target_file = "MAU 02- MẪU 5a+5b ĐƠN XIN GIA NHẬP CÔNG ĐOÀN.docx"
                if target_file in all_files:
                    try:
                        with open(all_files[target_file], "rb") as f:
                            # Thêm key=f"btn_{idx}" để mỗi nút có ID duy nhất, không bị lỗi Duplicate
                            st.download_button(
                                label="📥 Tải Mẫu đơn 02 (Word)", 
                                data=f, 
                                file_name=target_file,
                                key=f"dl_btn_{idx}" 
                            )
                    except: pass

    if prompt := st.chat_input("Nhập nội dung cần hỗ trợ..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            try:
                user_q = st.session_state.messages[-1]["content"]
                res = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": f"Bạn là trợ lý công đoàn Hòa Khánh. Dùng dữ liệu này để trả lời: {knowledge_context[:12000]}. Nếu hỏi về đơn gia nhập, hãy hướng dẫn và báo là đã đính kèm nút tải bên dưới."},
                        {"role": "user", "content": user_q}
                    ], model="llama-3.1-8b-instant")
                ans = res.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
                st.rerun()
            except: st.error("AI đang bận, thử lại sau nhé!")

st.markdown(f'<div class="digital-footer">Tác giả: <b>Lương Tấn Phát</b> | Dự án Chuyển đổi số cơ sở</div>', unsafe_allow_html=True)
