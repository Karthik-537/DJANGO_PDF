import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter

# Load the PDF
def delete_qr_code(file_path:str, page_number:int, y_position:int):

    pdf_path = file_path  # Change to your PDF file
    doc = fitz.open(pdf_path)

    # Select the page to inspect
    page = doc[page_number - 1]

    # Get all images on the page
    images = page.get_images(full=True)
    width = letter[0]
    # Print image details (coordinates, size, etc.)
    for img in images:
        xref = img[0]  # Image reference number
        bbox = page.get_image_rects(xref)  # Get image position

        if bbox:
            x0, y0, x1, y1 = bbox[0]
            if x0 > 0 and x1 < width/2 and y1 > y_position:
                page.delete_image(xref)
                print(x0, y0, x1, y1)

    doc.save("modified.pdf")
    doc.close()

delete_qr_code(
    file_path="sign_output.pdf",
    page_number=4,
    y_position=410
    )
