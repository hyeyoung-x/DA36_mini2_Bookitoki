import pandas as pd
# preprocessed-data -------------------------------------------------#
book_filter_df=pd.read_csv('csv/book_filter_df.csv')
user_book_df=book_filter_df.pivot_table(index='user_id',columns='book_title',values='rating',fill_value=0)
user_author_rating_df = book_filter_df.groupby(['user_id', 'book_author'])['rating'].mean().reset_index()
user_author_rating_df=user_author_rating_df.pivot_table(index="user_id",columns="book_author",values="rating",fill_value=0)
#--------------------------------------------------------------------------------------------------------#
# 연령대별 유사도
ages_similarity_df=pd.read_csv("csv/age_similarity_df.csv",index_col='book_title')
#--------------------------------------------------------------------------------------------------------#
# # user의 top category 추천
top_book_by_category=pd.read_csv("csv/top_book_by_category.csv",index_col=0)
#--------------------------------------------------------------------------------------------------------#
# # 책 평점별 유사도
book_similarity_df=pd.read_csv("csv/book_similarity_df.csv",index_col='book_title')
book_ratings_pred_df=pd.read_csv("csv/book_ratings_pred_df.csv",index_col='user_id')
#--------------------------------------------------------------------------------------------------------#
# # 작가 평점별 유사도
author_similarity_df=pd.read_csv("csv/author_similarity_df.csv",index_col='book_author')
author_ratings_pred_df=pd.read_csv("csv/author_ratings_pred_df.csv",index_col='user_id')
#--------------------------------------------------------------------------------------------------------#
# streamlit 시각화 자료
def match_L_Category(title):
    title_L_Category=book_filter_df[["book_title","L_Category"]].drop_duplicates()
    L_Category=title_L_Category[title_L_Category['book_title']==title]["L_Category"].iloc[0]
    return L_Category

def match_image_link(title):
    title_image=book_filter_df[["book_title","img_m"]].drop_duplicates()
    image=title_image[title_image['book_title']==title]["img_m"].iloc[0]
    return image

def match_author(title):
    title_author=book_filter_df[["book_title","book_author"]].drop_duplicates()
    author=title_author[title_author['book_title']==title]["book_author"].iloc[0]
    return author
#---------------------------------------------------------------------#
# 연령대 별 추천을 위한 method
def get_unseen_books(user_idx):
    user_read_df=user_book_df.loc[user_idx,:]
    return user_read_df[user_read_df==0].index

def user_fav_book(user_idx):
    user_ages=pd.DataFrame(book_filter_df[book_filter_df['user_id']==user_idx])
    user_ages.sort_values(by='rating',ascending=False,inplace=True)
    l_category=user_ages[:20]["L_Category"].value_counts().idxmax()
    i=0
    while True:
        if user_ages.iloc[i]["L_Category"]==l_category:
            favorite_book=user_ages.iloc[i]['book_title']
            break
    return l_category, favorite_book

def predict_books(user_idx):
    unseen_idx=get_unseen_books(user_idx)
    l_cate,fav_idx=user_fav_book(user_idx)
    temp=ages_similarity_df.loc[fav_idx][unseen_idx].sort_values(ascending=False)
    temp=pd.DataFrame(temp).reset_index()
    temp["L_Category"] = temp["book_title"][:300].apply(match_L_Category)
    predict_same_L_category=temp[temp["L_Category"]==l_cate][:5]
    predict_dif_L_category=temp[temp["L_Category"]!=l_cate][:5]
    return predict_same_L_category,predict_dif_L_category
#---------------------------------------------------------------------#
def recommend_by_ages_df(user_idx):
    same,dif=predict_books(user_idx)
    same["image_link"]=same["book_title"].apply(match_image_link)
    dif["image_link"]=dif["book_title"].apply(match_image_link)
    same["book_author"]=same["book_title"].apply(match_author)
    dif["book_author"]=dif["book_title"].apply(match_author)
    return same,dif
#---------------------------------------------------------------------#
# category별 추천
def get_top_category_book(user_idx):
    # 해당 user_id의 가장 많이 선택한 L_Category 찾기
    max_category = book_filter_df[book_filter_df['user_id'] == user_idx]['L_Category'].value_counts().idxmax()
    # top_book_by_category에서 해당 카테고리의 책 제목 반환
    result = top_book_by_category[max_category]
    result = pd.DataFrame(result).reset_index()
    result["L_Category"]=max_category
    return result,max_category

def recommend_by_category_df(user_idx):
    cate_df,max_category=get_top_category_book(user_idx)
    cate_df["image_link"] = cate_df[max_category].apply(match_image_link)
    cate_df["book_author"] = cate_df[max_category].apply(match_author)

    return cate_df
#---------------------------------------------------------------------#
# 책 평점 유사도별 추천
def get_top_books_rating(user_idx):
    unseen_idx=get_unseen_books(user_idx)
    temp=book_ratings_pred_df.loc[user_idx][unseen_idx].sort_values(ascending=False)[:10]
    result=pd.DataFrame(temp).reset_index()
    return result

def recommend_by_book_sim(user_idx):
    book_sim_df=get_top_books_rating(user_idx)

    book_sim_df["L_Category"] = book_sim_df["book_title"].apply(match_L_Category)
    book_sim_df["image_link"] = book_sim_df["book_title"].apply(match_image_link)
    book_sim_df["book_author"] = book_sim_df["book_title"].apply(match_author)

    return book_sim_df
#---------------------------------------------------------------------#
# 작가 유사도별 추천
def get_unread_author(user_idx):
    user_unread_author = user_author_rating_df.iloc[user_idx]
    return user_unread_author[user_unread_author==0].index

def favorite_authors_books(user_idx):
    user_ratings = user_author_rating_df.iloc[user_idx].sort_values(ascending=False)
    fav_author = user_ratings.index[0]
    return fav_author

def get_recommend_author(user_idx):
    fav_author=favorite_authors_books(user_idx)
    temp=author_similarity_df.loc[fav_author].sort_values(ascending=False)
    recommend_author=temp.index[1]
    return recommend_author

def recommend_by_author_sim(user_idx):
    recommend_author=get_recommend_author(user_idx)
    user_author_rating_df = book_filter_df.groupby(['book_author','book_title'])['rating'].mean().reset_index()
    author_sim_df=user_author_rating_df[user_author_rating_df["book_author"]==recommend_author].sort_values(by="rating",ascending=False)
    author_sim_df["L_Category"] = author_sim_df["book_title"].apply(match_L_Category)
    author_sim_df["image_link"] = author_sim_df["book_title"].apply(match_image_link)

    return author_sim_df