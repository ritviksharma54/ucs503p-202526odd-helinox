from pypdf import PdfReader

def extract_text_from_pdf(file_like) -> str:
    reader = PdfReader(file_like)
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts).strip()
