from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import shutil
import fitz  # PyMuPDF
import re

from app.services.ats import calculate_ats_score
from app.services.ai import get_resume_suggestions

router = APIRouter(prefix="/upload", tags=["Resume Upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = [".pdf", ".docx"]


# ---------------- Upload Resume ----------------
@router.post("/")
async def upload_resume(file: UploadFile = File(...)):
    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = ""

    if extension == ".pdf":
        doc = fitz.open(file_path)
        for page in doc:
            extracted_text += page.get_text()
        doc.close()
    else:
        extracted_text = "DOCX extraction coming in next update."

    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename,
        "text": extracted_text[:3000]
    }


# ---------------- Analyze Resume ----------------
@router.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    extension = os.path.splitext(file.filename)[1].lower()

    if extension != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF supported."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = fitz.open(file_path)

    text = ""
    for page in doc:
        text += page.get_text()

    page_count = len(doc)
    word_count = len(text.split())

    doc.close()

    ats = calculate_ats_score(text)

    return {
        "filename": file.filename,
        "pages": page_count,
        "words": word_count,
        "text": text[:3000],
        "ats_score": ats["score"],
        "matched_skills": ats["matched"],
        "missing_skills": ats["missing"]
    }


# ---------------- Resume vs Job Description ----------------
class JobDescription(BaseModel):
    resume_text: str
    job_description: str


@router.post("/match")
def match_resume(data: JobDescription):
    resume = data.resume_text.lower()
    jd = data.job_description.lower()

    jd_words = set(re.findall(r"\b[a-zA-Z]+\b", jd))
    resume_words = set(re.findall(r"\b[a-zA-Z]+\b", resume))

    matched = jd_words & resume_words
    missing = jd_words - resume_words

    score = int((len(matched) / max(len(jd_words), 1)) * 100)

    return {
        "match_score": score,
        "matched_skills": sorted(list(matched))[:20],
        "missing_skills": sorted(list(missing))[:20]
    }


# ---------------- AI Resume Suggestions ----------------
class AIRequest(BaseModel):
    resume_text: str
    job_description: str = ""


@router.post("/suggestions")
def ai_suggestions(data: AIRequest):
    result = get_resume_suggestions(
        data.resume_text,
        data.job_description
    )

    # Frontend expects: data.response
    return result