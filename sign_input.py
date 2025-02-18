from sign_block import SignBlock
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

regular_font_path = "pdf_letter_generator/fonts/Inter-4.1/extras/ttf/Inter-Regular.ttf"
medium_font_path = "pdf_letter_generator/fonts/Inter-4.1/extras/ttf/Inter-Medium.ttf"
bold_font_path = "pdf_letter_generator/fonts/Inter-4.1/extras/ttf/Inter-Bold.ttf"
italic_font_path = "pdf_letter_generator/fonts/Inter-4.1/extras/ttf/Inter-Italic.ttf"
bolditalic_font_path = "pdf_letter_generator/fonts/Inter-4.1/extras/ttf/Inter-BoldItalic.ttf"

# Register fonts
pdfmetrics.registerFont(TTFont("Inter", regular_font_path))
pdfmetrics.registerFont(TTFont("Inter-Medium", medium_font_path))
pdfmetrics.registerFont(TTFont("Inter-Bold", bold_font_path))
pdfmetrics.registerFont(TTFont("Inter-Italic", italic_font_path))
pdfmetrics.registerFont(TTFont("Inter-BoldItalic", bolditalic_font_path))

pdfmetrics.registerFontFamily(
    "Inter",
    normal="Inter",
    bold="Inter-Bold",
    italic="Inter-Italic",
    boldItalic="Inter-BoldItalic"
)

# Read your local PDF file
pdf_path = "pc_documents.pdf"  # Replace with your actual file path
if Path(pdf_path).exists():
    with open(pdf_path, "rb") as pdf_file:
        input_pdf_bytes = pdf_file.read()  # Read PDF as bytes

    # Define signature details
    signature_lines = [
        """<b>John Doe</b>""",
        "<i>Software Engineer</i>",
        "<i>ABC Corporation</i>"
    ]

    signature_img_link = "https://crm-backend-media-static.s3.ap-south-1.amazonaws.com/alpha/media/tgbpass_logo.png"

    description = "<b>This document is digitally signed for authentication.</b>"

    # Set signature position
    x_position = 400  # X-coordinate on the page
    y_position = 410  # Y-coordinate on the page
    page_number = 4   # Apply signature on page 1

    sign_block = SignBlock()
    # Call function
    signed_pdf_bytes = sign_block.add_signature_to_pdf(
        input_pdf_bytes=input_pdf_bytes,
        signature_lines=signature_lines,
        x=x_position,
        y=y_position,
        page_number=page_number,
        signature_img_link=signature_img_link,
        description=description
    )

    # Save the output PDF
    output_path = "sign_output.pdf"
    with open(output_path, "wb") as output_pdf:
        output_pdf.write(signed_pdf_bytes)

    print(f"Signed PDF saved as '{output_path}'")
else:
    print("Error: The specified PDF file was not found.")
