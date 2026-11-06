import logging
import os

from flask import current_app, jsonify, request
from werkzeug.utils import secure_filename

from models.upload_model import UploadModel

logger = logging.getLogger(__name__)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "txt"}


class UploadController:
    @staticmethod
    def arquivo_permitido(filename):
        return bool(filename and "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS)

    @staticmethod
    def upload_file():
        if "file" not in request.files:
            return jsonify({"erro": "Nenhum arquivo enviado. Use o campo 'file'."}), 400

        uploaded_file = request.files["file"]
        if not uploaded_file or not uploaded_file.filename:
            return jsonify({"erro": "Nome do arquivo vazio."}), 400

        filename = secure_filename(uploaded_file.filename)
        if not filename:
            return jsonify({"erro": "Nome de arquivo inválido."}), 400
        if not UploadController.arquivo_permitido(filename):
            return jsonify({
                "erro": "Tipo de arquivo não permitido.",
                "tipos_permitidos": sorted(ALLOWED_EXTENSIONS),
            }), 400

        # Verifica o tamanho do arquivo, não o tamanho total do formulário multipart.
        content = uploaded_file.stream.read(current_app.config["MAX_FILE_SIZE"] + 1)
        if len(content) > current_app.config["MAX_FILE_SIZE"]:
            return jsonify({"erro": "Arquivo excede o tamanho máximo permitido (30 KB)."}), 413
        uploaded_file.stream.seek(0)

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        file_path = os.path.join(upload_folder, filename)
        if os.path.exists(file_path) or UploadModel.find_by_filename(filename):
            return jsonify({"erro": "Já existe um arquivo com esse nome."}), 409

        try:
            uploaded_file.save(file_path)
            if not UploadModel.save_file(filename, file_path):
                if os.path.exists(file_path):
                    os.remove(file_path)
                return jsonify({"erro": "Já existe um arquivo com esse nome."}), 409
        except Exception:
            logger.exception("Falha ao salvar arquivo enviado")
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({"erro": "Não foi possível salvar o arquivo."}), 500

        logger.info("Upload concluído: %s | IP: %s", filename, request.remote_addr)
        return jsonify({
            "mensagem": "Arquivo salvo com sucesso!",
            "arquivo": filename,
            "tamanho_bytes": len(content),
            "link_download": f"/downloads/download/{filename}",
        }), 201
