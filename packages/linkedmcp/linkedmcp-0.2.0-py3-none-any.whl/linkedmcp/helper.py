import io
from fpdf import FPDF

def generate_pdf_from_text(text: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in text.splitlines():
        pdf.multi_cell(0, 10, line)
    output = io.BytesIO()
    pdf.output(output)
    return output.getvalue()
