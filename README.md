# FastAPI AI & RAG Starter Project

A beginner-friendly end-to-end FastAPI backend for learning:
- Student CRUD API (SQLite + SQLAlchemy)
- PDF upload and text extraction
- Document listing/deletion
- Simple retrieval-based Q&A endpoint (starter extractive response; plug in an LLM later)
- Swagger docs, validation, health check

## 1. Requirements
- Python 3.10+
- VS Code

## 2. Setup (Windows PowerShell)
Open this folder in VS Code, then Terminal > New Terminal:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3. Open API docs
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health: http://127.0.0.1:8000/health

## 4. Try Student CRUD
POST `/students` body:
```json
{"name":"Venisha","age":22,"course":"MSc AI"}
```
Then GET `/students`, GET `/students/1`, PUT `/students/1`, DELETE `/students/1`.

## 5. Try PDF endpoint
POST `/documents/upload` in Swagger; select a PDF. Text is extracted and metadata stored in SQLite.
GET `/documents` lists uploaded docs.
POST `/chat` with:
```json
{"question":"What does the document say about skills?","document_id":1}
```
The included chat uses simple keyword-based retrieval and returns matching excerpts. It is an educational RAG skeleton, not a full LLM-powered chatbot yet.

## Project structure
```text
app/
  main.py
  database.py
  models.py
  schemas.py
  routers/
    students.py
    documents.py
    chat.py
  services/
    pdf_service.py
    retrieval_service.py
uploads/             # uploaded PDFs
requirements.txt
.env.example
```

## Notes
- Uploaded files and SQLite database are local development data.
- Do not upload confidential or sensitive documents to an untrusted deployment.
- For production, add authentication, file size limits, malware scanning, robust chunking/vector DB, LLM integration, rate limiting, and deployment secrets.
