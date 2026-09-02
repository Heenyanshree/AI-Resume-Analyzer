import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_resume_suggestions(resume_text, job_description):
    prompt = f"""
You are an ATS Resume Expert.

Resume:
{resume_text}

Job Description:
{job_description}

Return:
1. ATS score out of 100
2. Missing skills
3. 5 resume improvement suggestions
4. Better summary for the resume.
"""

    # Retry 3 times
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )

            return {"response": response.text}

        except Exception as e:
            error = str(e)

            # Retry only on 503 errors
            if "503" in error and attempt < 2:
                time.sleep(3 * (attempt + 1))   # 3s, then 6s
                continue

            return {
                "response": f"AI is temporarily busy. Please try again in a few seconds.\n\nError: {error}"
            }