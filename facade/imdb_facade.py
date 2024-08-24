from dao import imdb_dao
from utils import connection


def insert_movie_table(id, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genres):
    conn = connection.get_sql_connection()
    imdb_dao.insert_movie_table(conn, id, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genres)
    conn.commit()

def get_all_movie_table():
    conn = connection.get_sql_connection()
    return imdb_dao.get_all_movie_table(conn)

def get_all_movie_table_by_text(text):
    conn = connection.get_sql_connection()
    print(conn)
    return imdb_dao.get_all_movie_table_by_text(conn, text)
