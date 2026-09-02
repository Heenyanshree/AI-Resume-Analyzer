def calculate_ats_score(resume_text, jd_text=""):
    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    # Default skills
    if jd_text.strip() == "":
        required_skills = [
            "python",
            "sql",
            "excel",
            "power bi",
            "docker",
            "fastapi",
        ]
    else:
        required_skills = list(set(jd_text.split()))

    matched = []
    missing = []

    for skill in required_skills:
        if skill in resume_text:
            matched.append(skill)
        else:
            missing.append(skill)

    score = int((len(matched) / len(required_skills)) * 100)

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
    }