from database.db import get_db_connection


class DownloadModel:
    @staticmethod
    def find_by_filename(filename):
        connection = get_db_connection()
        try:
            return connection.execute(
                "SELECT * FROM uploads WHERE filename = ?", (filename,)
            ).fetchone()
        finally:
            connection.close()
