import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_resume_suggestions(resume_text, job_description):
    prompt = f"""
You are an ATS Resume Expert.

Analyze the resume against the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Return your answer in this format:

ATS Score: XX/100

Missing Skills:
- Skill 1
- Skill 2

Resume Improvements:
1. Suggestion 1
2. Suggestion 2
3. Suggestion 3
4. Suggestion 4
5. Suggestion 5

Professional Resume Summary:
(Write a better professional summary.)
"""

    # Stable models (Free Tier)
    models = [
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash"
    ]

    for model in models:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                return {
                    "response": response.text
                }

            except Exception as e:
                error = str(e)

                # Retry only if Gemini is busy
                if "503" in error and attempt < 2:
                    time.sleep(3 * (attempt + 1))
                    continue

                break

    return {
        "response": (
            "⚠️ Gemini AI is temporarily experiencing high demand.\n\n"
            "Please try again after 30-60 seconds."
        )
    }