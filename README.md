# AI Resume Analyzer

A modern AI-powered resume analysis tool that helps candidates find matching jobs and recruiters identify top talent using Google Gemini AI.

## Features

- **Candidate Mode**: Upload your resume and find the best matching job descriptions
- **HR Mode**: Upload a job description and rank multiple candidate resumes
- **AI-Powered Analysis**: Uses Google Gemini 2.5 Flash for intelligent matching
- **Multiple Upload Options**: Support for PDF, TXT, and ZIP files
- **Modern UI**: Built with Vue.js 3 and Tailwind CSS with dark mode
- **Detailed Insights**: Get suitability scores, key matches, and skill gaps

## Tech Stack

**Backend:**
- Flask (Python 3.10+)
- Google Gemini 2.5 Flash (via LangChain)
- pypdf for PDF processing
- Flask-CORS for API handling

**Frontend:**
- Vue.js 3 with Vite
- Vue Router for navigation
- Tailwind CSS for styling
- Axios for API calls

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ritviksharma54/ucs503p-202526odd-helinox.git
cd ucs503p-202526odd-helinox
```

### 2. Backend Setup

**Create and activate virtual environment:**
```bash
python -m venv .venv

# Windows CMD:
.venv\Scripts\activate
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Configure environment:**
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env and add your Google Gemini API key:
GOOGLE_API_KEY=your_actual_api_key_here
PORT=5000
```

Get your API key from: [Google AI Studio](https://makersuite.google.com/app/apikey)

**Run the backend:**
```bash
python app.py
```
Backend will run on `http://localhost:5000`

### 3. Frontend Setup

**Navigate to frontend directory:**
```bash
cd frontend
```

**Install dependencies:**
```bash
npm install
```

**Run development server:**
```bash
npm run dev
```
Frontend will run on `http://localhost:5173`

**Build for production:**
```bash
npm run build
```

## Project Structure

```
├── app/                    # Backend Flask application
│   ├── __init__.py        # App factory
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic (PDF, LLM)
│   └── utils/             # Helper functions
├── frontend/              # Vue.js frontend
│   ├── src/
│   │   ├── components/   # Reusable components
│   │   ├── views/        # Page components
│   │   ├── router/       # Vue Router config
│   │   └── assets/       # Styles and images
│   └── public/
├── .env.example          # Environment template
├── requirements.txt      # Python dependencies
└── README.md
```

## Usage

1. **For Candidates:**
   - Navigate to "For Candidates"
   - Paste your resume text or upload a PDF
   - Upload job descriptions (PDF/TXT files or ZIP)
   - Click "Find Matches" to see ranked job opportunities

2. **For Recruiters:**
   - Navigate to "For Recruiters"
   - Upload a job description (PDF/TXT)
   - Upload candidate resumes (PDF files or ZIP)
   - Click "Rank Candidates" to see ranked candidates with scores

## API Endpoints

- `POST /api/find_jobs` - Candidate mode: Find matching jobs for a resume
- `POST /api/analyze` - HR mode: Rank candidates for a job description

## Deployment

The backend can be deployed using Gunicorn:
```bash
gunicorn -c gunicorn_config.py app:app
```

Frontend build can be served via any static hosting service (Netlify, Vercel, etc.)

## License

MIT License - See LICENSE file for details

## Contributors

- Ritvik Sharma - [GitHub](https://github.com/ritviksharma54)
