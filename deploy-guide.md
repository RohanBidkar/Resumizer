# 🚀 Deployment Guide: Resumizer on Render (Free Tier)
This guide will help you deploy the **Resumizer** app as a single web service on Render's free tier. The Frontend (React) will be served by the Backend (FastAPI).

## 1. Prerequisites
- A GitHub account with this project pushed to a repository.
- A [Render](https://render.com) account.
- Your API Keys (`GROQ_API_KEY`, `PINECONE_API_KEY`).

## 2. Project Setup (Already Done ✅)
I have configured the project for you:
1.  **Frontend**: Configured `api.js` to use relative paths in production.
2.  **Backend**: Configured `main.py` to serve the React build static files.
3.  **Config**: Added `render.yaml` to the project root.

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

### Option B: Manual Setup
If you prefer to configure it manually without `render.yaml`:
1.  Create a **New Web Service**.
2.  Connect your repo.
3.  **Name**: `resumizer`
4.  **Runtime**: `Python 3`
5.  **Build Command**: 
    ```bash
    cd frontend && npm install && npm run build && cd ../backend && pip install -r requirements.txt
    ```
6.  **Start Command**:
    ```bash
    cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    ```
7.  **Environment Variables**:
    *   Add `GROQ_API_KEY`, `PINECONE_API_KEY`, etc.
8.  Click **Create Web Service**.

## 4. Verification
Once deployed, Render will verify the service is "Live".
Visit the URL (e.g., `https://resumizer.onrender.com`).
*   The **Landing Page** should load.
*   The **Analysis** should work (files upload to backend).

## Troubleshooting
*   **Build Failures**: Check the logs. If `npm install` fails, make sure the `cd frontend` part is correct.
*   **404 on Refresh**: I added a catch-all route in `main.py`, so refreshing on `/results` should work fine.
