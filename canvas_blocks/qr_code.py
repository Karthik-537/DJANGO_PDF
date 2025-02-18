from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import qrcode
from PIL import Image as PILImage
import requests
import io
from reportlab.lib.pagesizes import letter


class QRCodeBlockCanvas:

    def add_qr_code_to_existing_pdf(
            self, input_pdf_bytes: bytes,
            qr_code_url: str,
            page_number: int,
            x: float,
            y: float,
            width: float,
            logo_url: str = None
    ) -> bytes:
        reader = PdfReader(io.BytesIO(input_pdf_bytes))
        writer = PdfWriter()

        for i, page in enumerate(reader.pages):
            if i == page_number - 1:
                page_width = letter[0]
                page_height = letter[1]
                qr_img = self._create_qr_code(url=qr_code_url)
                if logo_url:
                    qr_img = self._add_logo_to_qr(qr_img=qr_img, logo_url=logo_url)
                overlay_pdf = self._create_qr_overlay(
                                    qr_img=qr_img,
                                    x=x,
                                    y=y,
                                    width=width,
                                    page_width=page_width,
                                    page_height=page_height
                                )
                overlay_page = PdfReader(overlay_pdf).pages[0]
                page.merge_page(overlay_page)
            writer.add_page(page)

        output_pdf_bytes = io.BytesIO()
        writer.write(output_pdf_bytes)
        writer.close()

        return output_pdf_bytes.getvalue()

    @staticmethod
    def _create_qr_code(url: str) -> PILImage.Image:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=0
        )
        qr.add_data(url)
        qr.make(fit=True)
        return qr.make_image(fill="black", back_color="white")

    @staticmethod
    def _add_logo_to_qr(qr_img: PILImage.Image, logo_url: str) -> PILImage.Image:
        response = requests.get(logo_url)
        logo = PILImage.open(io.BytesIO(response.content)).convert("RGBA")

        qr_width, qr_height = qr_img.size
        logo_size = min(qr_width, qr_height) // 4
        logo = logo.resize((logo_size, logo_size))

        qr_img = qr_img.convert("RGB")
        logo_position = ((qr_width - logo.size[0]) // 2, (qr_height - logo.size[1]) // 2)
        qr_img.paste(logo, logo_position, logo)

        return qr_img

    @staticmethod
    def _create_qr_overlay(
            qr_img: PILImage.Image,
            x: float,
            y: float,
            width: float,
            page_width: float,
            page_height: float
    ) -> io.BytesIO:
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
        y = page_height - (y+width)
        qr_img_reader = ImageReader(qr_img)
        c.drawImage(qr_img_reader, x, y, width=width, height=width)
        c.save()
        buffer.seek(0)

        return buffer


pdf_path = "modified.pdf"
with open(pdf_path, "rb") as pdf_file:
    pdf_bytes = pdf_file.read()

qr_block = QRCodeBlockCanvas()
modified_pdf_bytes = qr_block.add_qr_code_to_existing_pdf(
    input_pdf_bytes=pdf_bytes,
    qr_code_url="https://www.amazon.in/",
    page_number=4,
    logo_url="https://crm-backend-media-static.s3.ap-south-1.amazonaws.com/alpha/media/tgbpass_logo.png",
    x=400,
    y=100,
    width=150
)

with open("canvas.pdf", "wb") as output_file:
    output_file.write(modified_pdf_bytes)

print("QR Code added successfully!")
