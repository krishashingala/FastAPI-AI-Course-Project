from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import students, documents, chat

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI AI Course Project",
    description="Learning backend: CRUD, SQLite, PDF upload, and starter document Q&A.",
    version="1.0.0",
)

# For local learning. In production, set allow_origins to your exact frontend URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(documents.router)
app.include_router(chat.router)


@app.get("/", tags=["Home"])
def home():
    return {"message": "FastAPI AI Course Project is running", "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

UI_DIR = Path(__file__).resolve().parent.parent / "ui"
app.mount("/ui", StaticFiles(directory=UI_DIR, html=True), name="ui")