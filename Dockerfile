# Step 1: Build the React Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/client
COPY client/package*.json ./
RUN npm install
COPY client/ ./
RUN npm run build

# Step 2: Build the Python Backend
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies if any are needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy python dependencies and install
COPY server/requirements.txt ./server/
RUN pip install --no-cache-dir -r server/requirements.txt

# Copy backend files and built frontend
COPY server/ ./server/
COPY --from=frontend-builder /app/client/dist ./client/dist

# Expose port (Render will override this, but good practice)
EXPOSE 3000

# Run gunicorn, binding to the PORT environment variable provided by Render, using 1 worker and 2 threads to conserve memory
CMD sh -c "gunicorn --chdir server app:app -b 0.0.0.0:\$PORT --workers 1 --threads 2"
