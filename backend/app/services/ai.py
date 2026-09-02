import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite"
]

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

    last_error = ""

    for model in MODELS:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                return {"response": response.text}

            except Exception as e:
                last_error = str(e)

                if "503" in last_error and attempt < 2:
                    time.sleep(2 * (attempt + 1))
                    continue
                break

    return {
        "response": "AI is temporarily busy. Please try again in 30 seconds."
    }