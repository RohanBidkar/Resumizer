# 🚀 Deployment Guide: Resumizer on Render (Docker)

This guide will help you deploy the **Resumizer** app as a single web service on Render using Docker. This method ensures a consistent environment for both the Node.js frontend and Python backend.

## 1. Prerequisites
- A GitHub account with this project pushed to a repository.
- A [Render](https://render.com) account.
- Your API Keys (`GROQ_API_KEY`, `PINECONE_API_KEY`).

## 2. Project Setup (Already Done ✅)
I have configured the project for you:
1.  **Dockerfile**: Created a multi-stage `Dockerfile` to handle building the frontend (Node.js) and setting up the backend (Python).
2.  **Render Config**: Updated `render.yaml` to specify the Docker environment.

## 3. Deployment Steps

### Option A: Blueprints (Recommended)
1.  Log in to the [Render Dashboard](https://dashboard.render.com/).
2.  Click **New +** and select **Blueprint**.
3.  Connect your GitHub repository.
4.  Render will detect the `render.yaml` file.
5.  Click **Apply**.
6.  You will be prompted to enter your Environment Variables:
    *   `GROQ_API_KEY`: Paste your key.
    *   `PINECONE_API_KEY`: Paste your key.
    *   `PINECONE_INDEX_NAME`: `resume-rag` (default)
7.  Click **Deploy**.

### Option B: Manual Setup (If not using Blueprint)
1.  Create a **New Web Service**.
2.  Connect your repo.
3.  **Name**: `resumizer`
4.  **Runtime**: `Docker` (Important!)
5.  **Environment Variables**:
    *   Add `GROQ_API_KEY`, `PINECONE_API_KEY`, etc.
6.  Click **Create Web Service**.

## 4. Verification
Once deployed, Render will verify the service is "Live".
Visit the URL (e.g., `https://resumizer.onrender.com`).
*   The **Landing Page** should load.
*   The **Analysis** should work (files upload to backend).

## Troubleshooting
*   **Build Failures**: Check the logs in the Render dashboard. The Docker build process steps will be visible there.
*   **Runtime Errors**: Check the "Logs" tab for any Python exceptions or missing environment variables.
