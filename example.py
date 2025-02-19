from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle

# Create a sample PDF document
doc = SimpleDocTemplate("example.pdf", pagesize=(4768, 6741))
elements = []
elements.append(Paragraph("""""",
                          style=ParagraphStyle(name="para", fontName="Helvetica", fontSize=12)))
doc.build(elements)
