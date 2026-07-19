"""FastAPI app with graceful error handling."""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from .config import settings
from .retriever import PDFRetriever
from .utils import validate_query, validate_pdf_file, ValidationError

app = FastAPI(title="Secure RAG API", version="1.0.0")
retriever = PDFRetriever(api_key=settings.OPENAI_API_KEY)

@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc: ValidationError):
    return JSONResponse(status_code=400, content={"error": "Validation Error", "detail": str(exc)})

@app.get("/")
def root():
    return {"status": "ok", "env": settings.APP_ENV, "debug": settings.DEBUG}

@app.get("/health")
def health():
    return {"status": "healthy", "documents_loaded": len(retriever.documents)}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        validate_pdf_file(file.filename)
        contents = await file.read()
        result = retriever.load_pdf(contents, filename=file.filename)
        return result
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    finally:
        await file.close()

@app.post("/query")
async def query(question: str):
    try:
        cleaned = validate_query(question)
        return retriever.query(cleaned)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

@app.delete("/documents")
async def clear_documents():
    retriever.clear()
    return {"status": "cleared", "message": "All documents removed."}