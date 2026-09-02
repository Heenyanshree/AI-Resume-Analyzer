# 🚀 AI Resume Analyzer

![React](https://img.shields.io/badge/React-20232A?style=for-the-badge\&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge\&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge\&logo=vercel)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge)

A Full Stack AI-powered Resume Analyzer built with **React**, **FastAPI**, and **Google Gemini AI** that analyzes resumes, calculates ATS scores, compares resumes with Job Descriptions, and generates AI-powered resume improvement suggestions.

---

## 🌐 Live Demo

* **Frontend:** https://ai-resume-analyzer.vercel.app
* **Backend:** `https://ai-resume-analyzer-api-5qm8.onrender.com`

---

## ✨ Features

* 📄 Upload PDF Resume
* 📊 ATS Score Analysis
* 🎯 Job Description Match
* ✅ Matched & Missing Skills
* 🤖 AI Resume Suggestions
* 📑 Download PDF Report
* 📈 Skills Analytics
* 📱 Modern Responsive UI
* ☁️ Live Deployment on Vercel & Render

---

## 🛠️ Tech Stack

| Frontend   | Backend    | AI                 | Deployment |
| ---------- | ---------- | ------------------ | ---------- |
| React      | FastAPI    | Google Gemini AI   | Vercel     |
| JavaScript | Python     | Google GenAI SDK   | Render     |
| Recharts   | SQLAlchemy | Prompt Engineering | GitHub     |

---

## 📂 Project Structure

```text
AI-Resume-Analyzer/
│
├── frontend/
│   ├── src/
│   ├── App.jsx
│   └── App.css
│
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── models/
│   │   ├── auth/
│   │   └── main.py
│   ├── requirements.txt
│   └── uploads/
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Heenyanshree/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔑 Environment Variables

Create a `.env` file inside the `backend` folder.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## 🚀 Workflow

1. Upload Resume
2. Extract PDF Text
3. Calculate ATS Score
4. Compare with Job Description
5. Identify Matched & Missing Skills
6. Generate AI Suggestions
7. Download PDF Report

---

## 🎯 Future Improvements

* Resume Version Comparison
* Cover Letter Generator
* Multi-language Support
* Recruiter Dashboard
* Resume Templates

---

## 👩‍💻 Author

**Heenyanshree**

* GitHub: https://github.com/Heenyanshree
* LinkedIn: https://www.linkedin.com/in/heenyan-shree/
