import io
import os
import tempfile
import unittest

from app import create_app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = create_app({
            "TESTING": True,
            "UPLOAD_FOLDER": os.path.join(self.temp.name, "uploads"),
            "DATABASE_PATH": os.path.join(self.temp.name, "test.db"),
            "MAX_FILE_SIZE": 30 * 1024,
        })
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp.cleanup()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_upload_and_download(self):
        response = self.client.post(
            "/uploads/upload",
            data={"file": (io.BytesIO(b"teste"), "teste.txt")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 201)
        download = self.client.get("/downloads/download/teste.txt")
        self.assertEqual(download.status_code, 200)
        self.assertEqual(download.data, b"teste")

    def test_invalid_extension(self):
        response = self.client.post(
            "/uploads/upload",
            data={"file": (io.BytesIO(b"x"), "programa.exe")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 400)

    def test_duplicate_filename(self):
        first = self.client.post(
            "/uploads/upload",
            data={"file": (io.BytesIO(b"um"), "igual.txt")},
            content_type="multipart/form-data",
        )
        second = self.client.post(
            "/uploads/upload",
            data={"file": (io.BytesIO(b"dois"), "igual.txt")},
            content_type="multipart/form-data",
        )
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 409)

    def test_file_too_large(self):
        response = self.client.post(
            "/uploads/upload",
            data={"file": (io.BytesIO(b"x" * (30 * 1024 + 1)), "grande.txt")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 413)

    def test_missing_file_download(self):
        response = self.client.get("/downloads/download/inexistente.txt")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
