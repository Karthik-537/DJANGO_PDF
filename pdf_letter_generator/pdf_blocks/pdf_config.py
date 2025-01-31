from reportlab.lib.colors import Color, black, gray
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from pdf_letter_generator.commons.constants import (
    BOLD_FONT,
    REGULAR_FONT,
)


class PDFConfig:
    """
    Centralized configuration for PDF generation with flexible styling
    """

    # Page Settings
    PAGE_SIZE = letter
    MARGIN = 48

    # Expanded font configurations with more flexibility
    FONTS = {
        "header": {
            "name": BOLD_FONT,
            "size": 10,
            "color": black,
            "weight": "bold",
            "style": "normal",
        },
        "title": {
            "name": BOLD_FONT,
            "size": 12,
            "color": black,
            "weight": "bold",
            "style": "normal",
        },
        "body": {
            "name": REGULAR_FONT,
            "size": 10,
            "color": black,
            "weight": "normal",
            "style": "normal",
        },
        "footer": {
            "name": REGULAR_FONT,
            "size": 8,
            "color": black,
            "weight": "normal",
            "style": "italic",
        },
    }

    # Table Colors
    HEADER_COLOR = Color(0.85, 0.85, 0.85)  # Light gray for header
    HEADER_TEXT_COLOR = black
    BODY_COLOR = Color(0.95, 0.95, 0.95)  # Very light gray for body
    BODY_TEXT_COLOR = black
    GRID_COLOR = gray

    # Block Positioning Configuration
    BLOCK_POSITIONS = {
        "header": {"y_start": 1 * inch, "line_spacing": 0.2 * inch},
        "title": {"y_start": 2.5 * inch, "centered": True},
        "recipient": {"y_start": 3.5 * inch, "line_spacing": 0.2 * inch},
        "subject": {"y_start": 5.5 * inch, "line_spacing": 0.2 * inch},
        "permission_body": {"y_start": 7.5 * inch, "line_spacing": 0.2 * inch},
        "road_conditions": {
            "y_start": 9.5 * inch,
            "line_spacing": 0.2 * inch,
            "x_offset": 6 * inch,
        },
        "remarks": {
            "y_start": 10.5 * inch,
            "line_spacing": 0.3 * inch,
            "x_offset": 6 * inch,
        },
        "general_conditions": {
            "y_start": 11.5 * inch,
            "line_spacing": 0.2 * inch,
        },
        "signature": {"y_start": 13 * inch, "line_spacing": 0.2 * inch},
    }

    # Positioning Helpers
    @classmethod
    def get_page_height(cls):
        return cls.PAGE_SIZE[1]

    @classmethod
    def get_page_width(cls):
        return cls.PAGE_SIZE[0]

    @classmethod
    def get_right_margin(cls):
        return cls.get_page_width() - cls.MARGIN

    @classmethod
    def get_block_config(cls, block_name):
        """
        Retrieve configuration for a specific block

        :param block_name: Name of the block to retrieve config for
        :return: Dictionary of block configuration
        """
        return cls.BLOCK_POSITIONS.get(block_name, {})

    @classmethod
    def get_font_config(cls, font_style):
        """
        Retrieve font configuration for a specific style

        :param font_style: Name of the font style
        :return: Dictionary of font configuration
        """
        return cls.FONTS.get(font_style, cls.FONTS["body"])

    @classmethod
    def set_font_config(cls, font_style: str, **kwargs):
        """
        Update font configuration dynamically.

        Args:
            font_style (str): Name of the font style to modify
            **kwargs: Font configuration parameters to update
        """
        if font_style not in cls.FONTS:
            raise ValueError(f"Font style '{font_style}' not found")

        cls.FONTS[font_style].update(kwargs)
