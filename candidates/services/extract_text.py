import PyPDF2
import docx

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path , 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    
    return text


def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_text(file_path, file_type):
    if file_type == 'pdf':
        return extract_text_from_pdf(file_path=file_path)
    
    if file_type == 'docx':
        return extract_text_from_docx(file_path=file_path)
    
    else:
        return ""
