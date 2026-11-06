import os
from flask import current_app, jsonify, send_from_directory
from models.download_model import DownloadModel


class DownloadController:
    @staticmethod
    def download_file(filename):
        record = DownloadModel.find_by_filename(filename)
        if not record:
            return jsonify({"erro": "Arquivo não encontrado."}), 404

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        if not os.path.isfile(os.path.join(upload_folder, filename)):
            return jsonify({"erro": "Arquivo não encontrado."}), 404

        return send_from_directory(upload_folder, filename, as_attachment=True)
