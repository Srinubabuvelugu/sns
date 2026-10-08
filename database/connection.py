import sqlite3


def DatabaseConnection():
    try:
        db_config = sqlite3.connect("sns_management.db")
        return db_config

    except Exception as e:
        return f"Something wrong in database/connection.py:{e}"
