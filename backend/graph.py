from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from datetime import datetime
import hashlib
import json

from models import ExtractedInfo, JDRequirements, ScoreBreakdown, ATSScoreResponse, ResumeQualityResponse
from rag import get_rag
from llm import get_llm


class ResumeAnalysisState(TypedDict):
    """State for resume analysis workflow"""
    resume_text: str
    jd_text: Optional[str]
    filename: str
    resume_id: str
    error: Optional[str]
    result: Optional[dict]


def store_resume_node(state: ResumeAnalysisState) -> ResumeAnalysisState:
    """
    Node 1: Store resume in Pinecone for RAG
    """
    print("🧠 Storing resume in vector database...")
    try:
        rag = get_rag()
        
        # Generate unique ID
        resume_id = hashlib.md5(
            f"{state['resume_text'][:100]}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        state["resume_id"] = resume_id
        
        # Store in Pinecone
        rag.store_resume(state["resume_text"], resume_id)
        print(f"   ✅ Stored with ID: {resume_id}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        state["error"] = f"Storage failed: {str(e)}"
    
    return state


def llm_analysis_node(state: ResumeAnalysisState) -> ResumeAnalysisState:
    """
    Node 2: Let LLM do ALL the analysis with comprehensive context
    
    This is the main node - LLM handles:
    - Resume parsing
    - Quality assessment
    - ATS scoring (if JD provided)
    - Suggestions
    """
    print("🤖 LLM analyzing resume with full context...")
    
    try:
        llm = get_llm(temperature=0.3)
        
        # Get RAG context if JD provided
        rag_context = ""
        if state["jd_text"]:
            rag = get_rag()
            results = rag.search(state["jd_text"][:500], top_k=3)
            rag_context = "\n".join([f"- {r['text'][:200]}" for r in results])
        
        # Build comprehensive prompt based on whether JD is provided
        if state["jd_text"]:
            # WITH JD - Full ATS Analysis
            system_prompt = """You are an ATS (Applicant Tracking System) analyzer. 
Analyze the resume against the job description and provide a comprehensive JSON response.

Calculate ATS score (0-100) based on:
- Skills Match (40%): How many required skills are present
- Experience Relevance (30%): How relevant is their experience
- Education Match (15%): Does education meet requirements
- Resume Quality (15%): Formatting, clarity, achievements

Be strict but fair in scoring."""

            user_prompt = f"""**RESUME:**
{state['resume_text']}

**JOB DESCRIPTION:**
{state['jd_text']}

**RELEVANT RESUME SECTIONS (from vector search):**
{rag_context}

Analyze and return JSON:
{{
    "ats_score": 75.5,
    "score_breakdown": {{
        "skills_score": 30.0,
        "experience_score": 22.5,
        "education_score": 12.0,
        "quality_score": 11.0
    }},
    "extracted_info": {{
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "123-456-7890",
        "skills": ["Python", "React", "AWS"],
        "experience": ["Senior Developer at XYZ Corp"],
        "education": ["BS Computer Science"],
        "years_of_experience": 5,
        "summary": "brief summary"
    }},
    "matched_skills": ["Python", "React"],
    "missing_skills": ["Docker", "Kubernetes"],
    "strengths": ["Strong technical background", "Clear achievements"],
    "suggestions": ["Add Docker experience", "Quantify more achievements"],
    "overall_feedback": "Candidate shows solid experience..."
}}"""
        
        else:
            # WITHOUT JD - Quality Assessment Only
            system_prompt = """You are a professional resume reviewer.
Analyze the resume quality and provide constructive feedback.

Quality score (0-100) based on:
- Clarity and formatting
- Quantified achievements
- Skill presentation
- Professional summary"""

            user_prompt = f"""**RESUME:**
{state['resume_text']}

Analyze and return JSON:
{{
    "quality_score": 82.0,
    "extracted_info": {{
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "123-456-7890",
        "skills": ["Python", "React"],
        "experience": ["Senior Developer at XYZ"],
        "education": ["BS Computer Science"],
        "years_of_experience": 5,
        "summary": "brief summary"
    }},
    "strengths": ["Well structured", "Clear skills section"],
    "suggestions": ["Add more quantified achievements"],
    "feedback": "This is a well-crafted resume..."
}}"""
        
        # Get LLM response
        response = llm.extract_json(user_prompt, system_prompt)
        
        # Store result
        state["result"] = response
        print(f"   ✅ Analysis complete!")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        state["error"] = f"Analysis failed: {str(e)}"
    
    return state


def check_for_errors(state: ResumeAnalysisState) -> str:
    """Router: Check if there were any errors"""
    if state.get("error"):
        return "error"
    return "success"


# Build the simple graph
def create_resume_analysis_graph():
    workflow = StateGraph(ResumeAnalysisState)
    
    # Add nodes
    workflow.add_node("store_resume", store_resume_node)
    workflow.add_node("llm_analysis", llm_analysis_node)
    
    # Build flow
    workflow.set_entry_point("store_resume")
    workflow.add_edge("store_resume", "llm_analysis")
    workflow.add_conditional_edges(
        "llm_analysis",
        check_for_errors,
        {
            "success": END,
            "error": END
        }
    )
    
    return workflow.compile()


# Main entry point
async def analyze_resume(resume_text: str, jd_text: Optional[str], filename: str):
    """
    Analyze resume using simplified LLM-centric workflow
    """
    print("\n" + "="*60)
    print("🚀 Resume Analysis (LLM-Powered)")
    print("="*60 + "\n")
    
    # Create graph
    graph = create_resume_analysis_graph()
    
    # Run analysis
    initial_state = ResumeAnalysisState(
        resume_text=resume_text,
        jd_text=jd_text,
        filename=filename,
        resume_id="",
        error=None,
        result=None
    )
    
    final_state = await graph.ainvoke(initial_state)
    
    # Check for errors
    if final_state.get("error"):
        raise Exception(final_state["error"])
    
    result = final_state["result"]
    
    # Format response based on whether JD was provided
    if jd_text:
        # Calculate total_score from components
        breakdown_data = result.get("score_breakdown", {})
        total = (
            breakdown_data.get("skills_score", 0) +
            breakdown_data.get("experience_score", 0) +
            breakdown_data.get("education_score", 0) +
            breakdown_data.get("quality_score", 0)
        )
        breakdown_data["total_score"] = round(total, 2)
        
        # ATS Score Response
        return ATSScoreResponse(
            ats_score=result.get("ats_score", total),
            score_breakdown=ScoreBreakdown(**breakdown_data),
            extracted_info=ExtractedInfo(**result.get("extracted_info", {})),
            matched_skills=result.get("matched_skills", []),
            missing_skills=result.get("missing_skills", []),
            strengths=result.get("strengths", []),
            suggestions=result.get("suggestions", []),
            overall_feedback=result.get("overall_feedback", ""),
            timestamp=datetime.now().isoformat()
        )
    else:
        # Quality Score Response
        return ResumeQualityResponse(
            quality_score=result.get("quality_score", 0),
            extracted_info=ExtractedInfo(**result.get("extracted_info", {})),
            strengths=result.get("strengths", []),
            suggestions=result.get("suggestions", []),
            feedback=result.get("feedback", ""),
            timestamp=datetime.now().isoformat()
        )
