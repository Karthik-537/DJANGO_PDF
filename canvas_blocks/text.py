from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
from typing import Optional
from reportlab.lib.pagesizes import letter


class TextBlockCanvas:

    TEXT_FONT_SIZE = 12
    FONT = "Helvetica"

    def add_text_to_existing_pdf(
            self, input_pdf_bytes: bytes,
            x: float,
            y: float,
            text: str,
            page_number: int,
            font_size: Optional[int] = TEXT_FONT_SIZE
    ) -> bytes:
        reader = PdfReader(io.BytesIO(input_pdf_bytes))
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            if i == page_number - 1:
                page_width = letter[0]
                page_height = letter[1]
                overlay_pdf = self._draw_text(
                    x=x,
                    y=y,
                    text=text,
                    page_width=page_width,
                    page_height=page_height,
                    font_size=font_size
                )
                overlay_page = PdfReader(overlay_pdf).pages[0]
                page.merge_page(overlay_page)
            writer.add_page(page)

        output_pdf_bytes = io.BytesIO()
        writer.write(output_pdf_bytes)
        writer.close()

        return output_pdf_bytes.getvalue()

    def _draw_text(
            self, text: str,
            x: float,
            y: float,
            page_width: float,
            page_height: float,
            font_size: int
    ) -> io.BytesIO:
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))

        y = page_height-y
        words = text.split(' ')
        current_line = ''
        line_height = 14
        max_width = page_width-x-48
        for word in words:
            test_line = current_line + ' ' + word if current_line else word
            test_width = c.stringWidth(test_line, self.FONT, font_size)
            if test_width > max_width:
                c.drawString(x, y, current_line)
                y -= line_height
                current_line = word
            else:
                current_line = test_line
        if current_line:
            c.drawString(x, y, current_line)
        c.save()
        packet.seek(0)

        return packet


pdf_path = "modified.pdf"
with open(pdf_path, "rb") as pdf_file:
    pdf_bytes = pdf_file.read()

text_block = TextBlockCanvas()
modified_pdf_bytes = text_block.add_text_to_existing_pdf(
    input_pdf_bytes=pdf_bytes,
    x=100,
    y=100,
    text="The Building permission is sanctioned subject to following conditions. The applicant should follow the clause 5.f (i) (ii) (iii) (iv) (v)( vii) (xi)&(xiv) of G.O.Ms.No.168, MA&UD, dt:07.04.2012.",
    page_number=4
)

with open("canvas.pdf", "wb") as output_file:
    output_file.write(modified_pdf_bytes)

print("Text block added successfully!")
