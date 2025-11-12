import os
import json
import re
import json5
import zipfile
from io import BytesIO

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask import render_template
from pypdf import PdfReader
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# =========================
# Setup
# =========================
load_dotenv()
app = Flask(__name__)

# =========================
# Utilities
# =========================
def extract_text_from_pdf(file_like) -> str:
    reader = PdfReader(file_like)
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts).strip()

def ensure_api_key():
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("Missing GOOGLE_API_KEY in .env")



import json, re, json5

def parse_model_json(result):
    """
    Robustly parse JSON from LLM output:
      - Accept dicts directly
      - Strip ```json ... ``` or ``` ... ``` fences if present
      - Extract the first full {...} object via brace counting
      - Try json.loads -> json5.loads -> cleaned json.loads
    Raises ValueError with a short raw excerpt if all attempts fail.
    """
    raw = getattr(result, "content", result)

    if isinstance(raw, dict):
        return raw
    if not isinstance(raw, str):
        raise ValueError(f"Model returned non-string content: {type(raw)}")

    text = raw.strip()
    if not text:
        raise ValueError("Model returned empty content.")

    # 1) Remove markdown code fences if present
    fenced = _extract_fenced_block(text)
    if fenced is not None:
        text = fenced.strip()

    # 2) Extract first full JSON object by brace counting
    obj = _extract_first_json_object(text)
    candidates = [c for c in [obj, text] if c]  # try object, then whole text

    # 3) Try strict JSON then JSON5 then quick-fix+strict
    for cand in candidates:
        cand = cand.strip()
        for parser in (_strict_json, _json5_json, _clean_then_strict):
            parsed = parser(cand)
            if parsed is not None:
                return parsed

    raise ValueError(f"Could not parse JSON from model. Raw (truncated):\n{text[:1500]}")

def _extract_fenced_block(s: str) -> str | None:
    """
    If the text contains ```json ... ``` or ``` ... ```, return the inner block.
    Otherwise None.
    """
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", s, flags=re.IGNORECASE)
    return fence.group(1) if fence else None

def _extract_first_json_object(s: str) -> str | None:
    """
    Extract the first complete {...} JSON object using brace counting.
    Handles braces inside strings in a minimal way.
    """
    in_str = False
    esc = False
    start = None
    depth = 0
    for i, ch in enumerate(s):
        if ch == '"' and not esc:
            in_str = not in_str
        esc = (ch == '\\' and not esc) if in_str else False
        if in_str:
            continue
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    return s[start:i+1]
    return None

def _strict_json(s: str):
    try:
        return json.loads(s)
    except Exception:
        return None

def _json5_json(s: str):
    try:
        return json5.loads(s)
    except Exception:
        return None

def _clean_then_strict(s: str):
    # Strip backticks and BOM, remove trailing commas before } or ]
    cleaned = s.strip().strip('`').replace("\ufeff", "")
    cleaned = re.sub(r",(\s*[}\]])", r"\1", cleaned)
    try:
        return json.loads(cleaned)
    except Exception:
        return None





# =========================
# HR FLOW
# =========================
HR_PROMPT = """
You are an expert HR recruiter. Your task is to evaluate and compare multiple resumes against a given Job Description (JD).
Output a SINGLE strict JSON object (no markdown, no code fences, no comments, no trailing commas).
Return STRICT JSON ONLY with no markdown, no commentary, no explanations. 
If a field is unknown, use an empty string or [].

Final Output (JSON only):
{{
  "Job Description Summary": "...",
  "Candidates": [
    {{
      "Candidate Name": "...",
      "Education": "...",
      "Years of Experience": "...",
      "Key Skills": ["..."],
      "Recent Job Titles": ["..."],
      "Reasoning": "...",
      "Suitability Score": 0
    }}
  ],
  "Ranking": [
    {{"Rank": 1, "Candidate Name": "Candidate A", "Justification": "..."}},
    {{"Rank": 2, "Candidate Name": "Candidate B", "Justification": "..."}}
  ]
}}

---
DATA
---

*JOB DESCRIPTION:*
{job_description}

---

*RESUMES:*
{resumes_block}
""".strip()

def build_resumes_block(named_texts):
    return "\n".join([f"--- RESUME: {fname} ---\n{text}\n" for fname, text in named_texts])

def hr_analyze(job_description_text: str, resume_named_texts):
    ensure_api_key()
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        response_mime_type="application/json",
    )
    prompt = PromptTemplate(template=HR_PROMPT, input_variables=["job_description", "resumes_block"])
    chain = prompt | llm
    result = chain.invoke({
        "job_description": job_description_text,
        "resumes_block": build_resumes_block(resume_named_texts)
    })
    return parse_model_json(result)

# =========================
# CANDIDATE FLOW
# =========================
CANDIDATE_PROMPT = """
You are a career advisor. Given ONE candidate resume and a SET of Job Descriptions (JDs),
Output a SINGLE strict JSON object (no markdown, no code fences, no comments, no trailing commas).
identify which roles best fit the candidate. Return STRICT JSON ONLY with no markdown, no commentary. 
If a field is unknown, use an empty string or [].

Final Output (JSON only):
{{
  "Candidate Summary": "...",
  "Jobs": [
    {{
      "Job Id": "...",
      "Job Title": "...",
      "Company": "...",
      "JD Summary": "...",
      "Matches": ["..."],
      "Gaps": ["..."],
      "Suitability Score": 0
    }}
  ],
  "Ranking": [
    {{"Rank": 1, "Job Id": "...", "Job Title": "...", "Company": "...", "Justification": "..."}}
  ],
  "Top Recommendations": [
    {{"Job Id": "...", "Why": "...", "How to Improve": ["..."]}}
  ]
}}

---
DATA
---

*RESUME (single):
{resume_text}

---

*JOB DESCRIPTIONS (multiple):
{jobs_block}
""".strip()

def build_jobs_block(named_texts):
    return "\n".join([f"--- JD: {name} ---\n{text}\n" for name, text in named_texts])

def candidate_find_jobs(resume_text: str, job_named_texts):
    ensure_api_key()
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        response_mime_type="application/json",
    )
    prompt = PromptTemplate(template=CANDIDATE_PROMPT, input_variables=["resume_text", "jobs_block"])
    chain = prompt | llm
    result = chain.invoke({
        "resume_text": resume_text,
        "jobs_block": build_jobs_block(job_named_texts),
    })
    return parse_model_json(result)

# =========================
# ROUTES
# =========================
from flask import render_template_string

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/hr", methods=["GET"])
def hr_page():
    html = """
    <h1>HR – Analyze Candidates</h1>
    <form method="POST" action="/analyze" enctype="multipart/form-data">
      <p><b>Upload JD file (TXT preferred, PDF supported):</b><br>
         <input type="file" name="jd_file" required></p>
      <p><b>Upload resumes (PDF, multiple) OR a ZIP of PDFs:</b><br>
         <input type="file" name="resumes" multiple>
         <br>or<br>
         <input type="file" name="resume_zip"></p>
      <p><button type="submit">Analyze</button></p>
    </form>
    """
    return render_template_string(html), 200

@app.route("/candidate", methods=["GET"])
def candidate_page():
    html = """
    <h1>Candidate – Find Best Jobs</h1>
    <form method="POST" action="/find_jobs" enctype="multipart/form-data">
      <p><b>Resume (paste text):</b><br>
         <textarea name="resume_text" rows="6" cols="80"
           placeholder="Or upload a file below"></textarea></p>
      <p><b>Or upload resume (TXT/PDF):</b><br>
         <input type="file" name="resume_file"></p>
      <p><b>Upload JDs (TXT/PDF, multiple) OR a ZIP of JDs:</b><br>
         <input type="file" name="jd_files" multiple>
         <br>or<br>
         <input type="file" name="jd_zip"></p>
      <p><button type="submit">Find Jobs</button></p>
    </form>
    """
    return render_template_string(html), 200

@app.route("/analyze", methods=["POST"])
def analyze_endpoint():
    try:
        # JD
        jd_file = request.files.get("jd_file")
        jd_text = ""
        if jd_file:
            fname = jd_file.filename
            raw = jd_file.read()
            jd_text = extract_text_from_pdf(BytesIO(raw)) if fname.lower().endswith(".pdf") else raw.decode("utf-8", errors="ignore")
        else:
            jd_text = request.form.get("job_description", "")
        if not jd_text.strip():
            return jsonify({"error": "Provide jd_file (TXT/PDF) or job_description text"}), 400

        # Resumes
        resume_named_texts = []
        for f in request.files.getlist("resumes"):
            if f.filename.lower().endswith(".pdf"):
                text = extract_text_from_pdf(BytesIO(f.read()))
                if text.strip():
                    resume_named_texts.append((f.filename, text))
        resume_zip = request.files.get("resume_zip")
        if resume_zip:
            with zipfile.ZipFile(BytesIO(resume_zip.read())) as z:
                for fname in z.namelist():
                    if fname.lower().endswith(".pdf"):
                        text = extract_text_from_pdf(BytesIO(z.read(fname)))
                        if text.strip():
                            resume_named_texts.append((fname, text))
        if not resume_named_texts:
            return jsonify({"error": "No valid resumes provided"}), 400

        result = hr_analyze(jd_text, resume_named_texts)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "HR flow failed", "detail": str(e)}), 500

@app.route("/find_jobs", methods=["POST"])
def find_jobs_endpoint():
    try:
        # Resume
        resume_text = request.form.get("resume_text", "")
        resume_file = request.files.get("resume_file")
        if resume_file:
            fname = resume_file.filename
            raw = resume_file.read()
            resume_text = extract_text_from_pdf(BytesIO(raw)) if fname.lower().endswith(".pdf") else raw.decode("utf-8", errors="ignore")
        if not resume_text.strip():
            return jsonify({"error": "Provide resume_text or resume_file"}), 400

        # JDs
        job_named_texts = []
        for f in request.files.getlist("jd_files"):
            raw = f.read()
            text = extract_text_from_pdf(BytesIO(raw)) if f.filename.lower().endswith(".pdf") else raw.decode("utf-8", errors="ignore")
            if text.strip():
                job_named_texts.append((f.filename, text))
        jd_zip = request.files.get("jd_zip")
        if jd_zip:
            with zipfile.ZipFile(BytesIO(jd_zip.read())) as z:
                for fname in z.namelist():
                    if fname.lower().endswith((".pdf", ".txt")):
                        raw = z.read(fname)
                        text = extract_text_from_pdf(BytesIO(raw)) if fname.lower().endswith(".pdf") else raw.decode("utf-8", errors="ignore")
                        if text.strip():
                            job_named_texts.append((fname, text))
        if not job_named_texts:
            return jsonify({"error": "No valid job descriptions provided"}), 400

        result = candidate_find_jobs(resume_text, job_named_texts)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Candidate flow failed", "detail": str(e)}), 500

@app.route("/analyze_v2", methods=["POST"])
def analyze_v2():
    mode = (request.args.get("mode") or request.form.get("mode") or "").lower()
    if mode == "hr":
        return analyze_endpoint()
    elif mode == "candidate":
        return find_jobs_endpoint()
    return jsonify({"error": "Provide mode=hr or mode=candidate"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)