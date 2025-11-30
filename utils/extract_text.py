import PyPDF2
import pdfplumber
from docx import Document
from PIL import Image
import pytesseract
import io
import shutil

tesseract_path = shutil.which("tesseract")
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

def extract_pdf_textlayer(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages[:5]:
            if page.extract_text():
                text += page.extract_text()
        return text
    except:
        return ""

def extract_pdf_ocr(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages[:3]:
            img = page.to_image(resolution=250).original
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            text += pytesseract.image_to_string(Image.open(buf))
    return text

def extract_pdf(file):
    text = extract_pdf_textlayer(file)
    if text.strip():
        return text
    file.seek(0)
    return extract_pdf_ocr(file)

def extract_docx(file):
    doc = Document(file)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text(upload_file):
    filename = upload_file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_pdf(upload_file.file)

    if filename.endswith(".docx"):
        return extract_docx(upload_file.file)

    return upload_file.file.read().decode("utf-8", errors="ignore")

