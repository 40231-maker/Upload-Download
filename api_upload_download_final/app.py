import os
from flask import Flask, jsonify

from database.db import init_db
from routes.upload_route import upload_bp
from routes.download_route import download_bp


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        UPLOAD_FOLDER=os.environ.get("UPLOAD_FOLDER", "uploads"),
        DATABASE_PATH=os.environ.get("DATABASE_PATH", "database.db"),
        MAX_FILE_SIZE=30 * 1024,
        MAX_CONTENT_LENGTH=1024 * 1024,
    )
    if test_config:
        app.config.update(test_config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(app.config["DATABASE_PATH"])), exist_ok=True)
    with app.app_context():
        init_db()

    app.register_blueprint(upload_bp, url_prefix="/uploads")
    app.register_blueprint(download_bp, url_prefix="/downloads")

    @app.get("/")
    def home():
        return jsonify({
            "mensagem": "API de Upload e Download funcionando!",
            "rotas": {
                "health": "GET /health",
                "upload": "POST /uploads/upload (multipart/form-data, campo 'file')",
                "download": "GET /downloads/download/<filename>"
            }
        }), 200

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    @app.errorhandler(413)
    def payload_too_large(_error):
        return jsonify({"erro": "Requisição excede o limite permitido."}), 413

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
