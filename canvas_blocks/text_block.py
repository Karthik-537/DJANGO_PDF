from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
from typing import Optional
from reportlab.lib.units import inch


class TextBlockCanvas:

    DEFAULT_TEXT_FONT_SIZE = 12
    FONT = "Helvetica"

    def add_text_to_existing_pdf(
            self, input_pdf_bytes: bytes,
            x: float,
            y: float,
            text: str,
            page_number: int,
            page_height: int,
            page_width: int,
            font_size: Optional[int] = DEFAULT_TEXT_FONT_SIZE
    ) -> bytes:
        reader = PdfReader(io.BytesIO(input_pdf_bytes))
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            if i == page_number - 1:
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

        y = page_height - y
        # words = text.split(' ')
        # current_line = ''
        line_height = 14
        max_width = 300
        c.setFont(self.FONT, font_size)
        count = 0
        text_count = 1
        while y > inch:
            words = text.split(' ')
            current_line = ''
            line_count = 1
            for word in words:
                test_line = current_line + ' ' + word if current_line else word
                test_width = c.stringWidth(test_line, self.FONT, font_size)
                if test_width > max_width and line_count == 1:
                    current_line = f"{text_count}.{current_line}"
                    c.drawString(x, y, current_line)
                    y -= line_height
                    current_line = word
                    line_count += 1
                elif test_width > max_width:
                    c.drawString(x, y, current_line)
                    y -= line_height
                    current_line = word
                    line_count += 1
                else:
                    current_line = test_line
            if current_line:
                c.drawString(x, y, current_line)
            text_count += 1
            y -= 20
            count += 1
        print(count)
        c.save()
        packet.seek(0)

        return packet


pdf_path = "example.pdf"
with open(pdf_path, "rb") as pdf_file:
    pdf_bytes = pdf_file.read()

text_block = TextBlockCanvas()
modified_pdf_bytes = text_block.add_text_to_existing_pdf(
    input_pdf_bytes=pdf_bytes,
    x=72,
    y=72,
    text="In the heart of a bustling city, quiet moments often go unnoticed. Beneath towering "
         "skyscrapers and busy streets, tiny pockets of serenity await discovery. A gentle breeze"
         " stirs the leaves, and soft whispers of nature remind us to pause. Every corner holds "
         "a story, and every face reflects hope, resilience, and dreams of a brighter tomorrow."
         " Amid the urban clamor, hidden gardens bloom with colors and fragrances that lift the "
         "spirit, inviting passersby to cherish fleeting beauty. Sunlight graces every bloom!!!",
    page_height=6741,
    page_width=4768,
    page_number=1
)

with open("canvas.pdf", "wb") as output_file:
    output_file.write(modified_pdf_bytes)

print("Text added successfully!")
