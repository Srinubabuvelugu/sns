from database.connection import DatabaseConnection


def CreateTables():
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        user_table_query = """
        CREATE TABLE IF NOT EXISTS USERS(
            USERID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERNAME TEXT NOT NULL,
            EMAIL TEXT NOT NULL UNIQUE,
            HASHPASSWORD TEXT NOT NULL,
            IS_ACTIVE INTEGER DEFAULT 0,
            CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        notes_table_query = """
        CREATE TABLE IF NOT EXISTS NOTES(
            NOTESID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERID INTEGER,
            TITLE TEXT NOT NULL,
            CONTENT TEXT NOT NULL,
            CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(USERID) REFERENCES USERS(USERID) ON DELETE CASCADE
        );
        """

        files_table_query = """
        CREATE TABLE IF NOT EXISTS FILES(
            FILEID INTEGER PRIMARY KEY AUTOINCREMENT,
            USERID INTEGER,
            ORIGINALNAME TEXT,
            STOREDNAME TEXT,
            MIMETYPE TEXT,
            SIZE INTEGER,
            FILEPATH TEXT,
            CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(USERID) REFERENCES USERS(USERID) ON DELETE CASCADE
        );
        """

        cursor.execute(user_table_query)
        cursor.execute(notes_table_query)
        cursor.execute(files_table_query)

        db_config.commit()

        cursor.close()
        db_config.close()

        return "Tables Created"

    except Exception as e:
        return f"Something wrong in database/tablesDB:{e}"
