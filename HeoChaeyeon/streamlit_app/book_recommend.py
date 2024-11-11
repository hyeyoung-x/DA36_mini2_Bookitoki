import module
import streamlit as st
import warnings
import pandas as pd
warnings.filterwarnings("ignore", category=FutureWarning)


def display_books(columns, lst):
    for i, (column, book) in enumerate(zip(columns, lst)):
        with column:
            if len(book["image"]) > 0:
                st.image(book["image"])
            else:
                st.image("https://xen-api.linkareer.com/attachments/55662")

            # CSS 스타일 적용 (줄 간격 조정 및 각 항목 스타일 지정)
            st.markdown("""
                <style>
                    .book-title {
                        font-size: 15px;
                        font-weight: bold;
                        margin-bottom: 2px;  /* 줄 간격 줄이기 */
                    }

                    .book-author {
                        font-size: 11px;
                        color: #333333;  /* 어두운 회색 */
                        margin-bottom: 2px;  /* 줄 간격 줄이기 */
                    }

                    .book-category {
                        font-size: 11px;
                        color: #666666;  /* 회색 */
                        margin-bottom: 30px;  /* 마지막 항목이라 줄 간격 없이 */
                    }
                </style>
                """, unsafe_allow_html=True)

            # 스타일 적용하여 출력
            st.markdown(f'<p class="book-title">{book["title"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="book-author">{book["author"]}</p>', unsafe_allow_html=True)
            st.markdown(f'<p class="book-category">{book["category"]}</p>', unsafe_allow_html=True)




#-----------------------------------------------#

st.set_page_config(
    page_title="Bookitoki",
    page_icon="📚",
)

if "page" not in st.session_state:
    st.session_state.page = "book_recommend"
    st.session_state['input_id']=""

def go_to_recommend_page():
    st.session_state.page = "recommend_page"

#---------------------------------------------------------------------------------------------------#
# main pages
if st.session_state.page == "book_recommend":

#---------------------#
    col1, col2, col3= st.columns([1,3,1])

    with col2:
        st.image("pic/logo.png")

#----------#
    col3, col1, col2= st.columns([0.4,4,1])
    with col1:
        st.markdown(
        """
        <style>            
        div[data-testid="stTextInput"] input {
            padding-top: 0px;
            background-color: transparent !important;
            color: #333333; /* 텍스트 색상 */
            padding: 3px;
            font-size: 16px; /* 글꼴 크기 */
            border-color : #black;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        input_id = st.text_input(label="", placeholder="사용자 id를 입력하세요 ! ex) 72196", value=" ", label_visibility="hidden")
        if input_id :
            st.session_state['input_id'] = input_id

    with col2:
        st.markdown(
            """
            <style>            
            div[data-testid="stButton"] > button {
                margin-top: 28px;
                background-color: #white; /* 입력 필드 배경색 */
                color: #333333; /* 텍스트 색상 */
                font-size: 16px; /* 글꼴 크기 */
                border-color: #black; /* 입력 필드 내부 경계선 제거 */
                text-align: center;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        confirm_button = st.button("확인")

    # 확인 버튼 클릭 시 동작
    if confirm_button:
        go_to_recommend_page()
#-----------------------------------------------------#

elif st.session_state.page == "recommend_page":

    if 'input_id' in st.session_state:
        input_id = st.session_state['input_id']

    st.markdown( """
            <style>            
            div[data-testid="stButton"] > button {
                font-size: 100px; /* 글꼴 크기 */
                font-color: #green;
            }
            </style>
            """, unsafe_allow_html=True)

    back_button = st.button("👈🏻")

    if back_button:
        st.session_state.page = "book_recommend"

    st.image("pic/book_img.png", )

    st.markdown(
        """
        <style> 
        /* 탭 배경색 및 텍스트 색상 변경 */
        div[data-testid="stTabs"] button {
            background-color: ##d8e7e5; 
            color: #323232; 
            font-size: 18px; /* 글자 크기 */
            padding: 10px;
            font-weight: bold;
        }
        
        div[data-testid="stTabs"] button:hover {
            color: black;  /* 텍스트 색상 */
            background-color: #white;  /* 배경 색상 (초록색 예시) */
            cursor: pointer;
        }

        /* 선택된 탭 스타일 변경 */
        div[data-testid="stTabs"] button[aria-selected="true"] {
            background-color: #5a847f; /* 진한 파란색 배경 */
            color: #ffffff; /* 흰색 글자 */
        }

        /* 탭 버튼 간 간격 조정 */
        div[data-testid="stTabs"] button + button {
             margin: 0;
             padding: 10px; 
        }
        
        div[data-testid="stTabs"] {
            gap: 0px; 
        </style>
        """,
        unsafe_allow_html=True
    )

# second page tab ------------------------------------------------------------------------#
    rating,author,cate,age = st.tabs(["rating", "author","cate","age"])
    input_id = int(input_id)
    # 1) by_rating tab ------------------------------------------------------------------------#
    with rating:

        rating_df=module.recommend_by_book_sim(input_id)


        columns1 = st.columns(5)
        columns2 = st.columns(5)
        rating_books=[]

        for i in range(10):
            rating_books.append({"image": rating_df.iloc[i,3], "title": rating_df.iloc[i,0], "author": rating_df.iloc[i,4],
                              "category": rating_df.iloc[i,2]})



        display_books(columns1, rating_books[:5])
        display_books(columns2, rating_books[5:])


    # 2) by_author tab ------------------------------------------------------------------------#
    with author:

        st.write("This is Tab 2")

        author_df=module.recommend_by_author_sim(input_id)

        columns1 = st.columns(5)
        author_books=[]

        for i in range(len(author_df)):
            author_books.append({"image": author_df.iloc[i,4], "title": author_df.iloc[i,1], "author": author_df.iloc[i,0],
                              "category": author_df.iloc[i,3]})



        display_books(columns1, author_books)

    # 3) by_cate tab ------------------------------------------------------------------------#

    with cate:
        st.write("this")

        cate_df=module.recommend_by_category_df(input_id)
        columns1 = st.columns(5)
        columns2 = st.columns(5)
        cate_books=[]
        for i in range(10):
            cate_books.append({"image": cate_df.iloc[i,3], "title": cate_df.iloc[i,1], "author": cate_df.iloc[i,4],
                              "category": cate_df.iloc[i,2]})


        display_books(columns1, cate_books[:5])
        display_books(columns2, cate_books[5:])

    # 4) by_ages tab ------------------------------------------------------------------------#

    with age:


        sim, dif = module.recommend_by_ages_df(input_id)

        columns1 = st.columns(5)
        columns2 = st.columns(5)
        sim_books = []
        dif_books = []

        for i, info in enumerate(sim):
            sim_books.append({"image": sim.iloc[i][3], "title": sim.iloc[i][0], "author": sim.iloc[i][4],
                              "category": sim.iloc[i][2]})
        for i, info in enumerate(dif):
            dif_books.append({"image": dif.iloc[i][3], "title": dif.iloc[i][0], "author": dif.iloc[i][4],
                              "category": dif.iloc[i][2]})

        display_books(columns1, sim_books)
        display_books(columns2, dif_books)
