import pytest
from io import BytesIO
from reportlab.pdfgen import canvas
from src.retriever import PDFRetriever
from src.utils import ValidationError

def create_pdf_bytes(text="Test content."):
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    c.drawString(100, 700, text)
    c.save()
    buffer.seek(0)
    return buffer.read()

class TestLoadPdf:
    def test_load_valid_pdf(self):
        r = PDFRetriever()
        result = r.load_pdf(create_pdf_bytes("AI is cool.\n\nML is a subset."), "test.pdf")
        assert result["status"] == "success"
        assert result["chunks"] > 0

    def test_empty_bytes_raises(self):
        with pytest.raises(ValidationError):
            PDFRetriever().load_pdf(b"", "empty.pdf")

    def test_corrupt_pdf_raises(self):
        with pytest.raises(ValidationError):
            PDFRetriever().load_pdf(b"not a pdf", "bad.pdf")

class TestQuery:
    def test_query_no_documents(self):
        r = PDFRetriever()
        result = r.query("What is AI?")
        assert "No documents loaded" in result["answer"]

    def test_query_with_documents(self):
        r = PDFRetriever()
        r.load_pdf(create_pdf_bytes("Artificial Intelligence is the future."), "ai.pdf")
        result = r.query("What is AI?")
        assert len(result["chunks"]) > 0
