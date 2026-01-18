from pypdf import PdfReader
from docx import Document
from io import BytesIO

def parse_pdf(file_bytes: bytes) -> str:
    text = ""
    reader = PdfReader(BytesIO(file_bytes))
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def parse_docx(file_bytes: bytes) -> str:
    doc = Document(BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file_bytes: bytes, filename: str) -> str:
    name = filename.lower()
    if name.endswith(".pdf"):
        return parse_pdf(file_bytes)
    elif name.endswith(".docx"):
        return parse_docx(file_bytes)
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")
