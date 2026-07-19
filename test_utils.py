import pytest
from src.utils import validate_query, validate_pdf_file, ValidationError

class TestValidateQuery:
    def test_valid_query(self):
        assert validate_query("  What is AI?  ") == "What is AI?"
    
    def test_none_query_raises(self):
        with pytest.raises(ValidationError):
            validate_query(None)
    
    def test_empty_string_raises(self):
        with pytest.raises(ValidationError):
            validate_query("   ")
    
    def test_too_short_raises(self):
        with pytest.raises(ValidationError):
            validate_query("ab")
    
    def test_too_long_raises(self):
        with pytest.raises(ValidationError):
            validate_query("a" * 501)

class TestValidatePdfFile:
    def test_valid_pdf(self):
        assert validate_pdf_file("doc.pdf") == "doc.pdf"
    
    def test_none_filename_raises(self):
        with pytest.raises(ValidationError):
            validate_pdf_file(None)
    
    def test_non_pdf_raises(self):
        with pytest.raises(ValidationError):
            validate_pdf_file("doc.txt")
