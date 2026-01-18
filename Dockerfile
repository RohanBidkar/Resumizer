# Build Stage for Frontend
FROM node:18-alpine as frontend-build

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build

# Runtime Stage for Backend
FROM python:3.10-slim

WORKDIR /app/backend

# Install system dependencies if needed (e.g. for some python packages)
# RUN apt-get update && apt-get install -y --no-install-recommends ...

# Copy backend requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Preload models
RUN python preload_model.py

# Copy frontend build artifacts from previous stage
# This assumes backend/main.py expects frontend files at ../frontend/dist
# So we create that structure in the container
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
