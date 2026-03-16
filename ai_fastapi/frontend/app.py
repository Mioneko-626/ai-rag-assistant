import streamlit as st
import requests

st.title("我的 AI 知识库助手")

# 1. 聊天记录保持
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. 显示聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. 输入框
# app.py 关键片段
if prompt := st.chat_input("问我..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        # 发送请求，注意这里的 stream=True
        response = requests.post("http://127.0.0.1:8000/api/chat-stream/",
                                 json={"prompt": prompt}, stream=True)

        # 实时写入界面
        message_placeholder = st.empty()
        full_response = ""
        for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
            if chunk:
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})