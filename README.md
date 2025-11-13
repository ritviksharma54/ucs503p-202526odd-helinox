# AI Resume Analyzer

**Live Demo**: [https://ai-resume-analyzer-s5nk.onrender.com/](https://ai-resume-analyzer-s5nk.onrender.com/)

A Flask-based web application that uses Google Gemini AI to analyze resumes against job descriptions. Supports two modes:
- **Candidate Mode**: Find the best job matches for your resume
- **HR Mode**: Compare multiple candidate resumes against a job description

## Features
- PDF and text file support for resumes and job descriptions
- ZIP file upload for batch processing of multiple documents
- AI-powered analysis using Google Gemini 2.5 Flash
- Clean, responsive UI with Tailwind CSS
- Detailed scoring and recommendations

## How to Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/ritviksharma54/ucs503p-202526odd-helinox.git
   cd ucs503p-202526odd-helinox
   ```

2. **Create virtual environment and install dependencies**
   ```bash
   python -m venv .venv
   
   # Activate virtual environment:
   # Windows CMD:
   .venv\Scripts\activate
   # Windows PowerShell:
   .\.venv\Scripts\Activate.ps1
   # Git Bash:
   source .venv/Scripts/activate
   
   pip install -r requirements.txt
   ```

3. **Set up Google API key**
   - Create a `.env` file in the project root
   - Add your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```
   - Get your API key from: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

4. **Run the application**
   ```bash
   python app.py
   ```
   - Open your browser and visit: [http://localhost:5000](http://localhost:5000)

## Tech Stack
- **Backend**: Flask, Python 3.10+
- **AI Model**: Google Gemini 2.5 Flash (via LangChain)
- **PDF Processing**: pypdf
- **Frontend**: Vanilla JavaScript + Tailwind CSS
- **Deployment**: Render.com with Gunicorn 
