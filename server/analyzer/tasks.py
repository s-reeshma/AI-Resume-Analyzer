import os
import pdfplumber
from celery import shared_task

skills_list = [
    "python","django","react","javascript","sql",
    "html","css","git","github","flask",
    "machine learning","data analysis",
    "excel","microsoft office","ms office",
    "c","c++","java"
]

ROLE_SKILL_MATRICES = {
    "Frontend Developer": ["html", "css", "javascript", "react", "git", "github"],
    "Backend Developer": ["python", "django", "flask", "sql", "git", "github"],
    "Data Analyst": ["python", "excel", "sql", "data analysis", "machine learning"]
}

@shared_task
def analyze_resume_task(file_path, target_role):
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Clean up the temporary file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

    text = text.lower()

    detected_skills = []
    for skill in skills_list:
        if skill.lower() in text:
            detected_skills.append(skill)

    score = len(detected_skills) * 10
    if score > 100:
        score = 100

    suggestions = []
    if "python" not in detected_skills:
        suggestions.append("Add Python projects")
    if "django" not in detected_skills:
        suggestions.append("Mention Django experience")
    if "react" not in detected_skills:
        suggestions.append("Add frontend skills like React")

    matched_skills = []
    missing_skills = []

    if target_role in ROLE_SKILL_MATRICES:
        required_skills = ROLE_SKILL_MATRICES[target_role]
        for skill in required_skills:
            if skill in detected_skills:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

    return {
        "score": score,
        "skills_found": detected_skills,
        "suggestions": suggestions,
        "target_role": target_role,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
