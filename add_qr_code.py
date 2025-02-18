from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
import qrcode
from PIL import Image as PILImage
import requests
import io

class QRCodeBlockCanvas:
    def _create_qr_code(self, url: str) -> PILImage.Image:
        """Generate a QR code for the provided URL."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=0
        )
        qr.add_data(url)
        qr.make(fit=True)
        return qr.make_image(fill="black", back_color="white")

    def _add_logo_to_qr(self, qr_img: PILImage.Image, logo_url: str) -> PILImage.Image:
        """Overlay a logo at the center of the QR code."""
        response = requests.get(logo_url)
        logo = PILImage.open(io.BytesIO(response.content)).convert("RGBA")

        qr_width, qr_height = qr_img.size
        logo_size = min(qr_width, qr_height) // 4
        logo = logo.resize((logo_size, logo_size))

        qr_img = qr_img.convert("RGB")
        logo_position = ((qr_width - logo.size[0]) // 2, (qr_height - logo.size[1]) // 2)
        qr_img.paste(logo, logo_position, logo)

        return qr_img

    def _create_qr_overlay(self, qr_img: PILImage.Image, x0: int, y0: int, x1: int, y1: int, page_width: float,
                           page_height: float) -> io.BytesIO:
        """Create a PDF overlay with the QR code at the specified location."""
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(page_width, page_height))

        # Convert coordinates to PDF space (flip y-axis)
        y0, y1 = page_height - y1, page_height - y0

        # Convert QR image to a format `drawImage` can use
        qr_img_reader = ImageReader(qr_img)

        # Draw the QR image on the canvas
        c.drawImage(qr_img_reader, x0, y0, width=x1 - x0, height=y1 - y0)
        c.save()
        buffer.seek(0)

        return buffer

    def add_qr_code_to_existing_pdf(self, input_pdf_bytes: bytes, qr_code_url: str, page_number: int, x0: int, y0: int, x1: int, y1: int, logo_url: str = None) -> bytes:
        """Add a QR code to a specific page of an existing PDF and return the modified PDF as bytes."""
        reader = PdfReader(io.BytesIO(input_pdf_bytes))
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            if i == page_number - 1:
                page_width = float(page.mediabox.width)
                page_height = float(page.mediabox.height)

                # Create the QR code
                qr_img = self._create_qr_code(qr_code_url)
                if logo_url:
                    qr_img = self._add_logo_to_qr(qr_img, logo_url)

                # Create overlay with QR code
                overlay_pdf = self._create_qr_overlay(qr_img, x0, y0, x1, y1, page_width, page_height)
                overlay_page = PdfReader(overlay_pdf).pages[0]

                # Merge overlay onto the original page
                page.merge_page(overlay_page)

            writer.add_page(page)

        output_pdf_bytes = io.BytesIO()
        writer.write(output_pdf_bytes)
        writer.close()

        return output_pdf_bytes.getvalue()


# Example Usage
pdf_path = "modified.pdf"
with open(pdf_path, "rb") as pdf_file:
    input_pdf_bytes = pdf_file.read()

qr_block = QRCodeBlockCanvas()
modified_pdf_bytes = qr_block.add_qr_code_to_existing_pdf(
    input_pdf_bytes=input_pdf_bytes,
    qr_code_url="https://www.amazon.in/",
    page_number=4,
    logo_url="https://crm-backend-media-static.s3.ap-south-1.amazonaws.com/alpha/media/tgbpass_logo.png",
    x0=54,
    y0=374,
    x1=204,
    y1=524
)

# Save the modified PDF
with open("final.pdf", "wb") as output_file:
    output_file.write(modified_pdf_bytes)

print("QR Code added successfully!")
