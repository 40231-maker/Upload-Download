from flask import jsonfy, send_from_directory

UPLOAD_FOLDER = 'uploads'

class DownloadController:

    @staticmethod
    def download_file(filename):
        try:
            return send_from_directory(UPLOAD_FOLDER, as_attachment-True)
        except FileNotFoundError:
            return jsonfy({"error" "Arquivo não encontrado"})