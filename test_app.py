import streamlit as st

st.set_page_config(
    page_title="测试应用",
    page_icon="👾",
    layout="wide",
)

st.title("测试页面")
st.write("Hello World!")
st.sidebar.write("侧边栏内容")
