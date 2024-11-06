import streamlit as st

# 세로줄이 지원되지 않는다. 마크다운으로 일일이 그어야 하는데, 그건 너무나 한계가 명확하다.

st.markdown(
    "<h1 style='text-align: center; font-size: 50px;'>Bookitoki</h1>",
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    div[data-testid="stButton"] > button {
        float: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("내정보"):
    st.switch_page("pages/myinfo_Bookitoki.py")

st.divider()

st.text_area(st.text('오늘의 책'),)

st.divider()

st.subheader('검색할 책을 입력하세요')
write,button = st.columns(2,vertical_alignment="bottom")

with write : st.text_input("책 이름을 입력해주세요")
with button : st.button("정보 입력",use_container_width=True)

st.divider()
st.header('추천도서')
import streamlit as st

# 4개의 열 생성 (두 번 반복)
columns1 = st.columns(4)
columns2 = st.columns(4)

# 책 정보 리스트
books = [
    {"image": "https://image.yes24.com/goods/77190977/XL", "name": "책이름1", "author": "저자명1", "genre":"장르1"},
    {"image": "https://image.yes24.com/goods/77190977/XL", "name": "책이름2", "author": "저자명2", "genre":"장르2"},
    {"image": "https://image.yes24.com/goods/77190977/XL", "name": "책이름3", "author": "저자명3", "genre":"장르3"},
    {"image": "https://image.yes24.com/goods/77190977/XL", "name": "책이름4", "author": "저자명4", "genre":"장르4"},
]

# 책 정보를 표시하는 함수
def display_books(columns, key_prefix):
    for i, (column, book) in enumerate(zip(columns, books)):
        with column:
            st.image(book["image"])
            st.write(f"책이름 : {book['name']}")
            st.write(f"저자명 : {book['author']}")
            st.write(f"장르 : {book['genre']}")
            st.feedback('stars', key=f'{key_prefix}_feedback_{i}')

# 첫 번째 행 출력
display_books(columns1, "row1")

# 두 번째 행 출력
display_books(columns2, "row2")

#버튼화
# html_content = """
# <div id="clickable-content" style="cursor: pointer; border: 1px solid #ddd; padding: 10px;">
#     <img src="https://image.yes24.com/goods/77190977/XL" style="width: 200px;">
#     <p>책이름</p>
#     <p>저자명</p>
#     <div>⭐⭐⭐⭐⭐</div>
# </div>
#
# <script>
# document.getElementById("clickable-content").addEventListener("click", function() {
#     alert("클릭되었습니다!");
# });
# </script>
# """
#
# st.markdown(html_content, unsafe_allow_html=True)

