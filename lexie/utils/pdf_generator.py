# === FILE: utils/pdf_generator.py ===
from fpdf import FPDF

def generate_pdf_report(user_id, interactions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Lexie Report for {user_id}", ln=1)
    for i, pair in enumerate(interactions):
        pdf.multi_cell(0, 10, f"Q{i+1}: {pair['user']}\nA{i+1}: {pair['bot']}")
    path = f"reports/{user_id}_report.pdf"
    pdf.output(path)
    return path
