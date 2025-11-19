import os
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from app.utils.parser import parse_model_json

def ensure_api_key():
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("Missing GOOGLE_API_KEY in .env")

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

def build_resumes_block(named_texts):
    return "\n".join([f"--- RESUME: {fname} ---\n{text}\n" for fname, text in named_texts])

def build_jobs_block(named_texts):
    return "\n".join([f"--- JD: {name} ---\n{text}\n" for name, text in named_texts])

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
