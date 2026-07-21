## 📌 Overview

In this task, I improved the reliability of my RAG chatbot by implementing testing and robust error handling. The application now validates user inputs, handles invalid PDF uploads gracefully, prevents crashes from unexpected errors, and includes unit tests for key components such as the Retriever and API.

---

## 🚀 Features Implemented

- 🧪 Unit testing using `pytest`
- 📄 Validation for empty or invalid PDF uploads
- ❌ Validation for empty user queries
- ⚠️ User-friendly error messages
- ✅ Graceful exception handling
- 🔍 Improved application stability

---

## 🛠️ Technologies Used

- Python 3.x
- FastAPI
- Streamlit
- pytest
- LangChain
- FAISS

---

## 📂 Project Structure

```text
rag-chatbot/
│
├── src/
│   ├── api.py
│   ├── retriever.py
│   ├── config.py
│   └── __init__.py
│
├── tests/
│   ├── test_api.py
│   └── test_retriever.py
│
├── uploads/
├── vectorstore/
├── app.py
├── requirements.txt
└── README.md
```

---

## 🧪 Unit Testing

The project uses **pytest** to verify that the API and Retriever behave correctly under normal and edge-case conditions.

### Install pytest

```bash
pip install pytest
```

### Run Tests

```bash
pytest
```

or

```bash
pytest tests/
```

---

## ✅ Test Cases

### Retriever Tests

- Vector store creation
- Loading existing vector store
- Retriever object creation
- Missing vector store handling

### API Tests

- Successful PDF upload
- Empty PDF upload
- Invalid file type
- Empty user query
- Invalid API request

---

## ⚠️ Error Handling

The application now handles common errors gracefully.

### PDF Upload

- Empty file
- Invalid file format
- Corrupted PDF

### User Query

- Empty prompt
- Missing request body

### Internal Errors

- Missing vector database
- API exceptions
- Unexpected server errors

Instead of crashing, the application returns meaningful error messages.

Example:

```json
{
  "detail": "Please upload a valid PDF file."
}
```

---

## ▶️ Running the Application

### Backend

```bash
uvicorn src.api:app --reload
```

### Frontend

```bash
streamlit run app.py
```

### Run Tests

```bash
pytest
```

---

## 📚 Concepts Learned

- pytest Basics
- Unit Testing
- Test Cases
- Edge Case Handling
- Exception Handling
- HTTP Error Responses
- Application Reliability

---

## 📸 Expected Output

- Valid PDFs upload successfully.
- Invalid PDFs return friendly error messages.
- Empty questions are rejected.
- API handles exceptions without crashing.
- Unit tests pass successfully.

---
