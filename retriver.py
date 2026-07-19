"""PDF Retriever — loads PDFs, extracts text, simulates RAG."""
import io
from typing import List, Optional
from PyPDF2 import PdfReader
from .utils import ValidationError

class PDFRetriever:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.documents: List[str] = []

    def load_pdf(self, file_bytes: bytes, filename: str = "unknown.pdf") -> dict:
        if not file_bytes or len(file_bytes) == 0:
            raise ValidationError("Uploaded file is empty.")
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
        except Exception as e:
            raise ValidationError(f"Could not read PDF '{filename}': {str(e)}")
        if len(reader.pages) == 0:
            raise ValidationError(f"PDF '{filename}' has no pages.")
        
        full_text = ""
        for page in reader.pages:
            try:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
            except Exception:
                continue
        
        cleaned = full_text.strip()
        if len(cleaned) == 0:
            raise ValidationError(f"PDF '{filename}' has no extractable text.")
        
        chunks = [c.strip() for c in cleaned.split("\n\n") if c.strip()]
        if len(chunks) == 0:
            raise ValidationError("Could not split into chunks.")
        
        self.documents.extend(chunks)
        preview = cleaned[:200] + "..." if len(cleaned) > 200 else cleaned
        
        return {
            "status": "success",
            "filename": filename,
            "pages": len(reader.pages),
            "chunks": len(chunks),
            "preview": preview,
        }

    def query(self, question: str, top_k: int = 3) -> dict:
        if not self.documents:
            return {
                "answer": "No documents loaded yet. Upload a PDF first! 📄",
                "chunks": [],
            }
        keywords = set(question.lower().split())
        scored = []
        for doc in self.documents:
            score = len(keywords.intersection(set(doc.lower().split())))
            if score > 0:
                scored.append((score, doc))
        
        scored.sort(reverse=True)
        top_chunks = [doc for _, doc in scored[:top_k]]
        
        if not top_chunks:
            return {
                "answer": "I couldn't find relevant info. Try rephrasing!",
                "chunks": [],
            }
        
        answer = f"Based on the document: {top_chunks[0][:300]}..."
        return {"answer": answer, "chunks": top_chunks}

    def clear(self) -> None:
        self.documents = []