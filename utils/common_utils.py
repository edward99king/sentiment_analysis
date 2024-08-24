from facade import imdb_facade

import pickle
import typing

import nltk
from nltk.util import ngrams

nltk.download('punkt')
nltk.download('punkt_tab')

import os


def get_current_directory():
    return os.path.dirname(os.path.realpath(__file__))

def save_pickle_file(path_filename, object):
    with open(path_filename, 'wb') as f:
        pickle.dump(object, f)

def import_pickle_file(path_filename):
    try:
        with open(path_filename, 'rb') as f:
            object = pickle.load(f)

        return object
    except Exception as ex:
        return None

def remove_links(text):
    import re
    return re.sub(r"http\S+", "", text)

def lower_text(text):
    return text.lower()

def clean_words(text_data, list_of_words_to_remove: typing.List):
    return [item for item in text_data if item not in list_of_words_to_remove]

def join_list_to_string(string_list):
    return ' '.join(string_list)

def remove_apostrophes(text):
    text = text.replace("\'", "")
    text = text.replace('\"', "")
    text = text.replace('`', "")
    return text

def remove_title_movie(text, title_movie):
    for item in text:
        if "movie" in item:
            text.remove(item)
        elif "film" in item:
            text.remove(item)

    return [item for item in text if item not in title_movie]

def generate_ngrams(text, n):
    try:

        words = nltk.word_tokenize(text)
        n_grams = ngrams(words, n)
        return [' '.join(grams) for grams in n_grams]
    except Exception as ex:
        print(ex)

def lemmatize_text(text):
    w_tokenizer = nltk.tokenize.WhitespaceTokenizer()
    lemmatizer = nltk.stem.WordNetLemmatizer()

    return [lemmatizer.lemmatize(w) for w in w_tokenizer.tokenize(text)]


def dict_person_to_string(dict_person, key_type):
    output_list = []

    if "writer" == key_type:
        for person in dict_person:
            if person._getitem("name") is not None:
                output_list.append(person._getitem("name"))
    elif "genres" == key_type:
        for genres in dict_person:
            output_list.append(genres)
    else:
        for person in dict_person:
            output_list.append(person["name"])

    return ", ".join(output_list)


def read_movies_title():
    df = pd.read_csv(r'.\title.basics.tsv\title.basics.tsv', sep='\t')
    df_movies = df[df['titleType'] == 'movie']

    return df_movies.values.tolist()

def extract_and_load_movies():
    movie_id_list = read_movies_title()

    for movie in movie_id_list:
        imdb_facade.insert_movie_table(
            id=movie[0].replace('tt', '').replace('\\N', '').replace('\'','`'),
            primary_title=str(movie[2]).replace('\\N', '').replace('\'','`'),
            original_title=str(movie[3]).replace('\\N', '').replace('\'','`'),
            is_adult=str(movie[4]).replace('\\N', '').replace('\'','`'),
            start_year=str(movie[5]).replace('\\N', '').replace('\'','`'),
            end_year=str(movie[6]).replace('\\N', '').replace('\'','`'),
            runtime_minutes=str(movie[7]).replace('\\N', '').replace('\'','`'),
            genres=str(movie[8]).replace('\\N', '').replace('\'','`')
        )

def transfer_movie_id_title_to_pickle():
    dict_movies = {}

    movies = import_pickle_file("dict_movies_full.pkl")

    if movies is None:
        movies = imdb_facade.get_all_movie_table()

        for movie in movies:
            dict_movies[movie.id] = movie.original_title

        save_pickle_file("dict_movies_full.pkl", dict_movies)





