# Build Stage for Frontend
FROM node:18-alpine as frontend-build

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci --production

COPY frontend/ .
RUN npm run build

# Runtime Stage for Backend
FROM python:3.10-slim

WORKDIR /app/backend

# Install system dependencies if needed (e.g. for some python packages)
# RUN apt-get update && apt-get install -y --no-install-recommends ...

# Copy backend requirements first for better layer caching
COPY backend/requirements.txt .

# Install Python dependencies with optimization flags
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Preload sentence-transformers model to cache it in the Docker image
# This reduces cold start time since the model won't need to be downloaded
RUN python preload_model.py

# Copy frontend build artifacts from previous stage
# This assumes backend/main.py expects frontend files at ../frontend/dist
# So we create that structure in the container
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# Expose the port
EXPOSE 8000

# Use exec form for better signal handling and faster shutdown
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
