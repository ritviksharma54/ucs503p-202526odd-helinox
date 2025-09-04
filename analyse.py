import os
import json
from dotenv import load_dotenv
import PyPDF2

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

def run_analysis():
    
    load_dotenv()
    resumes_folder_path = "resumes"
    jd_file_path = "jd.txt"

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        temperature=0.2,
        response_mime_type="application/json",
    )

    prompt_template = """
    You are an expert HR recruiter. Your task is to evaluate and compare multiple resumes against a given Job Description (JD).
    Follow these steps carefully and provide the final output in a structured JSON format ONLY.

    1. **Understand the Job Description (JD)**:
       - Summarize the required qualifications, skills, and experience.
       - Identify must-have vs. nice-to-have requirements.

    2. **For Each Resume**:
       - Extract key details: Candidate Name, Education, Years of Experience, Key Skills, and Recent Job Titles.
       - Compare these against the JD.
       - Highlight matches and gaps.
       - Provide concise reasoning about the candidate's fit.
       - Assign a suitability score from 0 to 10.

    3. **Comparison & Ranking**:
       - Compare all candidates side by side.
       - Rank candidates in descending order of suitability, justifying the ranking.

    4. **Final Output (Structured JSON)**:
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

    **JOB DESCRIPTION:**
    {job_description}

    ---

    **RESUMES:**
    {resumes_text}
    """

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["job_description", "resumes_text"]
    )

    chain = PROMPT | llm

    try:
        with open(jd_file_path, 'r', encoding='utf-8') as f:
            job_description = f.read()

        combined_resume_text = ""
        print(f"Scanning for resumes in '{resumes_folder_path}' folder...")
        for filename in os.listdir(resumes_folder_path):
            if filename.endswith(".pdf"):
                file_path = os.path.join(resumes_folder_path, filename)
                try:
                    with open(file_path, "rb") as file:
                        reader = PyPDF2.PdfReader(file)
                        text = "".join(page.extract_text() or "" for page in reader.pages)
                        combined_resume_text += f"--- RESUME: {filename} ---\n{text}\n\n"
                        print(f"  - Parsed {filename}")
                except Exception as e:
                    print(f"  - Could not parse {filename}. Error: {e}")

        if not combined_resume_text:
            print("\nError: No PDF resumes found or parsed in the specified folder.")
            return

    except FileNotFoundError:
        print(f"\nError: The job description file '{jd_file_path}' or resumes folder '{resumes_folder_path}' was not found.")
        return
    except Exception as e:
        print(f"\nAn error occurred during file processing: {e}")
        return

    print("\nSending data to the model for analysis... 🧠")
    try:
        result = chain.invoke({
            "job_description": job_description,
            "resumes_text": combined_resume_text
        })
        
        result_json = json.loads(result.content)
        
        print("\n--- ANALYSIS COMPLETE ---")
        print(json.dumps(result_json, indent=2))

    except Exception as e:
        print(f"\nAn error occurred while running the analysis: {e}")


if __name__ == "__main__":
    run_analysis()