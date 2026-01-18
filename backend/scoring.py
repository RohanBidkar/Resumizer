
from models import ExtractedInfo, JDRequirements, ScoreBreakdown
from rag import get_rag

def calculate_skills_score(resume_info, jd_requirements):
    # Normalize skills to lowercase
    resume_skills = {s.lower() for s in resume_info.skills}
    required_skills = {s.lower() for s in jd_requirements.required_skills}
    
    if not required_skills:
        return 35.0, [], []
    
    # Find matches
    matched = resume_skills & required_skills
    missing = required_skills - resume_skills
    
    # Calculate score
    match_rate = len(matched) / len(required_skills)
    score = 40 * match_rate
    
    return (
        round(score, 2),
        [s.title() for s in matched],
        [s.title() for s in missing]
    )


def calculate_experience_score(resume_info, resume_id, jd_text):
        rag = get_rag()
        results = rag.search(jd_text[:500], top_k=3)
        
        if not results:
            return 15.0
        avg_score = sum(r["score"] for r in results) / len(results)
        experience_score = avg_score * 30
        
        return round(min(30, max(0, experience_score)), 2)
    except:
        return 20.0  # Default


def calculate_education_score(resume_info, jd_requirements):
    if not jd_requirements.education_required:
        return 12.0  # No requirement = good score
    
    education_text = " ".join(resume_info.education).lower()
    required = jd_requirements.education_required.lower()
    
    # Check if bachelor, master, etc mentioned
    if "master" in required and "master" in education_text:
        return 15.0
    elif "bachelor" in required and ("bachelor" in education_text or "master" in education_text):
        return 15.0
    elif education_text:
        return 10.0
    else:
        return 5.0


def calculate_ats_score(resume_info, jd_requirements, resume_id, jd_text, quality_score):
    # Calculate each component
    skills_score, matched, missing = calculate_skills_score(resume_info, jd_requirements)
    experience_score = calculate_experience_score(resume_info, resume_id, jd_text)
    education_score = calculate_education_score(resume_info, jd_requirements)
    quality_component = round((quality_score / 100) * 15, 2)
    
    # Create breakdown
    breakdown = ScoreBreakdown(
        skills_score=skills_score,
        experience_score=experience_score,
        education_score=education_score,
        quality_score=quality_component,
        total_score=round(skills_score + experience_score + education_score + quality_component, 2)
    )
    
    return (breakdown, matched, missing)
