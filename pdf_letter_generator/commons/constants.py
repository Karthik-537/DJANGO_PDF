"""
Constants Module for PDF Generation

This module provides centralized, reusable constants for PDF generation,
ensuring consistent styling, spacing, and presentation across the entire project.

Key Features:
- Standardized text styles
- Consistent margins and indentation
- Uniform line spacing
- Presentation type enumerations

Design Principles:
1. Single source of truth for styling constants
2. Easy global configuration
3. Improved code readability and maintainability
4. Flexibility for future modifications

Usage:
    from commons.constants import PDFMargins, PDFLineSpacing, PresentationType

    # Example usage
    content_indent = PDFMargins.INDENT_SMALL
    line_height = PDFLineSpacing.SINGLE
    presentation = PresentationType.PARAGRAPH
"""
from enum import Enum

from reportlab.lib import colors
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch

REGULAR_FONT = "Helvetica"
BOLD_FONT = "Helvetica-Bold"


class PresentationType(Enum):
    """
    Enumeration for text presentation types in PDF blocks.

    Provides standardized presentation options for text rendering:
    - PARAGRAPH: Standard continuous text
    - UNORDERED_LIST: Bulleted list
    - ORDERED_LIST: Numbered list

    Example:
        block_config = {
            'presentation_type': PresentationType.UNORDERED_LIST
        }
    """

    PARAGRAPH = "paragraph"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class PDFMargins:
    """
    Standard margin and indentation values for PDF layout.

    Provides consistent spacing values for:
    - Page margins
    - Text indentation
    - Block spacing
    - Table cell padding

    Example:
        margin = PDFMargins.MARGIN
        indent = PDFMargins.INDENT_SMALL
    """

    MARGIN = 1 * inch
    TOP = inch
    BOTTOM = inch
    LEFT = 0.25 * inch
    RIGHT = 0.25 * inch
    INDENT_SMALL = 0.25 * inch
    INDENT_MEDIUM = 0.5 * inch
    INDENT_LARGE = 0.75 * inch

    # Block spacing
    BLOCK_SPACING = 12
    HEADING_SPACING = 0.15 * inch

    # Header Block
    HEADING_BLOCK_PADDING = 0.3 * inch

    # Table specific
    CELL_PADDING_LEFT = 12  # Points
    CELL_PADDING_RIGHT = 18  # Points
    TABLE_MARGIN_TOP = 0.2 * inch
    TABLE_MARGIN_BOTTOM = 0.2 * inch
    VERTICAL_MARGIN_BETWEEN_BLOCKS = 0.3 * inch


class PDFTextStyles:
    """
    Standardized text styles for consistent PDF typography.

    Provides predefined font, size, and color configurations
    for different text elements like headers and body text.

    Nested classes:
    - Header: Styling for section headers
    - TextBlockHeading: Styling for text block headings
    - Body: Styling for main content text
    - List: Styling for list-related text elements

    Example:
        canvas.setFont(PDFTextStyles.Header.FONT, PDFTextStyles.Header.SIZE)
    """

    DEFAULT_FONT = REGULAR_FONT
    DEFAULT_FONT_SIZE = 8
    DEFAULT_BOLD_FONT = BOLD_FONT
    DEFAULT_LEADING = 10
    DEFAULT_ALIGNMENT = "LEFT"
    DEFAULT_COLOR = colors.black
    DEFAULT_PADDING = 3

    class Header:
        """Header text style configuration."""

        FONT = BOLD_FONT
        SIZE = 16
        COLOR = colors.black
        ALIGNMENT = "left"
        SPACE_BEFORE = 10
        SPACE_AFTER = 0

    class SubHeader:
        """Body text style configuration."""

        FONT = BOLD_FONT
        SIZE = 13
        COLOR = black
        ALIGNMENT = "left"
        SPACE_BEFORE = 7
        SPACE_AFTER = 0

    class RightBlock:
        """Body text style configuration."""

        FONT = BOLD_FONT
        SIZE = 16
        COLOR = colors.green
        ALIGNMENT = "left"
        SPACE_BEFORE = 7
        SPACE_AFTER = 0

    class TextBlockHeading:
        """Text block heading style configuration."""

        FONT = BOLD_FONT
        SIZE = 10
        COLOR = black
        ALIGNMENT = "left"

    class TableBlockHeading:
        FONT = BOLD_FONT
        SIZE = 12
        COLOR = black
        ALIGNMENT = "left"

    class Body:
        """Body text style configuration."""

        FONT = REGULAR_FONT
        SIZE = 12
        COLOR = black
        ALIGNMENT = "left"
        SPACE_BEFORE = 7
        SPACE_AFTER = 0

    class List:
        """List text style configuration."""

        BULLET_FONT = REGULAR_FONT
        BULLET_SIZE = 12
        BULLET_COLOR = black
        BULLET_SYMBOL = "•"  # Default bullet symbol

    class Footer:
        """Footer text style configuration."""

        FONT = REGULAR_FONT
        SIZE = 10
        COLOR = black
        ALIGNMENT = "center"


class PDFLineSpacing:
    """
    Line spacing constants for precise text rendering.

    Provides multipliers and vertical spacing constants
    to control text line height and vertical positioning.

    Attributes:
        SINGLE (float): Standard single line spacing (1.2)
        CONDENSED (float): Tighter line spacing (1.1)
        VERTICAL_SPACING (float): Global vertical gap between lines
        COMPACT (float): Very compact line spacing (1.05)
        ONE_POINT_FIVE (float): One-and-a-half line spacing
        DOUBLE (float): Double line spacing

    Example:
        line_height = body_config['size'] * PDFLineSpacing.SINGLE
    """

    SINGLE = 1.2
    CONDENSED = 1.1
    VERTICAL_SPACING = 0.025  # Global vertical spacing
    COMPACT = 1.05
    ONE_POINT_FIVE = 1.5
    DOUBLE = 2.0


class PDFTableSpacing:
    """
    Configurable spacing constants for table blocks and headings.

    Provides consistent spacing values for:
    - Table block vertical spacing
    - Heading block vertical spacing
    """

    # Vertical spacing between table and surrounding text blocks
    TABLE_BLOCK_SPACING = 0.2 * inch

    # Heading spacing similar to text block spacing
    HEADING_BLOCK_SPACING = 0.3 * inch


class ParagraphBlockStyles:
    """
    Comprehensive styling configuration for paragraph blocks.

    Provides predefined styles for different paragraph elements:
    - Default styles for headers and body text
    - Font configurations
    - Spacing and alignment settings
    - Color schemes

    Example:
        header_style = {
            'font': ParagraphBlockStyles.Header.FONT,
            'size': ParagraphBlockStyles.Header.SIZE,
            'color': ParagraphBlockStyles.Header.COLOR,
            'alignment': ParagraphBlockStyles.Header.ALIGNMENT,
            'spacing': ParagraphBlockStyles.Header.LINE_SPACING
        }
    """

    class Header:
        """Header styling configuration for paragraph blocks."""

        FONT = BOLD_FONT
        SIZE = 12
        COLOR = black
        ALIGNMENT = TA_LEFT
        LINE_SPACING = 1.2
        SPACE_AFTER = 0.25
        INDENT = 0
        FIRST_LINE_INDENT = 0
        WORD_WRAP = "CJK"  # Better word wrapping for all text types

    class Body:
        """Body text styling configuration for paragraph blocks."""

        FONT = REGULAR_FONT
        SIZE = 10
        COLOR = black
        ALIGNMENT = (
            TA_LEFT  # Changed from justify to left for better readability
        )
        LINE_SPACING = 2
        SPACE_AFTER = 0.25
        INDENT = PDFMargins.INDENT_SMALL
        FIRST_LINE_INDENT = 0
        WORD_WRAP = "CJK"

    class Quote:
        """Block quote styling configuration for paragraph blocks."""

        FONT = REGULAR_FONT
        SIZE = 10
        COLOR = black
        ALIGNMENT = TA_LEFT
        LINE_SPACING = 1.1
        SPACE_AFTER = 0.25
        INDENT = PDFMargins.INDENT_MEDIUM
        FIRST_LINE_INDENT = 0
        WORD_WRAP = "CJK"

    class Emphasis:
        """Emphasized text styling configuration for paragraph blocks."""

        FONT = BOLD_FONT
        SIZE = 10
        COLOR = black
        ALIGNMENT = TA_LEFT
        LINE_SPACING = 1.2
        SPACE_AFTER = 0.25
        INDENT = PDFMargins.INDENT_SMALL
        FIRST_LINE_INDENT = 0
        WORD_WRAP = "CJK"

    # Spacing configurations
    DEFAULT_HEADING_SPACING = 0.1 * inch
    COMPACT_HEADING_SPACING = 0.1 * inch
    WIDE_HEADING_SPACING = 0.2 * inch

    # Paragraph spacing configurations
    PARAGRAPH_SPACING = {
        "DEFAULT": PDFMargins.BLOCK_SPACING,
        "COMPACT": 0.15 * inch,
        "WIDE": 0.4 * inch,
    }

    # Special formatting options
    BULLET_CHAR = "•"
    NUMBER_FORMAT = "{0}."
    INDENT_LEVELS = {
        0: PDFMargins.INDENT_SMALL,
        1: PDFMargins.INDENT_MEDIUM,
        2: PDFMargins.INDENT_LARGE,
    }


class ListBlockStyles:
    """
    Comprehensive styling configuration for list blocks.

    Provides predefined styles for different list elements:
    - Default styles for headers and list items
    - Font configurations
    - Spacing and alignment settings
    - Bullet and number formatting

    Example:
        list_style = {
            'font': ListBlockStyles.ListItem.FONT,
            'size': ListBlockStyles.ListItem.SIZE,
            'color': ListBlockStyles.ListItem.COLOR,
            'alignment': ListBlockStyles.ListItem.ALIGNMENT,
            'spacing': ListBlockStyles.ListItem.LINE_SPACING
        }
    """

    class Header:
        """Header styling configuration for list blocks."""

        FONT = BOLD_FONT
        SIZE = 12
        COLOR = black
        ALIGNMENT = TA_LEFT
        LINE_SPACING = 1.2
        SPACE_AFTER = 0.25
        INDENT = 0
        FIRST_LINE_INDENT = 0
        WORD_WRAP = "CJK"

    class ListItem:
        """List item styling configuration."""

        FONT = REGULAR_FONT
        SIZE = 10
        COLOR = black
        ALIGNMENT = TA_LEFT
        LINE_SPACING = 2
        SPACE_AFTER = 0.15
        INDENT = PDFMargins.INDENT_SMALL
        BULLET_INDENT = 0.02 * inch
        FIRST_LINE_INDENT = 0
        WORD_WRAP = "CJK"

        # Bullet configuration
        BULLET_CHAR = "•"
        BULLET_FONT = REGULAR_FONT
        BULLET_SIZE = 10
        BULLET_COLOR = black

        # Number configuration
        NUMBER_FORMAT = "{0}."
        NUMBER_FONT = REGULAR_FONT
        NUMBER_SIZE = 10
        NUMBER_COLOR = black

    # Spacing configurations
    DEFAULT_HEADING_SPACING = 0.1 * inch
    COMPACT_HEADING_SPACING = 0.1 * inch
    WIDE_HEADING_SPACING = 0.2 * inch

    # List item spacing configurations
    LIST_ITEM_SPACING = {
        "DEFAULT": 0.1 * inch,
        "COMPACT": 0.05 * inch,
        "WIDE": 0.15 * inch,
    }

    # Indentation levels for nested lists
    INDENT_LEVELS = {
        0: PDFMargins.INDENT_SMALL,
        1: PDFMargins.INDENT_MEDIUM,
        2: PDFMargins.INDENT_LARGE,
    }

    # Bullet characters for different levels
    BULLET_CHARS = {0: "•", 1: "○", 2: "▪"}


class GridBlockStyles:
    """
    Comprehensive styling configuration for grid blocks.
    """

    class Header:
        """Header styling configuration for grid blocks."""

        FONT = BOLD_FONT
        SIZE = 12
        COLOR = black
        ALIGNMENT = TA_LEFT
        LINE_SPACING = 1.2
        SPACE_AFTER = 0.25
        INDENT = 0
        FIRST_LINE_INDENT = 0
        WORD_WRAP = "CJK"

    class Body:
        """Body text styling configuration for grid blocks."""

        FONT = REGULAR_FONT
        SIZE = 10
        COLOR = black
        ALIGNMENT = TA_LEFT
        LINE_SPACING = 0.5
        SPACE_AFTER = 0.25
        INDENT = 0.25 * inch
        FIRST_LINE_INDENT = 0
        WORD_WRAP = "CJK"

    # Spacing configurations
    DEFAULT_HEADING_SPACING = 0.1 * inch
    COMPACT_HEADING_SPACING = 0.1 * inch
    WIDE_HEADING_SPACING = 0.2 * inch

    # Grid spacing configurations
    GRID_SPACING = {
        "DEFAULT": 0.1 * inch,
        "COMPACT": 0.05 * inch,
        "WIDE": 0.15 * inch,
    }

    # Indentation levels for nested content
    INDENT_LEVELS = [0.25 * inch, 0.5 * inch, 0.75 * inch]


# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
#
# FONTS_DIR = "/home/ps-dev-022/Desktop/Projects/crm-backend/plugins/pdf_letter_generator/fonts" # -> Need to Update
#
# # 1. First register the individual font files
# font_regular = os.path.join(FONTS_DIR, "verdana.ttf")
# font_bold = os.path.join(FONTS_DIR, "verdana-bold.ttf")
#
# pdfmetrics.registerFont(TTFont("Verdana", font_regular))
# pdfmetrics.registerFont(TTFont("Verdana-Bold", font_bold))

# Export key constants for easy importing
__all__ = [
    "PresentationType",
    "PDFTextStyles",
    "PDFMargins",
    "PDFLineSpacing",
    "PDFTableSpacing",
    "ParagraphBlockStyles",
    "ListBlockStyles",
    "GridBlockStyles",
]
