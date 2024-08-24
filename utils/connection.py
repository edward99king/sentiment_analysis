import sqlite3 as sq
from utils import common_utils


def get_sql_connection():
    db = sq.connect(common_utils.get_current_directory() + '\im.db')

    return db