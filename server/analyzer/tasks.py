import os
import pdfplumber
from celery import shared_task
from django.contrib.auth import get_user_model
from .models import ResumeAnalysis

User = get_user_model()

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
def analyze_resume_task(file_path, target_role, file_name="unknown", user_id=None):
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

    detected_skills = [s for s in skills_list if s.lower() in text]

    matched_skills = []
    missing_skills = []

    if target_role in ROLE_SKILL_MATRICES:
        required_skills = ROLE_SKILL_MATRICES[target_role]

        for skill in required_skills:
            if skill in detected_skills:
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)

        # Dynamic role-based score
        score = int((len(matched_skills) / len(required_skills)) * 100) if required_skills else 100

        # Dynamic suggestions
        suggestions = [
            f"Add experience or projects with {skill.upper() if skill in ['html', 'css', 'sql', 'git'] else skill.capitalize()}"
            for skill in missing_skills
        ]
    else:
        score = min(len(detected_skills) * 10, 100)

        suggestions = []
        if "python" not in detected_skills:
            suggestions.append("Add Python projects")
        if "django" not in detected_skills:
            suggestions.append("Mention Django experience")
        if "react" not in detected_skills:
            suggestions.append("Add frontend skills like React")

    if user_id:
        try:
            user = User.objects.get(id=user_id)
            ResumeAnalysis.objects.create(
                user=user,
                file_name=file_name,
                score=score,
                skills_found=detected_skills,
                suggestions=suggestions,
                matched_skills=matched_skills,
                missing_skills=missing_skills,
                target_role=target_role or "",
            )
        except User.DoesNotExist:
            pass

    return {
        "score": score,
        "skills_found": detected_skills,
        "suggestions": suggestions,
        "target_role": target_role,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
