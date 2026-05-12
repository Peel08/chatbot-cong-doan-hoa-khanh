import streamlit as st
from groq import Groq
from docx import Document
import os

# 1. Cấu hình trang - Căn giữa nội dung và tối ưu bố cục
st.set_page_config(
    page_title="Hòa Khánh Digital AI", 
    page_icon="🤖", 
    layout="centered", # Sử dụng "centered" để nội dung không bị quá rộng
    initial_sidebar_state="expanded"
)

# 2. Hệ thống CSS Premium (Custom UI V3.1 - Sửa lỗi vị trí và nâng cấp sang trọng)
st.markdown('''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;600;700&display=swap');

    /* Tối ưu hóa tổng thể ứng dụng */
    html, body, [class*="st-emotion-cache"] {
        font-family: 'Urbanist', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #eef2f7 0%, #dfe7f0 100%);
    }

    /* Ẩn Header, Footer và MainMenu của Streamlit để tăng sự chuyên nghiệp */
    header, footer, #MainMenu {visibility: hidden;}

    /* === SỬA LỖI VỊ TRÍ ĐĂNG NHẬP === */
    /* Container chính để ép nội dung */
    .stApp .block-container {
        padding-top: 2rem !important; /* Đưa nội dung sát lên đầu trang */
        padding-bottom: 2rem !important;
    }

    /* Wrapper đăng nhập mới - KHÔNG dùng flex căn giữa chiều cao */
    .login-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        margin-top: 0 !important; /* Đảm bảo không có khoảng trống trên cùng */
    }

    /* --- NÂNG CẤP GIAO DIỆN SANG TRỌNG --- */
    /* Card Đăng nhập phong cách Glassmorphism */
    .login-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px); /* Tăng độ mờ */
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 50px;
        border-radius: 30px;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.12); /* Đổ bóng mềm mại hơn */
        width: 100%;
        max-width: 500px;
        text-align: center;
        margin-top: 0 !important; /* Ép card sát lên robot */
        transition: transform 0.3s ease;
    }
    .login-card:hover {
        transform: translateY(-5px); /* Hiệu ứng hover nhẹ */
    }

    /* Hiệu ứng Robot Bay (Giữ nguyên nhưng tinh chỉnh) */
    .floating-robot {
        animation: float 4s ease-in-out infinite;
        filter: drop-shadow(0 15px 25px rgba(0, 68, 148, 0.35));
        margin-bottom: -10px !important; /* Ép sát card đăng nhập lên robot */
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(2deg); }
    }

    /* Nút bấm Premium - Kết hợp xanh navy và vàng gold */
    div.stButton > button {
        background: linear-gradient(90deg, #003366 0%, #004494 100%) !important; /* Xanh Navy */
        color: white !important;
        border-radius: 15px !important;
        border: 2px solid transparent !important; /* Viền trong */
        padding: 12px 24px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    /* Hiệu ứng Hover - Đổi màu viền vàng gold */
    div.stButton > button:hover {
        border-color: #ffd700 !important; /* Vàng Gold */
        box-shadow: 0 10px 20px rgba(0, 68, 148, 0.4);
    }

    /* --- SIDEBAR CHUYÊN NGHIỆP --- */
    [data-testid="stSidebar"] {
        background-color: #003366 !important;
        background-image: linear-gradient(180deg, #003366 0%, #002244 100%) !important;
    }
    
    .sidebar-content {
        color: white;
        text-align: center;
        padding: 20px;
    }

    /* --- BONG BÓNG CHAT CAO CẤP --- */
    [data-testid="stChatMessage"] {
        background-color: white !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06) !important;
        margin-bottom: 15px !important;
        border: 1px solid #e2e8f0 !important;
        transition: transform 0.2s ease;
    }
    [data-testid="stChatMessage"]:hover {
        transform: translateX(3px); /* Hiệu ứng hover nhẹ */
    }

    /* Thanh Chat Input - Tăng độ nhận diện */
    .stChatInputContainer {
        padding: 1rem 3rem !important;
        background: rgba(238, 242, 247, 0.8) !important; /* Nền input đồng bộ */
        border-top: 1px solid #cbd5e1;
    }
    .stChatInputContainer > div {
        border-radius: 25px !important;
        border: 1px solid #003366 !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05) !important;
    }

    /* Badge tác giả mới */
    .author-badge {
        font-size: 0.8rem;
        color: #64748b;
        text-align: center;
        margin-top: 2rem;
        border-top: 1px solid #cbd5e1;
        padding-top: 1rem;
    }
    .author-badge b { color: #003366; }
</style>
''', unsafe_allow_html=True)

# 3. Hàm nạp dữ liệu (Giữ nguyên logic của bạn)
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

# 4. Khởi tạo Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Chưa cấu hình GROQ_API_KEY trong secrets!")

# 5. Quản lý trạng thái
if "logged" not in st.session_state: st.session_state.logged = False
if "messages" not in st.session_state: st.session_state.messages = []

# 6. GIAO DIỆN ĐĂNG NHẬP (ĐÃ CHỈNH SỬA)
if not st.session_state.logged:
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    
    # Robot Mascot (Căn trên)
    st.markdown('<div class="floating-robot">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=180)
    st.markdown('</div>', unsafe_allow_html=True)

    # Login Card (Nâng cấp)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown("<h1 style='color: #003366; font-size: 2.2rem; margin-bottom: 5px;'>HÒA KHÁNH AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #004494; font-weight: 600; margin-bottom: 30px;'>TRỢ LÝ SỐ CÔNG ĐOÀN V3.1</p>", unsafe_allow_html=True)
    
    # Text input (Label ẩn)
    name = st.text_input("Định danh", placeholder="Nhập tên Anh/Chị để bắt đầu...", label_visibility="collapsed")
    
    # Nút bấm (Sẽ được CSS áp dụng)
    if st.button("KÍCH HOẠT HỆ THỐNG"):
        if name:
            st.session_state.user = name
            st.session_state.logged = True
            st.rerun()
        else:
            st.warning("Vui lòng danh xưng để Robot phục vụ!")
    
    # Author badge mới
    st.markdown(f'''
    <div class="author-badge">
        Phát triển bởi: <b>Lương Tấn Phát</b><br>
        <i>Chuyển đổi số Công đoàn xã Hòa Khánh</i>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

else:
    # 7. GIAO DIỆN CHAT CHÍNH (SIDEBAR & NỘI DUNG)
    with st.sidebar:
        st.markdown('<div style="text-align: center; padding: 20px 0;">', unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png", width=110)
        st.markdown(f"<h3 style='color: white;'>{st.session_state.user}</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #87ceeb; font-size: 0.9rem;'>Đã sẵn sàng hỗ trợ</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        st.markdown("<p style='color: white; font-weight: bold;'>TRUY CẬP NHANH</p>", unsafe_allow_html=True)
        
        # Nút truy cập nhanh mới có icon
        if st.button("📝 Mẫu Đơn Gia Nhập"):
            st.session_state.messages.append({"role": "user", "content": "Cho tôi mẫu đơn gia nhập công đoàn"})
            st.rerun()
            
        if st.button("📩 Gửi Phản Ánh/Kiến Nghị"):
            st.session_state.messages.append({"role": "user", "content": "Quy trình gửi phản ánh kiến nghị"})
            st.rerun()

        if st.button("⚖️ Quyền Lợi Người Lao Động"):
            st.session_state.messages.append({"role": "user", "content": "Tóm tắt quyền lợi người lao động"})
            st.rerun()
            
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        if st.button("🗑️ Làm mới hội thoại"):
            st.session_state.messages = []
            st.rerun()

    # KHÔNG GIAN CHAT - NÂNG CẤP TIÊU ĐỀ
    st.markdown(f'''
    <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 2px solid #003366; padding-bottom: 15px; margin-bottom: 20px;">
        <h2 style='color: #003366; margin: 0;'>🤖 Hòa Khánh Digital AI</h2>
        <span style="background: rgba(0, 51, 102, 0.1); color: #003366; padding: 5px 15px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">Hỗ trợ nghiệp vụ Công đoàn</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # Render tin nhắn (Hiệu ứng hover mới được CSS áp dụng)
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            # Xử lý hiển thị nút tải file (Cải tiến giao diện nút tải)
            if msg["role"] == "assistant" and "đơn gia nhập" in msg["content"].lower():
                target = "MAU 02- MẪU 5a+5b ĐƠN XIN GIA NHẬP CÔNG ĐOÀN.docx"
                if target in all_files:
                    with open(all_files[target], "rb") as f:
                        st.download_button(
                            label=f"📥 Tải xuống: {target}", 
                            data=f, 
                            file_name=target, 
                            key=f"dl_{idx}",
                            use_container_width=True # Nút tải rộng bằng container
                        )

    # Input người dùng
    if prompt := st.chat_input("Hãy hỏi tôi bất cứ điều gì về nghiệp vụ công đoàn..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # Phản hồi từ AI (Cải tiến spinner)
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Đang truy xuất dữ liệu từ cơ sở dữ liệu..."):
                try:
                    # System prompt tinh chỉnh
                    system_prompt = f"""Bạn là trợ lý AI công đoàn xã Hòa Khánh. 
                    Dùng dữ liệu sau để trả lời: {knowledge_context[:12000]}. 
                    Trả lời thân thiện, chuyên nghiệp, súc tích bằng tiếng Việt."""
                    
                    res = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": st.session_state.messages[-1]["content"]}
                        ],
                        model="llama-3.1-8b-instant"
                    )
                    ans = res.choices[0].message.content
                    st.markdown(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi hệ thống AI: {e}")

    # Footer trang chat mới
    st.markdown(f'''
    <div style="text-align:center; color:#94a3b8; font-size:0.8rem; margin-top:50px; padding-bottom: 20px; border-top: 1px solid #e2e8f0; padding-top: 15px;">
        Hệ thống hỗ trợ Công đoàn xã Hòa Khánh | Phiên bản Premium 3.1<br>
        Phát triển và vận hành bởi: <b>Lương Tấn Phát</b>
    </div>
    ''', unsafe_allow_html=True)
