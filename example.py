from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.flowables import DocAssign, DocExec, DocPara, DocIf, DocWhile

# Create a sample PDF document
doc = SimpleDocTemplate("example.pdf")
styles = getSampleStyleSheet()
normal = styles["Normal"]

Spacing = Spacer(1, 5)

# List of flowables (dynamic elements)
elements = [
    # Assign initial value to i
    DocAssign("i", 100),

    # Loop while i > 0
    DocWhile("i", [
        # Print current value of i
        DocPara("i", format="The value of i is %(__expr__)d", style=normal), Spacing,

        # Conditional check using DocIf
        DocIf("i > 50",
              Paragraph("The value of i is larger than 50", normal),
              Paragraph("The value of i is not larger than 50", normal)), Spacing,

        # Decrement i
        DocExec("i -= 1"),
    ])
]

# Build the PDF
doc.build(elements)
