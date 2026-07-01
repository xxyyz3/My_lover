import streamlit as st

st.set_page_config(
    page_title="测试应用",
    page_icon="👾",
    layout="wide",
)

st.title("测试页面")
st.write("Hello World!")

with st.sidebar:
    st.write("侧边栏内容")
    character = st.selectbox("选择角色", ["樱岛麻衣", "椎名真白", "喜多川海梦", "雷姆"])

col1, col2 = st.columns([3, 1])
with col1:
    st.write(f"当前角色: {character}")
    prompt = st.chat_input("请输入...")
    if prompt:
        st.chat_message("user").write(f"用户: {prompt}")
        st.chat_message("assistant").write(f"{character}: 收到你的消息了！")
with col2:
    st.write("右侧信息栏")
