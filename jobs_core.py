# jobs_core.py
import json
from typing import List, Tuple
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pypdf import PdfReader


PROMPT_TEMPLATE = """
You are a career advisor. Given ONE candidate resume and a SET of Job Descriptions (JDs),
identify which roles best fit the candidate. Return STRICT JSON ONLY.

1) Resume Understanding:
   - Summarize candidate's core profile: education, years of experience, primary skills, recent roles.

2) For Each JD:
   - Extract required qualifications, must-haves vs. nice-to-haves.
   - Compare the resume to the JD: matches, gaps, risk flags (if any).
   - Assign a suitability score 0–10 (number).

3) Ranking:
   - Rank all JDs by the candidate's fit (descending).
   - Give a short justification for each rank.

4) Final Output (JSON only):
{
  "Candidate Summary": "...",
  "Jobs": [
    {
      "Job Id": "...",
      "Job Title": "...",
      "Company": "...",
      "JD Summary": "...",
      "Matches": ["..."],
      "Gaps": ["..."],
      "Suitability Score": 0
    }
  ],
  "Ranking": [
    {"Rank": 1, "Job Id": "...", "Job Title": "...", "Company": "...", "Justification": "..."}
  ],
  "Top Recommendations": [
    {"Job Id": "...", "Why": "...", "How to Improve": ["..."]}
  ]
}

---
DATA
---

*RESUME (single):*
{resume_text}

---

*JOB DESCRIPTIONS (multiple):*
{jobs_block}
"""


def extract_text_from_pdf(file_obj) -> str:
    reader = PdfReader(file_obj)
    pages_text = []
    for p in reader.pages:
        pages_text.append(p.extract_text() or "")
    return "\n".join(pages_text).strip()


def build_jobs_block(items: List[Tuple[str, str]]) -> str:
    """
    items = [(job_id_or_filename, jd_text)]
    Formats multiple JDs in a consistent, parseable block.
    """
    parts = []
    for name, text in items:
        parts.append(f"--- JD: {name} ---\n{text}\n")
    return "\n".join(parts)


def run_llm_for_jobs(resume_text: str, jobs_block: str) -> dict:
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        response_mime_type="application/json",
    )
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["resume_text", "jobs_block"]
    )
    chain = prompt | llm
    result = chain.invoke({
        "resume_text": resume_text,
        "jobs_block": jobs_block
    })
    return json.loads(result.content)


def analyze_jobs(resume_text: str, job_named_texts: List[Tuple[str, str]]) -> dict:
    """
    Candidate flow:
      - resume_text: single candidate resume (string)
      - job_named_texts: list of (job_id_or_filename, jd_text)
    """
    if not resume_text.strip():
        raise ValueError("Resume text is empty.")
    if not job_named_texts:
        raise ValueError("No job descriptions provided.")
    jobs_block = build_jobs_block(job_named_texts)
    return run_llm_for_jobs(resume_text, jobs_block)