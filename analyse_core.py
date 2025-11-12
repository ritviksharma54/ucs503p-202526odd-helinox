# analyse_core.py
import json
from typing import List, Tuple, Optional

from pypdf import PdfReader
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


PROMPT_TEMPLATE = """
You are an expert HR recruiter. Your task is to evaluate and compare multiple resumes against a given Job Description (JD).
Follow these steps carefully and provide the final output in a structured JSON format ONLY.

1. Understand the Job Description (JD):
   - Summarize the required qualifications, skills, and experience.
   - Identify must-have vs. nice-to-have requirements.

2. For Each Resume:
   - Extract key details: Candidate Name, Education, Years of Experience, Key Skills, and Recent Job Titles.
   - Compare these against the JD.
   - Highlight matches and gaps.
   - Provide concise reasoning about the candidate's fit.
   - Assign a suitability score from 0 to 10.

3. Comparison & Ranking:
   - Compare all candidates side by side.
   - Rank candidates in descending order of suitability, justifying the ranking.

4. Final Output (Structured JSON):
   Provide results in the following JSON structure. Ensure the 'Ranking' array contains objects with all three keys: 'Rank', 'Candidate Name', and 'Justification'.

   {{
     "Job Description Summary": "...",
     "Candidates": [
       {{
         "Candidate Name": "...",
         "Education": "...",
         "Years of Experience": "...",
         "Key Skills": [...],
         "Recent Job Titles": [...],
         "Reasoning": "...",
         "Suitability Score": "X/10"
       }}
     ],
     "Ranking": [
       {{"Rank": 1, "Candidate Name": "Candidate A", "Justification": "..."}},
       {{"Rank": 2, "Candidate Name": "Candidate B", "Justification": "..."}}
     ]
   }}

---
HERE IS THE DATA:
---

*JOB DESCRIPTION:*
{job_description}

---

*RESUMES:*
{resumes_text}
"""


def extract_text_from_pdf(file_obj) -> str:
    """
    Extracts text from a PDF file-like object using pypdf.
    """
    reader = PdfReader(file_obj)
    pages_text = []
    for page in reader.pages:
        pages_text.append(page.extract_text() or "")
    return "\n".join(pages_text).strip()


def build_combined_resume_block(named_texts: List[Tuple[str, str]]) -> str:
    """
    Format resumes as a single block the model can parse reliably.
    named_texts: list of (filename, text)
    """
    parts = []
    for fname, text in named_texts:
        parts.append(f"--- RESUME: {fname} ---\n{text}\n")
    return "\n".join(parts)


def run_llm(job_description: str, resumes_block: str) -> dict:
    """
    Calls Gemini via LangChain with a strict JSON-only response.
    Returns a Python dict (parsed JSON).
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        temperature=0.2,
        response_mime_type="application/json",
    )
    prompt = PromptTemplate(
        template=PROMPT_TEMPLATE,
        input_variables=["job_description", "resumes_text"],
    )
    chain = prompt | llm
    result = chain.invoke({
        "job_description": job_description,
        "resumes_text": resumes_block
    })

    # Parse JSON; raise if invalid so the API can handle it cleanly
    return json.loads(result.content)


def analyze(job_description_text: str, resume_named_texts: List[Tuple[str, str]]) -> dict:
    """
    Orchestrates the whole flow:
      - formats resumes
      - calls the LLM
      - returns the JSON result (as dict)
    """
    if not job_description_text.strip():
        raise ValueError("Job description is empty.")
    if not resume_named_texts:
        raise ValueError("No resumes provided.")

    resumes_block = build_combined_resume_block(resume_named_texts)
    return run_llm(job_description_text, resumes_block)          