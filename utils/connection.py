import sqlite3 as sq


def get_sql_connection():
    db = sq.connect('C:\Workspace Python\SanberCode - Tugas Akhir\im.db')

    return db