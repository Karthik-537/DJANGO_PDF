import html
import re
from io import BytesIO

from bs4 import BeautifulSoup, NavigableString
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


class HTMLToPDFConverter:
    def __init__(self):
        self.buffer = BytesIO()
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )
        self.styles = getSampleStyleSheet()
        self.story = []

        # Create custom styles for alignment
        self.custom_styles = {
            "left": ParagraphStyle(
                "CustomLeft", parent=self.styles["Normal"], alignment=TA_LEFT
            ),
            "center": ParagraphStyle(
                "CustomCenter",
                parent=self.styles["Normal"],
                alignment=TA_CENTER,
            ),
            "right": ParagraphStyle(
                "CustomRight", parent=self.styles["Normal"], alignment=TA_RIGHT
            ),
            "justify": ParagraphStyle(
                "CustomJustify",
                parent=self.styles["Normal"],
                alignment=TA_JUSTIFY,
            ),
        }

    def clean_text(self, text):
        """Clean and normalize text content."""
        if text is None:
            return ""
        # Decode HTML entities
        text = html.unescape(text)
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def get_alignment_style(self, tag):
        """Determine text alignment from HTML tag."""
        if not tag:
            return self.styles["Normal"]

        align = tag.get("align", "").lower()
        if not align:
            # Check style attribute
            style = tag.get("style", "").lower()
            if "text-align" in style:
                align = re.search(r"text-align:\s*(\w+)", style)
                if align:
                    align = align.group(1)

        return self.custom_styles.get(align, self.styles["Normal"])

    def process_text_with_style(self, element):
        """Process text with inline styling (bold, italic)."""
        text = ""
        for item in element.contents:
            if isinstance(item, NavigableString):
                text += self.clean_text(str(item))
            else:
                if item.name == "b" or item.name == "strong":
                    text += f"<b>{self.process_text_with_style(item)}</b>"
                elif item.name == "i" or item.name == "em":
                    text += f"<i>{self.process_text_with_style(item)}</i>"
                elif item.name == "u":  # Add handling for underline tag
                    text += f"<u>{self.process_text_with_style(item)}</u>"
                else:
                    text += self.process_text_with_style(item)
        return text

    def process_list(self, list_tag, ordered=False):
        """Process ordered and unordered lists."""
        items = []
        start_number = 1
        if ordered:
            # Check if there's a custom start number
            start = list_tag.get("start")
            if start and start.isdigit():
                start_number = int(start)

        for i, li in enumerate(list_tag.find_all("li", recursive=False)):
            text = self.process_text_with_style(li)
            if ordered:
                bullet = str(start_number + i) + "."
            else:
                bullet = "."

            style = self.get_alignment_style(li)
            items.append(
                ListItem(
                    Paragraph(text, style), leftIndent=20, bulletText=bullet
                )
            )

        list_flowable = ListFlowable(
            items,
            bulletType="1" if ordered else "bullet",
            leftIndent=15,
            bulletFontSize=10,
        )
        self.story.append(list_flowable)
        self.story.append(Spacer(1, 12))

    def process_tag(self, tag):
        """Process individual HTML tags and convert to appropriate PDF elements."""
        if isinstance(tag, NavigableString):
            text = self.clean_text(str(tag))
            if text:
                self.story.append(Paragraph(text, self.styles["Normal"]))
            return

        if tag.name is None:
            return

        # Handle lists
        if tag.name == "ul":
            self.process_list(tag, ordered=False)
            return
        elif tag.name == "ol":
            self.process_list(tag, ordered=True)
            return
        elif tag.name == "li":
            self.process_list(tag, ordered=True)
            return
        elif tag.name == "br":
            self.story.append(Spacer(1, 12))

        # Handle other text elements
        text = self.process_text_with_style(tag)
        if not text:
            return

        style = self.get_alignment_style(tag)

        if tag.name == "h1":
            base_style = self.styles["Heading1"]
            custom_style = ParagraphStyle(
                "CustomH1", parent=base_style, alignment=style.alignment
            )
            self.story.append(Spacer(1, 16))
            self.story.append(Paragraph(text, custom_style))
            self.story.append(Spacer(1, 16))

        elif tag.name == "h2":
            base_style = self.styles["Heading2"]
            custom_style = ParagraphStyle(
                "CustomH2", parent=base_style, alignment=style.alignment
            )
            self.story.append(Spacer(1, 12))
            self.story.append(Paragraph(text, custom_style))
            self.story.append(Spacer(1, 12))

        elif tag.name == "h3":
            base_style = self.styles["Heading3"]
            custom_style = ParagraphStyle(
                "CustomH3", parent=base_style, alignment=style.alignment
            )
            self.story.append(Spacer(1, 10))
            self.story.append(Paragraph(text, custom_style))
            self.story.append(Spacer(1, 10))

        elif tag.name in ["p", "div"]:
            self.story.append(Paragraph(text, style))
            self.story.append(Spacer(1, 12))

    def convert(self, html_content):
        """Convert HTML content to PDF."""
        # Parse HTML content
        soup = BeautifulSoup(html_content, "html.parser")

        # Process body content
        body = soup.find("body") or soup
        for tag in body.children:
            self.process_tag(tag)

        # Build PDF
        return self.story

    def html_to_pdf(self, flowables):
        """
        Convert HTML content to PDF file.

        Args:
            html_content (str): HTML content to convert
            output_path (str): Path where the PDF file should be saved
        """
        self.doc.build(flowables)
        pdf_bytes = self.buffer.getvalue()
        self.buffer.close()

        return pdf_bytes


# Example usage
if __name__ == "__main__":
    sample_html = """
    <h1 align="center">Sample Document</h1>
    <p style="text-align: justify">This is a justified paragraph with <b>bold</b> and <i>italic</i> text.</p>
    <h2 align="right">Section 1</h2>
    <p>Normal Text</p><p>Bold Text</p><p>Italic Text</p><p>Underline Text</p><p><a href=\"https://bps-officer-alpha.flowwlabs.tech/templates/c0f628ce-1b12-47d9-b1ba-7069e864231c/b/15cd7e47-f0af-4550-9a0f-ef8fb0e6c910?pid=271e916b-1bd5-4964-8eeb-0dcc608567bb&amp;rid=23645e99-d590-406c-8b30-d78ecea065a3\" rel=\"noopener noreferrer\" target=\"_blank\">Hyper Link</a></p><p><br></p><ol><li>List 1</li><li>List 2</li><li>List 3</li></ol><p><br></p><ul><li>List 1</li><li>List 2</li><li>List 3</li></ul><p><br></p><p class=\"ql-align-center\">sdfksdklfjsd</p><p class=\"ql-align-center\">sdfl;kajsd;fklasdf</p><p class=\"ql-align-center\">ssdfl;kasjd;flskdfjsd</p><p class=\"ql-align-center\">Middle Text</p><p class=\"ql-align-center\"><br></p><p class=\"ql-align-center\"><br></p><p class=\"ql-align-right\">Right Text</p><p class=\"ql-align-right\">Right Text 2</p>
    <p>Regular paragraph with default alignment.</p>
    <ul>
        <li>First bullet point with <b>bold</b> text</li>
        <li>Second bullet point with <i>italic</i> text</li>
    </ul>
    <br></br>
    <br></br>
    <br></br>
    <ol>
        <li>Numbered list starting at 5</li>
        <li>Second item (number 6)</li>
        <li>Third item (number 7)</li>
    </ol>
    <p align="center">This is a centered paragraph.</p>
    """

    html_to_pdf(sample_html)
