# --- XỬ LÝ HỎI ĐÁP AI TỰ ĐỘNG ---
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_res = ""
            
            # Điều chỉnh chỉ dẫn để AI thông minh hơn, không nhắc thừa
            system_instruction = (
                f"Bạn là trợ lý ảo chuyên nghiệp của Công đoàn xã Hòa Khánh. "
                f"Tác giả hệ thống: Lương Tấn Phát. Chủ tịch: Nguyễn Thanh Toàn. "
                f"Chỉ cung cấp chi tiết mẫu đơn khi người dùng hỏi về 'đăng ký', 'mẫu đơn' hoặc 'gia nhập'. "
                f"Các câu hỏi khác hãy trả lời ngắn gọn, thân thiện và đi thẳng vào vấn đề. "
                f"Người đang trò chuyện với bạn là Anh/Chị {st.session_state.user}."
            )

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_instruction},
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
        st.rerun()
