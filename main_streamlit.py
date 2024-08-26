from utils import common_utils
from facade import imdb_facade

from imdb import Cinemagoer

import nltk
from nltk.corpus import stopwords

import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import spacy
import spacy.cli
from textblob import TextBlob

def package_preparation():
    nltk.download('stopwords')
    nltk.download('wordnet')
    spacy.cli.download("en_core_web_sm")

def get_sentiment_polarity(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment

    return sentiment.polarity

def get_sentiment_subjectivity(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment

    return sentiment.subjectivity

def count_ngrams(text, n):
    text = text.str.replace("'", "").replace("*", "").replace("-", "").replace(",", "").replace(".", "")
    ngrams = text.copy().str.split(' ').explode()

    for i in range(1, n):
        ngrams += ' ' + ngrams.groupby(level=0).shift(-i)

    ngrams = ngrams.dropna()

    return ngrams.value_counts().reset_index()

def data_cleansing(df):
    df['cleaned_text'] = df['review'].astype(str).apply(common_utils.remove_links)
    df['cleaned_text'] = df['cleaned_text'].astype(str).apply(common_utils.lower_text)
    df['cleaned_text'] = df['cleaned_text'].astype(str).apply(
        lambda x: common_utils.clean_words(x.split(), stopwords.words('english')))
    df['cleaned_text'] = df['cleaned_text'].apply(common_utils.join_list_to_string)
    df['cleaned_text'] = df['cleaned_text'].apply(common_utils.remove_apostrophes)
    df['cleaned_text'] = df['cleaned_text'].apply(
        lambda x: common_utils.remove_title_movie(x.split(), str(dict_movies[option]).split(" ")))

    df['clean_lemmatized'] = df['cleaned_text'].astype(str).apply(common_utils.lemmatize_text)
    df['clean_lemmatized'] = df['clean_lemmatized'].apply(common_utils.join_list_to_string)

def rating_font_color(rating):
    if rating < 6:
        return '<h1 style="color: red;">'
    elif rating < 8:
        return '<h1 style="color: orange;">'
    elif rating < 9:
        return '<h1 style="color: green;">'
    elif rating < 10:
        return '<h1 style="color: blue;">'

def get_dict_sum_group_rating(rating_list):
    dict_rating = {
        "Rating" : [0,1,2,3,4,5,6,7,8,9,10],
        "Point":   [0,0,0,0,0,0,0,0,0,0,0]
    }

    for rating in rating_list:
        if rating is None:
            rating = 0

        inst_rating_list = dict_rating["Rating"]
        inst_point_list = dict_rating["Point"]
        inst_point_list[inst_rating_list.index(rating)] = inst_point_list[inst_rating_list.index(rating)] + 1
        dict_rating["Point"] = inst_point_list

    return dict_rating


if __name__ == '__main__':
    package_preparation()
    ia = Cinemagoer()
    nlp = spacy.load("en_core_web_sm")

    st.title("IMDB - Sentiment Analysis")

    text_input = st.text_input("Enter more than 3 characters for filtering Movie Title:", key="text_input")

    dict_movies = {}

    if "clicked" not in st.session_state:
        st.session_state.clicked = False

    if st.button("Filter") or st.session_state["clicked"]:
        st.session_state["clicked"] = True

        movies = imdb_facade.get_all_movie_table_by_text(text_input)

        for movie in movies:
            dict_movies[movie.id] = f"{movie.original_title} ({str(movie.start_year)})"

        option = st.selectbox("Movie Title", options=list(dict_movies.keys()), format_func=lambda x: dict_movies[x])

        if "clicked" not in st.session_state:
            st.session_state.clicked = False

        if st.button('Process') or st.session_state["clicked"]:
            movie_data = ia.get_movie(str(option))

            col1, col2 = st.columns(2)

            with col1:
                if 'cover url' in movie_data:
                    st.header('')
                    cover_url = movie_data['full-size cover url']
                    st.image(cover_url, width=310)
                else:
                    st.write("no movie picture")

            with col2:
                st.header(dict_movies[option])
                st.markdown('<div style="text-align: justify;">' + movie_data['plot outline'] + ' </div>', unsafe_allow_html=True)

            st.markdown('<br>', unsafe_allow_html=True)


            st.markdown('<h4>Writer:</h4> <div style="text-align: justify;">' +
                        common_utils.dict_person_to_string(movie_data["writer"], "writer") + ' </div>',
                        unsafe_allow_html=True)
            st.markdown('<h4>Director:</h4> <div style="text-align: justify;">' +
                        common_utils.dict_person_to_string(movie_data["director"], "director") + ' </div>',
                        unsafe_allow_html=True)
            st.markdown('<h4>Cast:</h4> <div style="text-align: justify;">' + common_utils.dict_person_to_string(movie_data["cast"], "cast") + ' </div>',
                        unsafe_allow_html=True)
            st.markdown('<h4>Genres:</h4> <div style="text-align: justify;">' + common_utils.dict_person_to_string(movie_data["genres"], "genres") + ' </div>',
                        unsafe_allow_html=True)


            reviews = ia.get_movie_reviews(str(option))

            if reviews is not None :
                review_list = []
                rating_list = []

                try:
                    for index in range(0, len(reviews['data']['reviews'])):
                        review_list.append(reviews['data']['reviews'][index]['content'])
                        rating_list.append(reviews['data']['reviews'][index]['rating'])

                    df = pd.DataFrame(review_list, columns=['review'])

                    rating_df = pd.DataFrame(get_dict_sum_group_rating(rating_list))

                    st.markdown('<h4>Rating:</h4>' + rating_font_color(movie_data["rating"]) + str(
                        movie_data["rating"]) + '</h1>',
                                unsafe_allow_html=True)

                    fig, ax = plt.subplots()
                    ax.barh(rating_df['Rating'], rating_df['Point'], color=['lightsalmon'])
                    ax.set_ylabel('Rating')
                    st.pyplot(fig)

                    st.markdown('<center><h1>User Sentiment</h1></center>', unsafe_allow_html=True)

                    data_cleansing(df)

                    wordcloud = WordCloud().generate(' '.join(df['clean_lemmatized'].astype(str)))

                    fig, ax = plt.subplots()

                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis("off")
                    st.pyplot(fig)

                    df['Polarity'] = df['clean_lemmatized'].astype(str).apply(lambda x: get_sentiment_polarity(x))
                    df['Subjectivity'] = df['clean_lemmatized'].astype(str).apply(lambda x: get_sentiment_subjectivity(x))
                    df['NGrams'] = df['clean_lemmatized'].astype(str).apply(lambda x: common_utils.generate_ngrams(x, 1))

                    sentiment_polarity = "Positive" if df['Polarity'].mean() > 0 else "Negative"
                    sentiment_subjetivity = "Subjective" if df['Subjectivity'].mean() > 0 else "Objective"
                    st.markdown('<center><h3>' + sentiment_polarity + ' & ' + sentiment_subjetivity + '</h3></center>', unsafe_allow_html=True)

                    st.markdown('<br>', unsafe_allow_html=True)

                    count_ngram = count_ngrams(df['clean_lemmatized'], 1)

                    ngram_df = pd.DataFrame(count_ngram)
                    ngram_list = ngram_df['clean_lemmatized'].tolist()
                    count_list = ngram_df['count'].tolist()

                    checkbox_state = {}
                    counter = 0
                    num_of_cols = 4
                    cols_checkbox = st.columns(num_of_cols)

                    value_mapping = {}

                    for index, item in enumerate(ngram_list):
                        if len(ngram_list[index].replace(',','').replace('-','').replace(' ','')) > 0:
                            checkbox_state[counter] = cols_checkbox[counter%num_of_cols].checkbox(
                                ngram_list[index].replace(',','').replace('-','').replace(' ','') + ' (' +str(count_list[index]) + ')',
                                value=False,
                                key=ngram_list[index].replace(',','').replace('-','').replace(' ',''),
                                disabled=False,
                                label_visibility='visible'
                            )

                            value_mapping[counter] = ngram_list[index].replace(',','')

                            if counter == 9:
                                break
                            else:
                                counter = counter + 1

                    selected_items = [item for item, checked in checkbox_state.items() if checked]
                    filter = []

                    for item in selected_items:
                        filter.append(value_mapping[item])

                    mask = df['review'].apply(lambda x: any(item in x for item in filter))
                    filtered_df = df[mask]

                    st.dataframe(filtered_df['review'], use_container_width=True, hide_index=True)

                except Exception as ex:
                    print(ex)
                    review_list = []
                    st.write('There is no review')







