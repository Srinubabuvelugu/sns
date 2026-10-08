from database.connection import DatabaseConnection


# check user already exist or not
def getUserByEmail(email: str, data=False):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        get_user_by_email = """
        SELECT * FROM USERS
        WHERE EMAIL = ?;
        """

        cursor.execute(get_user_by_email, (email,))
        user = cursor.fetchone()

        if user:
            columns = [column[0] for column in cursor.description]
            user = dict(zip(columns, user))

        cursor.close()
        db_config.close()

        if data == True:
            if user:
                return True, user
            else:
                return False, "Check your user credentials"

        if not user:
            return True
        else:
            return False

    except Exception as e:
        return f"Something wrong in database/utilityDB.py:getUserByEmail: {e}"


# insert user data into table
def insertUserRecord(name: str, email: str, hash_pasword: bytes):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        insert_record_query = """
        INSERT INTO USERS(USERNAME, EMAIL, HASHPASSWORD, IS_ACTIVE)
        VALUES(?, ?, ?, ?);
        """

        cursor.execute(
            insert_record_query,
            (name, email, hash_pasword, 1)
        )

        db_config.commit()

        cursor.close()
        db_config.close()

        return True, "User Successfully Registred"

    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:getUserByEmail: {e}"


# insert notes into table
def insertNotesRecord(userid: int, title: str, content: str):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        insert_record_query = """
        INSERT INTO NOTES(USERID, TITLE, CONTENT)
        VALUES(?, ?, ?);
        """

        cursor.execute(
            insert_record_query,
            (userid, title, content)
        )

        db_config.commit()

        cursor.close()
        db_config.close()

        return True, "Notes Added"

    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:insertNotesRecord: {e}"


# get Notes by userid
def getNotesByUserid(userid: int, title: str = None, limit: int = None):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        get_notes_query = """
        SELECT * FROM NOTES
        WHERE USERID = ?
        """

        values = [userid]

        if title:
            get_notes_query += " AND TITLE LIKE ?"
            values.append(f"%{title}%")

        get_notes_query += " ORDER BY UPDATED_AT DESC"

        if limit:
            get_notes_query += " LIMIT ?"
            values.append(limit)

        cursor.execute(get_notes_query, tuple(values))

        notes = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        notes = [
            dict(zip(columns, note))
            for note in notes
        ]

        cursor.close()
        db_config.close()

        return True, notes

    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:getNotesByUserid: {e}"


# get notes by notes id
def getNotesByNotesid(notesid: int, userid: int):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        get_notes_query = """
        SELECT * FROM NOTES
        WHERE NOTESID = ? AND USERID = ?;
        """

        cursor.execute(
            get_notes_query,
            (notesid, userid)
        )

        notes = cursor.fetchone()

        if notes:
            columns = [column[0] for column in cursor.description]
            notes = dict(zip(columns, notes))

        cursor.close()
        db_config.close()

        if notes:
            return True, notes
        else:
            return False, "Notes id not found"

    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:getNotesByNotesid: {e}"


# update notes by notes id
def updateNotesByNotesid(
    notesid: int,
    userid: int,
    title: str,
    content: str
):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        update_notes_query = """
        UPDATE NOTES
        SET TITLE = ?,
            CONTENT = ?,
            UPDATED_AT = CURRENT_TIMESTAMP
        WHERE NOTESID = ? AND USERID = ?;
        """

        cursor.execute(
            update_notes_query,
            (title, content, notesid, userid)
        )

        db_config.commit()

        cursor.close()
        db_config.close()

        return True, "Notes Updated"

    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:getNotesByNotesid: {e}"


# delete notes by notes id
def deleteNotesByNotesid(notesid: int, userid: int):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        delete_notes_query = """
        DELETE FROM NOTES
        WHERE NOTESID = ? AND USERID = ?;
        """

        cursor.execute(
            delete_notes_query,
            (notesid, userid)
        )

        db_config.commit()

        cursor.close()
        db_config.close()

        return True, "Notes Deleted"

    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:deleteNotesByNotesid: {e}"


# check file duplicate exists or not
def checkFileDuplicate(filename: str, userid: int):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        get_file_query = """
        SELECT * FROM FILES
        WHERE STOREDNAME = ? AND USERID = ?;
        """

        cursor.execute(
            get_file_query,
            (filename, userid)
        )

        file = cursor.fetchone()

        cursor.close()
        db_config.close()

        if file:
            return False, "File already exists"
        else:
            return True, "File Not Exists"

    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:checkFileDuplicate: {e}"


# insert file metadata record
def insertFileMetaDataRecord(filemetadata: tuple):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        insert_record_query = """
        INSERT INTO FILES
        (
            USERID,
            ORIGINALNAME,
            STOREDNAME,
            MIMETYPE,
            SIZE,
            FILEPATH
        )
        VALUES(?, ?, ?, ?, ?, ?);
        """

        cursor.execute(
            insert_record_query,
            filemetadata
        )

        db_config.commit()

        cursor.close()
        db_config.close()

        return True, "File saved"

    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:insertFileMetaDataRecord(): {e}"


# get files by userid
def getFilesByUserid(userid: int):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        get_files_query = """
        SELECT * FROM FILES
        WHERE USERID = ?
        ORDER BY CREATED_AT DESC;
        """

        cursor.execute(
            get_files_query,
            (userid,)
        )

        files = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        files = [
            dict(zip(columns, file))
            for file in files
        ]

        cursor.close()
        db_config.close()

        return True, files

    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:getFilesByUserid(): {e}"


# get total files and notes count
def getFileAndNotesCount(userid: int):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        get_files_count = """
        SELECT COUNT(*)
        FROM FILES
        WHERE USERID = ?;
        """

        cursor.execute(
            get_files_count,
            (userid,)
        )

        files_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM NOTES WHERE USERID = ?;",
            (userid,)
        )

        notes_count = cursor.fetchone()[0]

        cursor.close()
        db_config.close()

        return notes_count, files_count

    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:getFilesAndNotesCount(): {e}"


# update Password by using email
def updatePasswordByEmail(email: str, hash_password: str):
    try:
        db_config = DatabaseConnection()
        cursor = db_config.cursor()

        query = """
        UPDATE USERS
        SET HASHPASSWORD = ?
        WHERE EMAIL = ?
        """

        cursor.execute(
            query,
            (hash_password, email)
        )

        db_config.commit()

        cursor.close()
        db_config.close()

        return True, "Password Updated Successfully"

    except Exception as e:
        return False, f"Something wrong in database/utilityDB.py:updatePasswordByEmail(): {e}"
