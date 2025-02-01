from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.pdfgen import canvas
from reportlab.platypus import Flowable


class RoundedTablePDF(Flowable):
    def __init__(self, filename, data, x=100, y=500, col_width=100, row_height=30, radius=10):
        self.filename = filename
        self.data = data
        self.x = x
        self.y = y
        self.col_width = col_width
        self.row_height = row_height
        self.radius = radius

        # Set the width and height of the flowable
        self.width = col_width * len(data[0])  # Width of the table
        self.height = row_height * len(data)  # Height of the table

    def draw_rounded_table(self, c):
        """Draw a table with rounded corners."""
        rows = len(self.data)
        cols = len(self.data[0])

        # Loop through rows and columns to draw rounded rects for cells and add text
        for row in range(rows):
            for col in range(cols):
                x_pos = self.x + col * self.col_width
                y_pos = self.y - (row + 1) * self.row_height

                # Draw rounded rectangle for each cell
                c.setFillColor(colors.white)  # Cell background color
                c.setStrokeColor(colors.black)  # Cell border color
                c.roundRect(x_pos, y_pos, self.col_width, self.row_height, self.radius, stroke=1, fill=1)

                # Add text to each cell
                c.setFont("Helvetica-Bold", 10)
                text = str(self.data[row][col])
                c.drawString(x_pos + 10, y_pos + 10, text)

    def draw(self):
        """Override the draw method from Flowable to render on the canvas."""
        canvas_obj = self.canv
        self.draw_rounded_table(canvas_obj)

    def wrap(self, aW, aH):
        """Override wrap to specify width and height."""
        return self.width, self.height

    def generate_pdf(self):
        """Generates the PDF with a rounded table."""
        doc = SimpleDocTemplate(self.filename, pagesize=letter)
        elements = [self]  # Add the current flowable (rounded table) to elements list
        doc.build(elements)
        print(f"PDF generated successfully: {self.filename}")


# Sample Data
data = [
    ['Name', 'Age', 'City'],
    ['Alice', '24', 'New York'],
    ['Bob', '27', 'London'],
    ['Charlie', '22', 'Paris']
]

# Generate the PDF
pdf = RoundedTablePDF("rounded_table.pdf", data)
pdf.generate_pdf()
