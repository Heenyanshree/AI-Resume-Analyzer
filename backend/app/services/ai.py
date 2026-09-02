import os
import re
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def local_resume_analysis(resume_text, job_description):
    resume = resume_text.lower()
    jd = job_description.lower()

    jd_words = set(re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.]*\b", jd))
    resume_words = set(re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.]*\b", resume))

    matched = sorted(list(jd_words & resume_words))
    missing = sorted(list(jd_words - resume_words))

    score = int((len(matched) / max(len(jd_words), 1)) * 100)

    suggestions = []

    if score < 60:
        suggestions.append("Add more keywords from the Job Description.")
        suggestions.append("Include missing technical skills in your Skills section.")
    if len(missing) > 0:
        suggestions.append(f"Add skills like: {', '.join(missing[:5])}.")
    suggestions.extend([
        "Write a stronger professional summary tailored to the JD.",
        "Use measurable achievements in your experience section.",
        "Keep ATS-friendly formatting (simple headings, no tables)."
    ])

    summary = (
        f"Results-oriented candidate with relevant technical skills. "
        f"Resume currently matches approximately {score}% of the job requirements. "
        f"Strengthen the profile by adding missing keywords and measurable achievements."
    )

    return {
        "response": f"""
ATS Score: {score}/100

Matched Skills:
{', '.join(matched[:20]) if matched else 'None'}

Missing Skills:
{', '.join(missing[:20]) if missing else 'None'}

Resume Improvements:
{chr(10).join([f"{i+1}. {s}" for i, s in enumerate(suggestions[:5])])}

Professional Resume Summary:
{summary}
"""
    }


def get_resume_suggestions(resume_text, job_description=""):
    prompt = f"""
You are an ATS Resume Expert.

Analyze this resume against the Job Description.

Resume:
{resume_text}

Job Description:
{job_description}

Return:
1. ATS Score out of 100
2. Matched Skills
3. Missing Skills
4. 5 Resume Improvement Suggestions
5. Professional Resume Summary
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return {"response": response.text}

    except Exception:
        # Gemini fail ho to local real-time JD analysis
        return local_resume_analysis(resume_text, job_description)