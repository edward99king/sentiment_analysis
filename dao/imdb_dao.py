from utils import connection
from model.Movies import Movies


def create_movie_table():
    try:
        query = '''CREATE TABLE MOVIES(
            id TEXT PRIMARY KEY,
            primary_title TEXT,
            original_title TEXT,
            is_adult INTEGER,
            start_year INTEGER,
            end_year INTEGER,
            runtime_minutes INTEGER,
            genres TEXT
        )
        '''

        cursor_db = connection.get_sql_connection().cursor()
        cursor_db.execute(query)
        cursor_db.close()

    except Exception as ex:
        print(ex)


def insert_movie_table(conn, id, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genres):
    try:
        query = '''INSERT INTO MOVIES (id, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genres) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
                '''.format(id, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genres)


        print(query)

        cursor_db = conn.cursor()
        cursor_db.execute(query)
        cursor_db.close()

    except Exception as ex:
        print(ex)

def get_all_movie_table(conn):
    try:
        query = f'''
                    SELECT id, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genres FROM MOVIES
                '''

        cursor_db = conn.cursor()
        cursor_db.execute(query)
        result = cursor_db.fetchall()
        result = [Movies(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]) for item in result]
        cursor_db.close()

        return result
    except Exception as e:
        print(e)

def get_all_movie_table_by_text(conn, text):
    try:
        query = f'''
                    SELECT id, primary_title, original_title, is_adult, start_year, end_year, runtime_minutes, genres FROM MOVIES
                    WHERE original_title LIKE '%{text}%'
                '''

        cursor_db = conn.cursor()
        cursor_db.execute(query)
        result = cursor_db.fetchall()
        result = [Movies(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]) for item in result]
        cursor_db.close()

        return result
    except Exception as e:
        print(e)