import PyPDF2

def extract_text_from_pdf(uploaded_file):
    """
    User jo PDF report upload karega, ye function uska text nikalega.
    """
    text = ""
    try:
        # Read the uploaded PDF file
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading report: {e}"