import streamlit as st
from groq import Groq
from streamlit_mic_recorder import mic_recorder
import os

# --- CẤU HÌNH HỆ THỐNG ---
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("Thiếu API Key!")
    st.stop()

# --- CSS ĐỂ NÚT MIC ĐẸP HƠN ---
st.markdown('''
<style>
    /* Làm cho khu vực điều khiển mic trông chuyên nghiệp */
    .mic-container {
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f0f4f8;
        padding: 10px;
        border-radius: 15px;
        border: 1px solid #003366;
        margin-bottom: 10px;
    }
    /* Hiệu ứng sóng âm giả lập khi đang ghi âm (Tùy chọn) */
</style>
''', unsafe_allow_html=True)

# --- HÀM XỬ LÝ CHUYỂN ĐỔI ÂM THANH (STT) ---
def transcribe_audio(audio_bytes):
    if audio_bytes:
        try:
            # Lưu tạm file âm thanh để gửi lên API
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_bytes)
            
            # Sử dụng Model Whisper-large-v3 của Groq (Siêu nhanh và chính xác tiếng Việt)
            with open("temp_audio.wav", "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=("temp_audio.wav", file.read()),
                    model="whisper-large-v3",
                    language="vi", # Ép nhận diện tiếng Việt
                    response_format="text"
                )
            
            # Xóa file tạm sau khi xong
            os.remove("temp_audio.wav")
            return transcription
        except Exception as e:
            st.error(f"Lỗi xử lý âm thanh: {e}")
            return None
    return None

# --- GIAO DIỆN CHAT CHÍNH ---
if st.session_state.get("logged"):
    st.markdown("### 🤖 Trợ lý AI Hòa Khánh")

    # 1. KHU VỰC THU ÂM (Voice Input Area)
    st.markdown('<p style="font-size:0.9rem; font-weight:bold;">🎤 Nhấn để nói (Hệ thống tự nhận diện tiếng Việt):</p>', unsafe_allow_html=True)
    
    # Widget mic_recorder
    audio = mic_recorder(
        start_prompt="Bắt đầu ghi âm",
        stop_prompt="Dừng & Gửi",
        key='recorder',
        just_once=True,
    )

    # Xử lý khi có dữ liệu âm thanh sau khi bấm "Dừng"
    voice_text = ""
    if audio:
        with st.spinner("Robot đang lắng nghe và chuyển ngữ..."):
            voice_text = transcribe_audio(audio['bytes'])
            if voice_text:
                st.success(f"Đã nhận diện: {voice_text}")
                # Gán voice_text vào prompt để xử lý như tin nhắn văn bản
                prompt = voice_text 
            else:
                prompt = None
    else:
        # Nếu không dùng giọng nói thì lấy từ chat_input mặc định
        prompt = st.chat_input("Hỏi tôi về thủ tục hành chính...")

    # 2. LOGIC XỬ LÝ CHAT (Giữ nguyên phần xử lý tin nhắn của bạn)
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Hiển thị hiệu ứng gõ chữ và gọi API Chat
            # (Phần này Phát dùng lại code cũ của mình nhé)
            pass
