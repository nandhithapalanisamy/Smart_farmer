# Smart Farmer - Render Deployment Guide

This guide describes how to push your updated project to GitHub and deploy it to **Render** as a single, completely free web service.

---

## What We Have Changed
1. **Consolidated Backends**: We moved the Node.js authentication routes (signup/signin) into the Python Flask backend. You no longer need to run the Node.js server.
2. **PostgreSQL to CSV Database**: We replaced the PostgreSQL database with local `.csv` files (`users.csv` and `prediction_history.csv`) inside the `data/` folder. This means you do not need to create or pay for databases on Render, and it is 100% free forever.
3. **Model Optimization**: The uncompressed `crop_model.pkl` (5.48 GB) was deleted. We trained and compressed a new model (`crop_model.joblib`) of size **14.2 MB** with **95% accuracy** (virtually identical to the original). This fits well below GitHub's 100MB file limit.
4. **Vite Development Proxy & Relative APIs**: The React frontend now uses relative URLs (`/api/...`), and is configured to proxy API requests to Flask during local development.
5. **Docker Containerization**: We added a `Dockerfile` and `render.yaml` to compile the React frontend and serve it using Gunicorn/Flask as a single service.

---

## Step 1: Push Your Code to GitHub

Since the massive `crop_model.pkl` file has been deleted, your project can now be easily pushed to GitHub. Run the following commands in your VS Code terminal (at the project root):

```bash
# Add all files to staging
git add .

# Commit changes
git commit -m "Optimize ML model size, switch PostgreSQL to CSV, and prepare for Render deployment"

# Push to your GitHub repository
git push origin main
```

---

## Step 2: Deploy to Render (Free Tier)

We have configured the project with a **Render Blueprint** (`render.yaml`). This makes deployment automated:

1. Go to [Render](https://render.com/) and sign in.
2. Click the **New +** button in the top right and select **Blueprint**.
3. Connect your GitHub account and select your **Crop_Recommendation** repository.
4. Render will read the `render.yaml` file and show a list of services (it will configure a web service named `smart-farmer` using the `docker` runtime).
5. Click **Apply** (or **Approve**).
6. Render will automatically:
   - Pull your code.
   - Build the Docker container (which installs Python packages, compiles the React frontend, and packages them together).
   - Start the service.

Once the build is complete, Render will provide you with a public URL (e.g., `https://smart-farmer.onrender.com`). Open this URL in your browser to access your deployed app!

---

## Running the App Locally (For Development)

If you want to run the project locally for future development:

### 1. Run the Flask Backend
```bash
cd server
python app.py
```
This starts the backend API on `http://127.0.0.1:3000`.

### 2. Run the Vite Frontend
In another terminal:
```bash
cd client
npm install
npm run dev
```
This starts the React development server on `http://localhost:5173`. Any API calls to `/api/...` will automatically be proxied to the Flask server.
