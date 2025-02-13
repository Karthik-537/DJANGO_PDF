import fitz  # PyMuPDF
import requests
from io import BytesIO
import qrcode
from PIL import Image as PILImage
from pathlib import Path


class QRCodeBlockCanvas:
    def _create_qr_code(self, url: str) -> PILImage.Image:
        """Generate a QR code for the provided URL."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=0
        )
        qr.add_data(url)
        qr.make(fit=True)
        return qr.make_image(fill="black", back_color="white")

    def _add_logo_to_qr(self, qr_img: PILImage.Image, logo_url: str) -> PILImage.Image:
        """Overlay a logo at the center of the QR code."""
        response = requests.get(logo_url)
        logo = PILImage.open(BytesIO(response.content)).convert("RGBA")

        qr_width, qr_height = qr_img.size
        logo_size = min(qr_width, qr_height) // 4
        logo = logo.resize((logo_size, logo_size))

        qr_img = qr_img.convert("RGB")
        logo_position = ((qr_width - logo.size[0]) // 2, (qr_height - logo.size[1]) // 2)
        qr_img.paste(logo, logo_position, logo)

        return qr_img

    def add_qr_code_to_existing_pdf(self, input_pdf_bytes: bytes, qr_code_url: str,
                                    page_number: int, x0: int, y0: int, x1: int, y1: int,
                                    logo_url: str = None) -> bytes:
        """Add a QR code to a specific page of an existing PDF and return the modified PDF as bytes."""
        # Load the existing PDF from bytes
        doc = fitz.open(stream=input_pdf_bytes, filetype="pdf")

        # Ensure the page number is within range
        if page_number < 1 or page_number > len(doc):
            raise ValueError(f"Invalid page number! PDF has {len(doc)} pages.")

        # Get the specified page (page_number is 1-based, but PyMuPDF uses 0-based index)
        page = doc[page_number - 1]

        # Create the QR code
        qr_img = self._create_qr_code(qr_code_url)
        if logo_url:
            qr_img = self._add_logo_to_qr(qr_img, logo_url)

        # Convert QR code image to bytes
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)

        # Insert the QR code image at the specified location on the page
        img_rect = fitz.Rect(x0, y0, x1, y1)  # (x0, y0, x1, y1)
        page.insert_image(img_rect, stream=qr_buffer.read())

        # Save the modified PDF to bytes
        output_pdf_bytes = BytesIO()
        doc.save(output_pdf_bytes)
        doc.close()

        return output_pdf_bytes.getvalue()


# Example Usage
pdf_path = "modified.pdf"
if Path(pdf_path).exists():
    with open(pdf_path, "rb") as pdf_file:
        input_pdf_bytes = pdf_file.read()

    qr_block = QRCodeBlockCanvas()
    modified_pdf_bytes = qr_block.add_qr_code_to_existing_pdf(
        input_pdf_bytes=input_pdf_bytes,
        qr_code_url="https://www.amazon.in/?&tag=googhydrabk1-21&ref=pd_sl_5szpgfto9i_e&adgrpid=155259813593&hvpone=&hvptwo=&hvadid=674893540034&hvpos=&hvnetw=g&hvrand=7141621320752816559&hvqmt=e&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9062140&hvtargid=kwd-64107830&hydadcr=14452_2316413&gad_source=1",
        page_number=4,
        logo_url="https://crm-backend-media-static.s3.ap-south-1.amazonaws.com/alpha/media/tgbpass_logo.png",
        x0=54,
        y0=374,
        x1=204,
        y1=524
    )

    # Save the modified PDF for verification
    with open("final.pdf", "wb") as output_file:
        output_file.write(modified_pdf_bytes)