from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import io
from reportlab.lib.pagesizes import letter


class ImageBlockCanvas:

    def add_image_to_existing_pdf(
            self, input_pdf_bytes: bytes,
            image_url: str,
            x: float,
            y: float,
            width: float,
            height: float,
            page_number: int
    ) -> bytes:
        reader = PdfReader(io.BytesIO(input_pdf_bytes))
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            if i == page_number - 1:
                page_width = letter[0]
                page_height = letter[1]
                overlay_pdf = self._draw_image(
                    x=x,
                    y=y,
                    image_url=image_url,
                    page_width=page_width,
                    page_height=page_height,
                    width=width,
                    height=height
                )
                overlay_page = PdfReader(overlay_pdf).pages[0]
                page.merge_page(overlay_page)
            writer.add_page(page)

        output_pdf_bytes = io.BytesIO()
        writer.write(output_pdf_bytes)
        writer.close()

        return output_pdf_bytes.getvalue()

    @staticmethod
    def _draw_image(
            image_url: str,
            x: float,
            y: float,
            width: float,
            height: float,
            page_width: float,
            page_height: float
    ) -> io.BytesIO:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
        y = page_height - (y + width)
        c.drawImage(image_url, x, y, width=width, height=height, mask="auto")
        c.save()
        buffer.seek(0)

        return buffer


pdf_path = "modified.pdf"
with open(pdf_path, "rb") as pdf_file:
    pdf_bytes = pdf_file.read()

image_block = ImageBlockCanvas()
modified_pdf_bytes = image_block.add_image_to_existing_pdf(
    input_pdf_bytes=pdf_bytes,
    page_number=4,
    image_url="https://crm-backend-media-static.s3.ap-south-1.amazonaws.com/alpha/media/tgbpass_logo.png",
    x=400,
    y=100,
    width=150,
    height=150
)

with open("canvas.pdf", "wb") as output_file:
    output_file.write(modified_pdf_bytes)

print("Image added successfully!")
