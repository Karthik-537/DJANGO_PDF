"""
Recipient Block Module for Work Commencement Letter

This module handles the creation and formatting of the recipient block
with a focus on clean, modular design.
"""

import logging
from typing import Dict

from reportlab.lib.colors import black

from plugins.interactors.dms.pdf_blocks.pdf_config import PDFConfig
from plugins.pdf_letter_generator.commons.constants import (
    BOLD_FONT,
    REGULAR_FONT,
    PDFLineSpacing,
    PDFMargins,
)
from plugins.pdf_letter_generator.pdf_blocks import (
    ValidationError,
    validate_data,
)

# Configure logging
logger = logging.getLogger(__name__)

# Recipient block specific styles
RECIPIENT_STYLES = {
    "header": {"font": BOLD_FONT, "size": 10, "color": black},
    "body": {"font": REGULAR_FONT, "size": 10, "color": black},
}


class RecipientBlockValidator:
    """Validates recipient block data before PDF generation."""

    @staticmethod
    def validate(data: Dict[str, str]) -> None:
        """
        Validate recipient block data with comprehensive checks.

        :param data: Dictionary of recipient block data
        :raises ValidationError: If data fails validation
        """
        required_fields = [
            "recipient_name",
            "recipient_father",
            "recipient_address",
            "recipient_state",
            "letter_no",
            "letter_date",
        ]
        validate_data(data, required_fields)

        # Length validations
        field_max_lengths = {
            "recipient_name": 100,
            "recipient_father": 100,
            "recipient_address": 200,
            "recipient_state": 50,
            "letter_no": 50,
            "letter_date": 20,
        }

        for field, max_length in field_max_lengths.items():
            if len(data[field]) > max_length:
                raise ValidationError(
                    "{} is too long (max {} characters)".format(
                        field.replace("_", " ").title(), max_length
                    )
                )


def add_recipient_block(canvas, data: Dict[str, str], layout):
    """
    Add the recipient details block to the PDF with precise formatting.

    :param canvas: PDF canvas to draw on
    :param data: Dictionary containing recipient information
    :param layout: Layout manager
    """
    # Validate recipient block data
    RecipientBlockValidator.validate(data)

    # Get font configurations
    header_config = RECIPIENT_STYLES["header"]
    body_config = RECIPIENT_STYLES["body"]

    # Calculate page dimensions
    page_width = PDFConfig.get_page_width()
    margin = PDFConfig.MARGIN

    # Calculate maximum width for each block
    max_width = (page_width - (2 * margin)) / 2

    # Wrap long address
    def wrap_text(text, max_width, font, font_size):
        """
        Wrap text to fit within a specified width

        :param text: Text to wrap
        :param max_width: Maximum width in points
        :param font: Font name
        :param font_size: Font size
        :return: List of wrapped lines
        """
        words = text.split()
        lines = []
        current_line = []
        current_line_width = 0

        for word in words:
            # Calculate width of the word
            word_width = canvas.stringWidth(word + " ", font, font_size)

            # If adding this word would exceed max width, start a new line
            if current_line_width + word_width > max_width:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_line_width = canvas.stringWidth(
                    word + " ", font, font_size
                )
            else:
                current_line.append(word)
                current_line_width += word_width

        # Add the last line
        if current_line:
            lines.append(" ".join(current_line))

        return lines

    # Prepare recipient details with wrapped address
    recipient_details = [
        "To,",
        data["recipient_name"],
        data["recipient_father"],
    ]

    # Wrap address
    wrapped_address = wrap_text(
        data["recipient_address"],
        max_width,
        body_config["font"],
        body_config["size"],
    )
    recipient_details.extend(wrapped_address)
    recipient_details.append(data["recipient_state"])

    # Prepare letter details
    letter_details = [
        "Letter No: {}".format(data["letter_no"]),
        "Date: {}".format(data["letter_date"]),
    ]

    # Draw "To" block (Left-aligned)
    canvas.setFont(header_config["font"], header_config["size"])
    canvas.setFillColor(header_config["color"])

    current_y = layout.current_y
    current_x = margin

    # Draw each line of recipient details
    for line in recipient_details:
        canvas.setFont(
            header_config["font"] if line == "To," else body_config["font"],
            header_config["size"] if line == "To," else body_config["size"],
        )
        canvas.setFillColor(
            header_config["color"] if line == "To," else body_config["color"]
        )

        canvas.drawString(current_x, current_y, line)
        current_y -= (
            header_config["size"] * PDFLineSpacing.SINGLE
            + PDFLineSpacing.VERTICAL_SPACING
        )

    # Draw Letter Details block (Left-aligned within its section)
    canvas.setFont(body_config["font"], body_config["size"])
    canvas.setFillColor(body_config["color"])

    current_y = layout.current_y
    current_x = page_width - max_width

    for line in letter_details:
        # Draw left-aligned within the Letter Details section
        canvas.drawString(current_x, current_y, line)
        current_y -= (
            body_config["size"] * PDFLineSpacing.SINGLE
            + PDFLineSpacing.VERTICAL_SPACING
        )

    # Adjust current Y position to the lower of the two blocks
    layout.current_y = min(
        layout.current_y
        - len(recipient_details)
        * (
            header_config["size"] * PDFLineSpacing.SINGLE
            + PDFLineSpacing.VERTICAL_SPACING
        ),
        layout.current_y
        - len(letter_details)
        * (
            body_config["size"] * PDFLineSpacing.SINGLE
            + PDFLineSpacing.VERTICAL_SPACING
        ),
    )

    # Add vertical spacing between blocks
    layout.current_y -= PDFMargins.VERTICAL_MARGIN_BETWEEN_BLOCKS
