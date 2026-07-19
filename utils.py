"""Validation helpers."""
from typing import Optional

class ValidationError(Exception):
    pass

def validate_query(query: Optional[str]) -> str:
    if query is None:
        raise ValidationError("Query cannot be None. Ask me something!")
    cleaned = query.strip()
    if len(cleaned) == 0:
        raise ValidationError("Query cannot be empty.")
    if len(cleaned) < 3:
        raise ValidationError("Query too short. At least 3 characters.")
    if len(cleaned) > 500:
        raise ValidationError("Query too long. Max 500 characters.")
    return cleaned

def validate_pdf_file(filename: Optional[str]) -> str:
    if filename is None or filename.strip() == "":
        raise ValidationError("No file provided. Upload a PDF!")
    if not filename.lower().endswith(".pdf"):
        raise ValidationError(f"Invalid file: '{filename}'. Only PDFs allowed.")
    return filename.strip()