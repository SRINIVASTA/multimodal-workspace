import io
import pandas as pd
from pypdf import PdfReader
try:
    import docx
except ImportError:
    docx = None

def extract_text_from_file(uploaded_file) -> str:
    """Extracts raw text strings from PDF, DOCX, CSV, and TXT matrices."""
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    if file_type == "txt":
        return uploaded_file.read().decode("utf-8")
        
    elif file_type == "pdf":
        pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
        text_content = []
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_content.append(page_text)
        return "\n".join(text_content)
        
    elif file_type == "docx":
        if docx is None:
            return "Error: python-docx library is not installed."
        doc = docx.Document(io.BytesIO(uploaded_file.read()))
        return "\n".join([para.text for para in doc.paragraphs])
        
    elif file_type in ["csv", "xlsx"]:
        try:
            df = pd.read_csv(uploaded_file) if file_type == "csv" else pd.read_excel(uploaded_file)
            return df.to_string()
        except Exception as e:
            return f"Error parsing structured sheet structure: {str(e)}"
            
    return "Unsupported file context structure."
