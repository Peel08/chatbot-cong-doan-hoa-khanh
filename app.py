import streamlit as st
from groq import Groq
import time

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Hòa Khánh Digital AI", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS & JAVASCRIPT ĐỂ ÉP HIỆN NÚT MENU (FIX TRIỆT ĐỂ) ---
st.markdown('''
<style>
    /* Nền ứng dụng */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #fdfbfb 0%, #ebedee 100%);
    }

    /* TẠO NÚT MENU NỔI (FLOATING MENU) - LUÔN HIỆN TRÊN ĐIỆN THOẠI */
    .floating-menu-btn {
        position: fixed;
        top: 12px;
        left: 12px;
        width: 45px;
        height: 45px;
        background: #0047AB;
        color: white;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999999;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        cursor: pointer;
        border: 2px solid rgba(255,255,255,0.2);
    }

    /* Ẩn tiêu đề mặc định và các nút thừa của Streamlit để lấy chỗ cho nút mới */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }
    
    /* Ép hiển thị nội dung Sidebar xịn mịn */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #002B5B 0%, #001524 100%) !important;
    }

    /* Nút Kích hoạt & Nhiệm vụ nhanh */
    div.stButton > button {
        background: linear-gradient(90deg, #0047AB 0%, #0072ff 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        text-transform: uppercase !important;
        opacity: 1 !important;
    }

    .gradient-text {
        background: -webkit-linear-gradient(#004494, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }

    #MainMenu, footer, header {visibility: hidden;}
</style>

<!-- Nút Menu HTML -->
<div class="floating-menu-btn" onclick="openSidebar()">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
        <line x1="3" y1="12" x2="21" y2="12"></line>
        <line x1="3" y1="6" x2="21" y2="6"></line>
        <line x1="3" y1="18" x2="21" y2="18"></line>
    </svg>
</div>

<script>
    function openSidebar() {
        // Tìm nút mũi tên ẩn của Streamlit và click vào nó
        const buttons = window.parent.document.getElementsByTagName('button');
        for (let i = 0; i < buttons.length; i++) {
            if (buttons[i].getAttribute('aria-label') === 'Open sidebar' || 
                buttons[i].querySelector('svg path[d^="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6-6-6z"]')) {
                buttons[i].click();
                break;
            }
        }
    }
</script>
''', unsafe_allow_html=True)

# --- 3. KHỞI TẠO CLIENT ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ Thiếu API Key!")
    st.stop()

if "messages" not in st.session_state: st.session_state.messages = []
if "logged" not in st.session_state: st.session_state.logged = False

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})

# --- 4. GIAO DIỆN CHÀO ---
if not st.session_state.logged:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.5, 1])
    with col2:
        st.markdown('<div style="text-align:center;"><img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="150"></div>', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#004494;'>HÒA KHÁNH DIGITAL AI</h2>", unsafe_allow_html=True)
        name = st.text_input("👤 Định danh của bạn:", placeholder="Nhập tên...", key="user_login_name")
        if st.button("🚀 KÍCH HOẠT HỆ THỐNG"):
            if name:
                st.session_state.user = name
                st.session_state.logged = True
                st.rerun()

# --- 5. GIAO DIỆN CHÍNH ---
else:
    with st.sidebar:
        st.markdown(f'''
            <div style="text-align:center; padding:10px;">
                <img src="https://raw.githubusercontent.com/peel08/chatbot-cong-doan-hoa-khanh/main/robot.png" width="80">
                <h3 style="color:white; margin-bottom:0;">{st.session_state.user}</h3>
                <p style="color:#00d4ff; font-size:0.8rem;">Cán bộ đang trực tuyến</p>
            </div>
            <hr style="opacity:0.2;">
        ''', unsafe_allow_html=True)

        st.markdown("<p style='color:white; font-size:0.7rem; opacity:0.6; margin-left:10px;'>NHIỆM VỤ NHANH</p>", unsafe_allow_html=True)
        
        suggestions = {
            "📩 Phản ánh kiến nghị": "Tôi muốn gửi một phản ánh kiến nghị công việc.",
            "🆘 Yêu cầu hỗ trợ": "Hướng dẫn tôi cách yêu cầu hỗ trợ kỹ thuật.",
            "📝 Đăng ký Công đoàn": "Cho tôi hỏi thủ tục đăng ký tham gia công đoàn.",
            "📜 Quy định chính sách": "Các chính sách mới nhất cho công đoàn viên là gì?"
        }

        for label, prompt_text in suggestions.items():
            if st.button(label, key=f"btn_{label}"):
                add_message("user", prompt_text)
                st.rerun()

        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("🗑️ Làm mới hội thoại"):
            st.session_state.messages = []
            st.rerun()

    # Chat chính
    st.markdown(f"### <span class='gradient-text'>Xin chào {st.session_state.user}!</span>", unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Nhập câu hỏi tại đây..."):
        add_message("user", prompt)
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_res = ""
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "Bạn là trợ lý AI công đoàn xã Hòa Khánh."},
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
