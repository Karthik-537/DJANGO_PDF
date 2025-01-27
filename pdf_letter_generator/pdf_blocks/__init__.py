"""
Utilities for PDF block generation and validation
"""
from reportlab.lib.units import inch

from plugins.interactors.dms.pdf_blocks.pdf_config import PDFConfig


class ValidationError(Exception):
    """Custom exception for data validation errors"""


def validate_data(data, required_fields):
    """
    Validate that all required fields are present in the data dictionary

    :param data: Dictionary of input data
    :param required_fields: List of required field names
    :raises ValidationError: If any required field is missing
    """
    missing_fields = [
        field
        for field in required_fields
        if field not in data or data[field] is None
    ]
    if missing_fields:
        raise ValidationError(
            "Missing required fields: {}".format(", ".join(missing_fields))
        )


def draw_text_line(
    canvas, text, x, y, font_style="body", align="left", color=None
):
    """
    Utility function to draw text with consistent formatting

    :param canvas: PDF canvas to draw on
    :param text: Text to draw
    :param x: X position
    :param y: Y position
    :param font_style: Font style to use
    :param align: Text alignment
    :param color: Optional text color
    """
    # Get font configuration
    font_config = PDFConfig.get_font_config(font_style)

    # Set font
    canvas.setFont(font_config["name"], font_config["size"])

    # Set color if provided, otherwise use default
    if color:
        canvas.setFillColor(color)
    else:
        canvas.setFillColor(font_config.get("color", (0, 0, 0)))

    # Adjust text based on alignment
    if align == "center":
        text_width = canvas.stringWidth(
            text, font_config["name"], font_config["size"]
        )
        x = x - text_width / 2
    elif align == "right":
        text_width = canvas.stringWidth(
            text, font_config["name"], font_config["size"]
        )
        x = x - text_width

    # Draw text
    canvas.drawString(x, y, text)


def draw_multiline_text(
    canvas,
    lines,
    x,
    y,
    font_style="body",
    align="left",
    line_spacing=None,
    color=None,
):
    """
    Draw multiple lines of text

    :param canvas: PDF canvas to draw on
    :param lines: List of text lines to draw
    :param x: Starting X position
    :param y: Starting Y position
    :param font_style: Font style to use
    :param align: Text alignment
    :param line_spacing: Optional line spacing
    :param color: Optional text color
    """
    # Use default line spacing if not provided
    line_spacing = line_spacing or PDFConfig.get_font_config(font_style).get(
        "line_spacing", 0.2 * inch
    )

    # Draw each line
    current_y = y
    for line in lines:
        draw_text_line(
            canvas,
            line,
            x,
            current_y,
            font_style=font_style,
            align=align,
            color=color,
        )
        current_y -= line_spacing


class PDFLayoutManager:
    """
    Manages PDF layout, tracking current position and handling page breaks
    """

    def __init__(self, canvas, initial_y=None):
        """
        Initialize the layout manager

        :param canvas: PDF canvas to draw on
        :param initial_y: Optional initial Y position, defaults to top of page
        """
        self.canvas = canvas
        self.current_y = (
            initial_y or PDFConfig.get_page_height() - PDFConfig.MARGIN
        )
        self.current_x = PDFConfig.MARGIN
        self.page_width = PDFConfig.get_page_width()
        self.page_height = PDFConfig.get_page_height()
        self.margin = PDFConfig.MARGIN
        self.min_space_required = (
            1 * inch
        )  # Minimum space before forcing a page break

    def get_next_position(self):
        """Get the next available position for content."""
        return self.current_x, self.current_y

    def get_content_width(self):
        """Get the available width for content."""
        return self.page_width - (2 * self.margin)

    def ensure_space(self, space_needed):
        """
        Ensure there's enough space for the next block, create new page if needed

        :param space_needed: Amount of vertical space required
        :return: Y position to start drawing
        """
        if self.current_y - space_needed < self.margin:
            # Not enough space, create a new page
            self.canvas.showPage()
            self.current_y = self.page_height - self.margin

        return self.current_y

    def draw_multiline_text(
        self,
        lines,
        x,
        font_style="body",
        align="left",
        line_spacing=None,
        color=None,
    ):
        """
        Draw multiline text and update current Y position

        :param lines: List of text lines to draw
        :param x: X position to start drawing
        :param font_style: Font style to use
        :param align: Text alignment
        :param line_spacing: Optional line spacing
        :param color: Optional text color
        :return: Final Y position after drawing
        """
        # Use default line spacing if not provided
        line_spacing = line_spacing or PDFConfig.get_font_config(
            font_style
        ).get("line_spacing", 0.2 * inch)

        # Ensure space for text
        space_needed = len(lines) * line_spacing
        start_y = self.ensure_space(space_needed)

        # Draw text
        current_y = start_y
        for line in lines:
            draw_text_line(
                self.canvas,
                line,
                x,
                current_y,
                font_style=font_style,
                align=align,
                color=color,
            )
            current_y -= line_spacing

        # Update current Y position
        self.current_y = current_y
        return current_y

    def draw_text_line(
        self,
        text,
        x,
        align="left",
        font_style="body",
        color=None,
        y_position=None,
    ):
        """
        Draw a single line of text with flexible positioning and styling

        :param text: Text to draw
        :param x: X-coordinate for text positioning
        :param align: Text alignment (left, center, right)
        :param font_style: Style of font to use
        :param color: Color of text (optional)
        :param y_position: Optional specific Y-coordinate for text (overrides current_y)
        """
        # Get font configuration
        font_config = PDFConfig.get_font_config(font_style)

        # Set font and size
        self.canvas.setFont(font_config["name"], font_config["size"])

        # Set color (use provided color or default from font config)
        text_color = (
            color if color is not None else font_config.get("color", (0, 0, 0))
        )
        self.canvas.setFillColor(text_color)

        # Determine Y position
        y = y_position if y_position is not None else self.current_y

        # Calculate text width for alignment
        text_width = self.canvas.stringWidth(
            text, font_config["name"], font_config["size"]
        )
        page_width = PDFConfig.get_page_width()

        # Adjust X based on alignment
        if align == "center":
            x = (page_width - text_width) / 2
        elif align == "right":
            x = page_width - text_width - PDFConfig.MARGIN

        # Draw text
        self.canvas.drawString(x, y, text)

        # Update current Y if not using specific y_position
        if y_position is None:
            self.current_y -= font_config["size"] * 1.2  # Line spacing

    def update_position(self, new_y):
        """Update the current Y position and handle page breaks if needed.

        Args:
            new_y: New Y position to move to
        """
        self.current_y = new_y
        if self.current_y < self.margin:
            self.canvas.showPage()
            self.current_y = self.page_height - self.margin

    def update_y_position(self, new_y):
        """
        Update the current vertical position.

        :param new_y: New vertical position to set
        """
        self.current_y = new_y
