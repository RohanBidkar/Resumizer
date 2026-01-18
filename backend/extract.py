from llm import get_llm
from models import ExtractedInfo, JDRequirements

def extract_resume_info(resume_text):
    """
    Extract structured information from resume
    
    Uses LLM to parse resume and return JSON with:
    - Name, email, phone
    - Skills list
    - Experience entries
    - Education
    """
    llm = get_llm(temperature=0.3)  # Low temp = more consistent
    
    # Simple prompt
    prompt = f"""Extract information from this resume as JSON:

{{
    "name": "full name or null",
    "email": "email or null",
    "phone": "phone or null",
    "skills": ["list", "of", "skills"],
    "experience": ["job title at company", ...],
    "education": ["degree from school", ...],
    "summary": "brief summary"
}}

Resume:
{resume_text}

Return ONLY the JSON, nothing else."""
    
    try:
        data = llm.extract_json(prompt)
        return ExtractedInfo(**data)
    except Exception as e:
        print(f"   Error: {e}")
        # Return basic fallback
        return ExtractedInfo(
            skills=[],
            summary="Could not parse resume"
        )


def extract_jd_requirements(jd_text):
    """
    Extract requirements from job description
    """
    llm = get_llm(temperature=0.3)
    
    prompt = f"""Extract requirements from this job description as JSON:

{{
    "required_skills": ["skill1", "skill2"],
    "preferred_skills": ["skill1", "skill2"],
    "experience_required": "X years",
    "education_required": "degree"
}}

Job Description:
{jd_text}

Return ONLY the JSON."""
    
    try:
        data = llm.extract_json(prompt)
        return JDRequirements(**data)
    except Exception as e:
        print(f"   Error: {e}")
        return JDRequirements(required_skills=[])


def assess_resume_quality(resume_text):
    """
    Simple quality assessment
    
    Returns: (score, strengths, suggestions)
    """
    llm = get_llm(temperature=0.5)
    
    prompt = f"""Rate this resume quality (0-100) and provide feedback:

Resume:
{resume_text[:1000]}

Return JSON:
{{
    "quality_score": 75,
    "strengths": ["strength 1", "strength 2"],
    "suggestions": ["suggestion 1", "suggestion 2"]
}}"""
    
    try:
        result = llm.extract_json(prompt)
        return (
            float(result.get("quality_score", 70)),
            result.get("strengths", []),
            result.get("suggestions", [])
        )
    except:
        return (70.0, ["Resume parsed"], ["Add more details"])
