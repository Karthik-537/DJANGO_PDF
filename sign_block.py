import textwrap
from io import BytesIO
from typing import List, Optional

import pypdf
import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Flowable, Spacer, Paragraph

from pdf_letter_generator.commons.constants import (
    REGULAR_FONT,
    ParagraphBlockStyles,
)


class DummySignBlock(Flowable):
    def __init__(self, width=200, height=300):
        super().__init__()
        self.width = width
        self.height = height

        self.location = None
        self.parent_table = None

    def draw(self):
        # Get the canvas coordinates
        x, y = self.canv._currentMatrix[4], self.canv._currentMatrix[5]

        # If we have a parent table, use its top position
        if self.parent_table:
            # The table's y position will be the current y plus its height
            table_top = y + self.parent_table._height - 70
            self.location = (self.canv.getPageNumber(), x, table_top)
        else:
            # Fallback to original behavior
            top_y = y + self.height
            self.location = (self.canv.getPageNumber(), x, top_y)

    def add_spaces(self):
        return Spacer(1, 100)


def add_signature_to_pdf(
        input_pdf_bytes: bytes,
        signature_lines: List[str],
        x: float,
        y: float,
        page_number: int,
        signature_img_link: Optional[str] = None,
        description: Optional[str] = None,
):
    # Step 1: Create the signature overlay using reportlab
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    curr_y = y

    styles = getSampleStyleSheet()

    # Add "Yours Faithfully" text before the tick
    c.setFont(REGULAR_FONT, ParagraphBlockStyles.Body.SIZE)
    c.drawString(x, curr_y+60, "Yours Faithfully")  # Position above the tick

    # sign_icon_path = "plugins/pdf_letter_generator/images/sign_tick.png"
    # Add the signature image
    # c.drawImage(
    #     sign_icon_path,
    #     x,
    #     curr_y,
    #     width=50,
    #     height=50,
    #     mask="auto",  # This is key for handling transparency
    # )
    # curr_y -= 50  # Adjust y-coordinate after tick icon

    if signature_img_link:
        try:
            # Get image from URL
            response = requests.get(signature_img_link)
            if response.status_code == 200:
                img_data = BytesIO(response.content)
                img_reader = ImageReader(img_data)

                c.drawImage(
                    img_reader,
                    x,
                    curr_y,
                    width=100,
                    height=30,
                    mask="auto",
                )
                curr_y -= 30  # Adjust y-coordinate after signature image
        except Exception as e:
            print(f"Warning: Could not add signature image: {str(e)}")

    # Add additional signature lines
    # line_spacing = ParagraphBlockStyles.Body.SIZE + 4
    curr_y -= 2  # Add some padding between image and text
    # max_width = 40
    width, height = letter[0], letter[1]
    max_width = width - x - 50
    max_height = height
    for i, line in enumerate(signature_lines):
        # c.setFont(BOLD_FONT, ParagraphBlockStyles.Body.SIZE)
        # # # Wrap the text into multiple lines
        # wrapped_lines = textwrap.wrap(line, width=max_width)
        # for wrapped_line in wrapped_lines:
        paragraph = Paragraph(line, styles["Normal"])
        actual_width, actual_height = paragraph.wrapOn(c, max_width, max_height)
        paragraph.wrapOn(c, actual_width, actual_height)  # Wrap text within width
        paragraph.drawOn(c, x, curr_y-actual_height)
        curr_y -= actual_height

    curr_y -= 2  # Add some padding between lines and description

    # Add description after signature lines
    if description:
        paragraph = Paragraph(description, styles["Normal"])
        actual_width, actual_height = paragraph.wrapOn(c, max_width, max_height)
        paragraph.wrapOn(c, actual_width, actual_height)  # Wrap text within width
        paragraph.drawOn(c, x, curr_y - actual_height)
        curr_y -= actual_height

    c.save()

    # Step 2: Create PDF reader from input bytes
    pdf_reader = pypdf.PdfReader(BytesIO(input_pdf_bytes))
    pdf_writer = pypdf.PdfWriter()

    # Step 3: Create the signature overlay as a PDF
    packet.seek(0)
    new_pdf = pypdf.PdfReader(packet)
    signature_page = new_pdf.pages[0]

    # Step 4: Merge the signature overlay on the specified page
    page_index = page_number - 1
    if page_index < len(pdf_reader.pages):
        target_page = pdf_reader.pages[page_index]
        target_page.merge_page(signature_page)

        # Add all pages to the writer in original order
        for i in range(len(pdf_reader.pages)):
            if i == page_index:
                pdf_writer.add_page(target_page)  # Add the modified page
            else:
                pdf_writer.add_page(pdf_reader.pages[i])  # Add original pages

        # Step 5: Write the modified content to bytes
        output = BytesIO()
        pdf_writer.write(output)
        return output.getvalue()
    else:
        raise ValueError(
            f"Error: The PDF has only {len(pdf_reader.pages)} pages. The specified page number is out of range."
        )
