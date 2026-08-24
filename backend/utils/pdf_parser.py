import pdfplumber
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts raw text from a PDF file byte stream."""
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""
