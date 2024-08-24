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

    df[f'Polarity'] = df['review'].astype(str).apply(lambda x: get_sentiment_polarity(x))
    df[f'Subjectivity'] = df['review'].astype(str).apply(lambda x: get_sentiment_subjectivity(x))


if __name__ == '__main__':
    package_preparation()
    ia = Cinemagoer()
    nlp = spacy.load("en_core_web_sm")

    st.title("IMDB - Sentiment Analysis")

    text_input = st.text_input("Enter more than 3 characters:", key="text_input")

    dict_movies = {}

    if "clicked" not in st.session_state:
        st.session_state.clicked = False

    if st.button("Search") or st.session_state["clicked"]:
        st.session_state["clicked"] = True

        movies = imdb_facade.get_all_movie_table_by_text(text_input)

        for movie in movies:
            dict_movies[movie.id] = f"{movie.original_title} ({str(movie.start_year)})"

        option = st.selectbox("Movie Title", options=list(dict_movies.keys()), format_func=lambda x: dict_movies[x])

        if st.button('Process'):
            movie_data = ia.get_movie(str(option))

            col1, col2 = st.columns(2)

            with col1:
                if 'cover url' in movie_data:
                    cover_url = movie_data['full-size cover url']
                    st.image(cover_url, width=300)
                else:
                    st.write("no movie picture")

            with col2:
                st.header(dict_movies[option])
                st.markdown('<div style="text-align: justify;">' + movie_data['plot outline'] + ' </div>', unsafe_allow_html=True)

            st.write("Rating: ", str(movie_data["rating"]))
            st.write("Writer: ",  common_utils.dict_person_to_string(movie_data["writer"], "writer"))
            st.write("Director: ", common_utils.dict_person_to_string(movie_data["director"], "cast"))
            st.markdown('<b>Cast</b>: <div style="text-align: justify;">' + common_utils.dict_person_to_string(movie_data["cast"], "cast") + ' </div>',
                        unsafe_allow_html=True)
            st.write("Genres: ", common_utils.dict_person_to_string(movie_data["genres"], "genres"))

            reviews = ia.get_movie_reviews(str(option))

            if reviews is not None :
                review_list = []

                try:
                    for index in range(0, len(reviews['data']['reviews'])):
                        review_list.append(reviews['data']['reviews'][index]['content'])

                    df = pd.DataFrame(review_list, columns=['review'])

                    data_cleansing(df)

                    wordcloud = WordCloud().generate(' '.join(df['clean_lemmatized'].astype(str)))

                    fig, ax = plt.subplots()

                    plt.imshow(wordcloud, interpolation='bilinear')
                    plt.axis("off")
                    st.pyplot(fig)

                    st.subheader("User Comment Sentiment: ")
                    st.header("Positive" if df['Polarity'].mean() > 0 else "Negative")

                    st.subheader("Comment Clasification: ")
                    st.header("Subjective" if df['Subjectivity'].mean() > 0 else "Objective")

                    #TODO: Tambahkan n-gram -> ketahui sebagian komen itu mengenai apa.

                except Exception as ex:
                    review_list = []
                    st.write('There is no review')







