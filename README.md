# AI Resume Analyzer

A Flask-based web application that uses Google Gemini AI to analyze resumes against job descriptions. Supports two modes:
- **HR Mode**: Compare multiple candidate resumes against a single job description
- **Candidate Mode**: Find the best job matches for a single resume

## Features
- PDF and text file support for resumes and job descriptions
- ZIP file upload for batch processing
- AI-powered analysis using Google Gemini 1.5 Flash
- Clean, responsive UI with Tailwind CSS
- JSON API endpoints for programmatic access

## Local Setup

1. **Clone and install dependencies**
   ```bash
   git clone https://github.com/ritviksharma54/ucs503p-202526odd-helinox.git
   cd ucs503p-202526odd-helinox
   python -m venv .venv
   source .venv/Scripts/activate  # Windows Git Bash
   # or: .venv\Scripts\activate    # Windows CMD
   # or: .\.venv\Scripts\Activate.ps1  # PowerShell
   pip install -r requirements.txt
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key:
   # GOOGLE_API_KEY=your_actual_key_here
   ```

3. **Run the app**
   ```bash
   python app.py
   # Visit http://localhost:5000
   ```

## Deploy to Render.com

1. **Push code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Create a new Web Service on Render**
   - Go to [render.com](https://render.com) and sign up/login
   - Click **New +** → **Web Service**
   - Connect your GitHub account and select this repository
   - Configure:
     - **Name**: `ai-resume-analyzer` (or your choice)
     - **Region**: Choose closest to you
     - **Branch**: `main`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Instance Type**: Free

3. **Set environment variable**
   - In Render dashboard → Environment
   - Add: `GOOGLE_API_KEY` = your Google Gemini API key

4. **Deploy**
   - Click **Create Web Service**
   - Render will auto-deploy and give you a URL like `https://ai-resume-analyzer.onrender.com`

## API Endpoints

- `GET /` - Web UI
- `GET /health` - Health check
- `POST /analyze` - HR mode: analyze candidates against JD
- `POST /find_jobs` - Candidate mode: find matching jobs
- `POST /analyze_v2?mode=hr|candidate` - Unified endpoint

## Tech Stack
- **Backend**: Flask, Python 3.10+
- **AI**: Google Gemini 1.5 Flash (via LangChain)
- **PDF Processing**: pypdf
- **Frontend**: Vanilla JS + Tailwind CSS (CDN)
- **Deployment**: Render.com 
