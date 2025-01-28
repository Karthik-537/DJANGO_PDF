from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf():
    doc = SimpleDocTemplate("custom_line_with_paragraph.pdf", pagesize=letter)

    # Get the page dimensions
    page_width, page_height = letter

    # Define the width of the line (48 units less than the full page width)
    line_width = page_width - 48

    # Get the stylesheet
    styles = getSampleStyleSheet()

    # Create a Paragraph with an <hr> to simulate a line
    # The line width is dynamically controlled by the width variable
    line_paragraph = Paragraph(f'<hr width="{line_width}"/>', style=styles["Normal"])

    # Create flowables (elements to add to the document)
    flowables = []

    # Add the line and some space below it
    flowables.append(line_paragraph)
    flowables.append(Spacer(1, 15))  # Spacer to create space after the line

    # Build the document
    doc.build(flowables)


generate_pdf()
