from flask import Blueprint, request, jsonify
from io import BytesIO
import zipfile
from app.services.pdf_service import extract_text_from_pdf
from app.services.llm_service import hr_analyze, candidate_find_jobs

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route("/analyze", methods=["POST"])
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

@api_bp.route("/find_jobs", methods=["POST"])
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
