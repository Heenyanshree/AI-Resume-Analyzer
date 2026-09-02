import os
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

# Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_resume_suggestions(resume_text, job_description):
    prompt = f"""
You are an ATS Resume Expert.

Resume:
{resume_text}

Job Description:
{job_description}

Analyze the resume and return the answer in this format:

ATS Score: XX/100

Missing Skills:
- Skill 1
- Skill 2

Resume Improvement Suggestions:
1. Suggestion
2. Suggestion
3. Suggestion
4. Suggestion
5. Suggestion

Professional Summary:
Write a better professional summary tailored to the job description.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        # Safe fallback if response is empty
        if hasattr(response, "text") and response.text:
            return {"response": response.text}

        return {"response": "AI could not generate suggestions."}

    except Exception as e:
        print("GEMINI ERROR:", e)
        return {"response": f"AI Error: {str(e)}"}