import requests
from io import BytesIO
from typing import List, Optional
import qrcode
from PIL import Image as PILImage
from reportlab.platypus import Spacer, Image, Flowable
from pdf_letter_generator.commons import QRCodeBlockStyles

class QRCodeBlock:

    def _create_qr_code(self, url: str) -> PILImage.Image:
        """
        Generate a QR code for the provided URL.

        Args:
            url (str): The URL to be encoded in the QR code.

        Returns:
            PIL.Image.Image: The generated QR code image.
        """
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
        """
        Download a logo image from a URL, resize it to fit in the center of the QR code,
        and overlay it on the QR code.

        Args:
            qr_img (PIL.Image.Image): The QR code image.
            logo_url (str): The URL of the logo image.

        Returns:
            PIL.Image.Image: The QR code with the logo overlayed.
        """
        # Download the logo image from the URL
        response = requests.get(logo_url)
        logo = PILImage.open(BytesIO(response.content))

        # Ensure the logo has an alpha channel (RGBA)
        logo = logo.convert("RGBA")

        # Resize the logo to fit into the QR code
        qr_width, qr_height = qr_img.size
        logo_size = min(qr_width, qr_height) // 4  # Set logo size as 1/4th of QR code size
        logo = logo.resize((logo_size, logo_size))

        # Calculate the position to center the logo on the QR code
        logo_position = ((qr_width - logo.size[0]) // 2, (qr_height - logo.size[1]) // 2)

        # Convert the QR code to RGB mode to ensure compatibility with colored logos
        qr_img = qr_img.convert("RGB")

        # Overlay the logo on the QR code using the alpha channel of the logo as the mask
        qr_img.paste(logo, logo_position, logo)

        return qr_img

    # Function to create PDF with QR code and logo
    def create_qr_code_flowables(self,
            qr_code_url:str,
            logo_url:Optional[str]=None,
            width:Optional[float]=QRCodeBlockStyles.DEFAULT_QRCODE_WIDTH,
            height:Optional[float]=QRCodeBlockStyles.DEFAULT_QRCODE_HEIGHT
    )->List[Flowable]:
        """
        Create a PDF with the QR code and logo.

        Args:
            pdf_filename (str): The output PDF file name.
            qr_img (PIL.Image.Image): The QR code image with the logo.
        """
        flowables = []
        qr_img = self._create_qr_code(url=qr_code_url)

        if logo_url:
            qr_img_with_logo = self._add_logo_to_qr(qr_img=qr_img, logo_url=logo_url)

            final_qr_buffer = BytesIO()
            qr_img_with_logo.save(final_qr_buffer, format="PNG")  # Save as PNG format for reportlab compatibility
            final_qr_buffer.seek(0)

        else:
            final_qr_buffer = BytesIO()
            qr_img.save(final_qr_buffer, format="PNG")  # Save as PNG format for reportlab compatibility
            final_qr_buffer.seek(0)


        final_qr_image = Image(final_qr_buffer, width=width, height=height)
        final_qr_image.hAlign = "LEFT"

        flowables.append(final_qr_image)
        flowables.append(Spacer(1, 24))

        return flowables