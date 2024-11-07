import streamlit as st



st.subheader("겨울을 따뜻하게 그리고 :red[포근하게] ❤️")
st.subheader("This is a subheader with a divider", divider="gray")
st.subheader("These subheaders have rotating dividers", divider=True)
st.subheader("One", divider=True)
st.subheader("Two", divider=True)
st.subheader("Three", divider=True)
st.subheader("Four", divider=True)

col1, col2, col3 = st.columns(3)
col1.metric("오늘의 신간", "67권", "어제 보다 30권 더")
col2.metric("같이 독서하는 친구", "203,471", "-8%")
col3.metric("내 평균 완독률", "46%", "-4%")



stars = st.select_slider(
    "별점을 선택하세요",
    options=range(1, 11),
    format_func=lambda x: "⭐" * x
)

if stars:
    st.markdown(f"{stars}개의 별을 선택하셨습니다.")


options = st.multiselect(
    "어떤 분위기가 좋으세요?",
    ["아늑한", "오싹한", "할로윈", "흥미로운"],
    ["오싹한", "할로윈"],
)

st.write("You selected:", options)

import time

#@st.fragment
def release_the_balloons():
    st.button("Release the balloons", help="Fragment rerun")
    st.balloons()

with st.spinner("Inflating balloons..."):
    time.sleep(5)
release_the_balloons()
st.button("Inflate more balloons", help="Full rerun")

if "app_runs" not in st.session_state:
    st.session_state.app_runs = 0
    st.session_state.fragment_runs = 0

