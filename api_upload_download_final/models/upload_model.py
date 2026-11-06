import sqlite3
from database.db import get_db_connection


class UploadModel:
    @staticmethod
    def save_file(filename, filepath):
        connection = get_db_connection()
        try:
            connection.execute(
                "INSERT INTO uploads (filename, filepath) VALUES (?, ?)",
                (filename, filepath),
            )
            connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            connection.close()

    @staticmethod
    def find_by_filename(filename):
        connection = get_db_connection()
        try:
            return connection.execute(
                "SELECT * FROM uploads WHERE filename = ?", (filename,)
            ).fetchone()
        finally:
            connection.close()
