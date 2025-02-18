import fitz
from reportlab.lib.pagesizes import letter
from pathlib import Path
import io


def delete_qr_code(input_pdf_bytes: bytes, page_number: int, y_position: int) -> bytes:
    """
    Remove QR code from the given PDF (bytes) and return the modified PDF as bytes.
    :param input_pdf_bytes: The input PDF as bytes.
    :param page_number: The page number where the QR code needs to be removed.
    :param y_position: The Y-coordinate threshold for deletion.
    :return: The modified PDF as bytes.
    """
    # Load the PDF from bytes
    doc = fitz.open(stream=input_pdf_bytes, filetype="pdf")

    # Select the page to inspect
    page = doc[page_number - 1]

    # Get all images on the page
    images = page.get_images(full=True)
    width = letter[0]

    # Process each image on the page
    for img in images:
        xref = img[0]  # Image reference number
        bbox = page.get_image_rects(xref)  # Get image position

        if bbox:
            x0, y0, x1, y1 = bbox[0]
            if x0 > 0 and x1 < width / 2 and y1 > y_position:
                page.delete_image(xref)
                print(f"Deleted image at: {x0}, {y0}, {x1}, {y1}")

    # Save the modified PDF to bytes
    output_pdf_bytes = io.BytesIO()
    doc.save(output_pdf_bytes)
    doc.close()

    return output_pdf_bytes.getvalue()


# Example usage:
pdf_path = "sign_output.pdf"
if Path(pdf_path).exists():
    with open(pdf_path, "rb") as pdf_file:
        input_pdf_bytes = pdf_file.read()

    modified_pdf_bytes = delete_qr_code(
        input_pdf_bytes=input_pdf_bytes,
        page_number=4,
        y_position=410
    )

    # Save the modified PDF for verification
    with open("modified.pdf", "wb") as output_file:
        output_file.write(modified_pdf_bytes)