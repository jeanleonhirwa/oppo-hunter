import fitz  # PyMuPDF
import io
from gemini_client import extract_resume_info

async def parse_resume(file_bytes: bytes, filename: str) -> dict:
    text = ""
    
    if filename.endswith(".pdf"):
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            for page in doc:
                text += page.get_text()
        except Exception as e:
            text = f"Error parsing PDF: {e}"
    elif filename.endswith(".docx"):
        try:
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            text = "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            text = f"Error parsing DOCX: {e}"
    else:
        text = file_bytes.decode("utf-8", errors="ignore")
    
    # Extract structured info using Gemini
    info = await extract_resume_info(text)
    info["text"] = text
    return info
