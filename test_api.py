import os
os.environ["OPENAI_API_KEY"] = "sk-test"
os.environ["PINECONE_API_KEY"] = "pc-test"
os.environ["APP_ENV"] = "testing"
os.environ["DEBUG"] = "False"

from fastapi.testclient import TestClient
from io import BytesIO
from reportlab.pdfgen import canvas
from src.api import app, retriever

client = TestClient(app)

def create_pdf_bytes(text="Test."):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 700, text)
    c.save()
    buffer.seek(0)
    return buffer.read()

class TestUpload:
    def test_valid_pdf(self):
        pdf = create_pdf_bytes("Content here.")
        response = client.post("/upload", files={"file": ("test.pdf", pdf, "application/pdf")})
        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_empty_file(self):
        response = client.post("/upload", files={"file": ("empty.pdf", b"", "application/pdf")})
        assert response.status_code == 400

    def test_non_pdf(self):
        response = client.post("/upload", files={"file": ("hack.exe", b"bad", "application/octet-stream")})
        assert response.status_code == 400

class TestQuery:
    def test_empty_query(self):
        response = client.post("/query", params={"question": "   "})
        assert response.status_code == 400

    def test_too_short(self):
        response = client.post("/query", params={"question": "ab"})
        assert response.status_code == 400
