import streamlit as st

st.markdown("""
<style>
    .clickable-title {
        cursor: pointer;
        color: #ffffff;
        text-align: center;
        display: block;
        font-size: 3em;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .clickable-title:hover {
        color: #22a0af;
        text-decoration: underline;
    }
</style>

<script>
    function navigateToMain() {
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: true}, '*');
    }
</script>

<h1 class="clickable-title" onclick="navigateToMain()">Bookitoki</h1>
""", unsafe_allow_html=True)

if st.session_state.get('navigate_to_main', False):
    st.switch_page("app_Bookitoki.py")  # 메인 페이지 파일명을 여기에 입력하세요

# 'my info' 페이지의 나머지 내용을 여기에 추가하세요