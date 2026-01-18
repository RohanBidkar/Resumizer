/**
 * Resume Analyzer API Service
 * 
 * This file handles all communication between the React frontend and FastAPI backend.
 * It provides easy-to-use functions for uploading resumes and getting ATS scores.
 */

// Backend URL - Automatically detects dev (localhost:8000) vs prod (relative path)
const API_BASE_URL = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : '');

/**
 * Analyze resume and optionally a job description
 * 
 * @param {File} resumeFile - Resume file (PDF or DOCX)
 * @param {File|null} jdFile - Optional job description file
 * @param {string|null} jdText - Optional job description as text
 * @returns {Promise<Object>} Analysis result with ATS score
 * 
 * WHAT IT DOES:
 * 1. Sends resume + JD to backend /api/analyze endpoint
 * 2. Backend extracts text from files
 * 3. Runs LangGraph workflow (Extract → Store → RAG → Score)
 * 4. Returns ATS score with breakdown and suggestions
 */
export async function analyzeResume(resumeFile, jdFile = null, jdText = null) {
    try {
        // Create FormData to send files
        const formData = new FormData();
        formData.append('resume', resumeFile);

        // Add JD if provided (either as file or text)
        if (jdFile) {
            formData.append('jd', jdFile);
        } else if (jdText) {
            formData.append('jd_text', jdText);
        }

        console.log('📤 Sending resume to backend for analysis...');

        // Send to backend
        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed');
        }

        const data = await response.json();
        console.log('✅ Analysis complete:', data);

        return data;

    } catch (error) {
        console.error('❌ Error analyzing resume:', error);
        throw error;
    }
}

/**
 * Extract information from resume without scoring
 * 
 * @param {File} resumeFile - Resume file
 * @returns {Promise<Object>} Extracted resume information
 * 
 * WHAT IT DOES:
 * - Useful for previewing what data was extracted before providing a JD
 * - Returns: name, email, skills, experience, education
 */
export async function extractResumeInfo(resumeFile) {
    try {
        const formData = new FormData();
        formData.append('resume', resumeFile);

        console.log('📤 Extracting resume information...');

        const response = await fetch(`${API_BASE_URL}/api/extract`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Extraction failed');
        }

        const data = await response.json();
        console.log('✅ Extraction complete:', data);

        return data;

    } catch (error) {
        console.error('❌ Error extracting resume:', error);
        throw error;
    }
}

/**
 * Check backend health status
 * 
 * @returns {Promise<Object>} Health check data
 * 
 * WHAT IT DOES:
 * - Verifies backend is running
 * - Checks Pinecone and Groq connections
 * - Returns service status
 */
export async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);

        if (!response.ok) {
            throw new Error('Health check failed');
        }

        return await response.json();

    } catch (error) {
        console.error('❌ Backend health check failed:', error);
        throw error;
    }
}

/**
 * Get Pinecone statistics
 * 
 * @returns {Promise<Object>} Pinecone index stats
 */
export async function getPineconeStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/stats`);

        if (!response.ok) {
            throw new Error('Failed to get stats');
        }

        return await response.json();

    } catch (error) {
        console.error('❌ Error getting stats:', error);
        throw error;
    }
}

/**
 * Helper function to validate file type
 * 
 * @param {File} file - File to validate
 * @returns {boolean} True if valid
 */
export function isValidResumeFile(file) {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const validExtensions = ['.pdf', '.docx'];

    const fileName = file.name.toLowerCase();
    const hasValidExtension = validExtensions.some(ext => fileName.endsWith(ext));
    const hasValidType = validTypes.includes(file.type);

    return hasValidExtension || hasValidType;
}

/**
 * Helper function to validate file size
 * 
 * @param {File} file - File to validate
 * @param {number} maxSizeMB - Maximum size in MB (default 5)
 * @returns {boolean} True if valid
 */
export function isValidFileSize(file, maxSizeMB = 5) {
    const maxSizeBytes = maxSizeMB * 1024 * 1024;
    return file.size <= maxSizeBytes;
}

export default {
    analyzeResume,
    extractResumeInfo,
    checkHealth,
    getPineconeStats,
    isValidResumeFile,
    isValidFileSize,
};
