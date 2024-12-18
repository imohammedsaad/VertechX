from fpdf import FPDF

def generate_pdf(title, content, pdf_output_path="output.pdf"):
    """
    Generate a PDF from the provided content.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)

    pdf.multi_cell(0, 10, content)  # multi_cell for wrapping text
    pdf.output(pdf_output_path)

    return pdf_output_path
