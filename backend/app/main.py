from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Resume Analyzer API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router (prefix auth.py me already hai)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API Running 🚀"}

@app.get("/health")
def health():
    return {"status": "healthy"}