from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import json

# Load JSON file
with open("layout.json", "r") as f:
    json_data = json.load(f)

# Create PDF document
pdf = SimpleDocTemplate("json2pdf.pdf", pagesize=letter)
styles = getSampleStyleSheet()
elements = []

# Process JSON elements
for item in json_data["elements"]:
    if item["type"] == "title":
        elements.append(Paragraph(f"<b>{item['content']}</b>", styles["Title"]))
    elif item["type"] == "para":
        elements.append(Paragraph(item["content"], styles["Normal"]))
    elif item["type"] == "table":
        table = Table(item["data"])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)

# Build PDF
pdf.build(elements)
print("PDF created successfully!")
