from pydantic import BaseModel, Field, field_validator
import pydantic as org_pydantic
from typing import Optional, List
from datetime import datetime


class ExtractedInfo(BaseModel):
    """Structured information extracted from resume"""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    experience: List[str] = Field(default_factory=list)
    education: List[str] = Field(default_factory=list)
    summary: Optional[str] = None
    years_of_experience: Optional[int] = None

    @org_pydantic.field_validator('years_of_experience', mode='before')
    @classmethod
    def parse_years(cls, v):
        if isinstance(v, str):
            # Extract first number found or return 0
            import re
            match = re.search(r'\d+', v)
            if match:
                return int(match.group())
            return 0
        return v


class JDRequirements(BaseModel):
    """Extracted requirements from job description"""
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    experience_required: Optional[str] = None
    education_required: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)


class ScoreBreakdown(BaseModel):
    """Detailed scoring breakdown"""
    skills_score: float = Field(..., ge=0, le=40, description="Skills match score (max 40)")
    experience_score: float = Field(..., ge=0, le=30, description="Experience relevance score (max 30)")
    education_score: float = Field(..., ge=0, le=15, description="Education match score (max 15)")
    quality_score: float = Field(..., ge=0, le=15, description="Resume quality score (max 15)")
    total_score: float = Field(..., ge=0, le=100, description="Total ATS score (0-100)")


class ATSScoreResponse(BaseModel):
    """Complete ATS analysis response"""
    ats_score: float = Field(..., ge=0, le=100, description="Overall ATS score")
    score_breakdown: ScoreBreakdown
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    overall_feedback: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ResumeAnalysisRequest(BaseModel):
    """Request model for resume analysis"""
    resume_text: str
    jd_text: Optional[str] = None
    filename: str = "resume.pdf"


class ResumeQualityResponse(BaseModel):
    """Response for resume-only analysis (without JD)"""
    quality_score: float = Field(..., ge=0, le=100)
    extracted_info: ExtractedInfo
    strengths: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    feedback: str
    timestamp: datetime = Field(default_factory=datetime.now)
