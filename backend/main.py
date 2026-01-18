from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import Config
from pinecone import Pinecone
from parse import extract_text
from graph import analyze_resume
from models import ATSScoreResponse, ResumeQualityResponse
from typing import Optional
import traceback
import uvicorn
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Check critical env vars
    print("🚀 Starting Resume RAG Analyzer...")
    if not Config.GROQ_API_KEY:
        print("⚠️ WARNING: GROQ_API_KEY is missing! Analysis will fail.")
    else:
        print("✅ GROQ_API_KEY found.")
        
    if not Config.PINECONE_API_KEY:
        print("⚠️ WARNING: PINECONE_API_KEY is missing! RAG will fail.")
    else:
        print("✅ PINECONE_API_KEY found.")
        
    yield
    # Shutdown logic (if any)

app = FastAPI(
    title="Resume RAG Analyzer",
    description="AI-powered ATS score calculator using RAG (LangGraph + ChatGroq + Pinecone)",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
def api_root():
    """API Root endpoint"""
    return {
        "message": "Resume RAG Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "analyze": "POST /api/analyze - Upload resume + optional JD for ATS score",
            "health": "GET /api/health - Service health check"
        }
    }


@app.get("/api/health")
def health_check():
    """
    Health check endpoint with service status
    """
    try:
        pc = Pinecone(api_key=Config.PINECONE_API_KEY)
        pinecone_status = "connected"
    except Exception as e:
        pinecone_status = f"error: {str(e)}"
    
    groq_status = "configured" if Config.GROQ_API_KEY else "missing"
    
    return {
        "status": "healthy",
        "services": {
            "pinecone": pinecone_status,
            "groq": groq_status,
            "embedding_model": Config.EMBEDDING_MODEL
        },
        "config": {
            "model": Config.GROQ_MODEL,
            "index": Config.PINECONE_INDEX_NAME,
            "embedding_dim": Config.EMBEDDING_DIMENSION
        }
    }


@app.post("/api/analyze")
async def analyze_resume_endpoint(
    resume: UploadFile = File(..., description="Resume file (PDF, DOC, or DOCX)"),
    jd: Optional[UploadFile] = File(None, description="Optional Job Description file"),
    jd_text: Optional[str] = Form(None, description="Or provide JD as text")
):
    try:
        if not resume.filename:
            raise HTTPException(status_code=400, detail="Resume filename is required")
        
        allowed_extensions = ['.pdf', '.doc', '.docx']
        resume_ext = resume.filename.lower()[resume.filename.rfind('.'):]
        if resume_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported resume format. Allowed: {', '.join(allowed_extensions)}"
            )
        
        resume_bytes = await resume.read()
        resume_text = extract_text(resume_bytes, resume.filename)
        
        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Resume text extraction failed or resume is too short"
            )
        
        print(f"📄 Resume extracted: {len(resume_text)} characters")
        
        jd_content = None
        if jd:
            jd_bytes = await jd.read()
            jd_content = extract_text(jd_bytes, jd.filename)
            print(f"📋 JD extracted: {len(jd_content)} characters")
        elif jd_text:
            jd_content = jd_text
            print(f"📋 JD provided as text: {len(jd_content)} characters")
        
        result = await analyze_resume(
            resume_text=resume_text,
            jd_text=jd_content,
            filename=resume.filename
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        print(f" Error in analysis: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )


@app.post("/api/extract")
async def extract_resume_info_endpoint(
    resume: UploadFile = File(..., description="Resume file to extract information from")
):
    try:
        resume_bytes = await resume.read()
        resume_text = extract_text(resume_bytes, resume.filename)
        
        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Resume text extraction failed"
            )
        
        from extract import extract_resume_info
        info = extract_resume_info(resume_text)
        
        return {
            "filename": resume.filename,
            "extracted_info": info,
            "text_length": len(resume_text),
            "preview": resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
        }
        
    except Exception as e:
        print(f"❌ Error in extraction: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Extraction failed: {str(e)}"
        )


@app.get("/api/stats")
def get_pinecone_stats():
    try:
        from rag import get_pinecone_rag
        rag = get_pinecone_rag()
        stats = rag.get_stats()
        return {
            "index_name": Config.PINECONE_INDEX_NAME,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------
# SERVE FRONTEND (Production Mode)
# -------------------------------------------
# Mount the built React app (SPA)
# Check if frontend dist folders exist (Production)
frontend_dist = os.path.join(os.path.dirname(__file__), "../frontend/dist")

if os.path.exists(frontend_dist):
    # Mount assets (js, css, etc.)
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    # Catch-all route for SPA (React Router)
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Don't catch API routes (they are defined above)
        if full_path.startswith("api"):
             raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # Check if a specific file is requested (e.g. favicon.ico, logo.png)
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
            
        # Otherwise return index.html for React Router to handle
        return FileResponse(os.path.join(frontend_dist, "index.html"))

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
