"""
Recipient Block Module V2 for PDF Generation

This module provides functionality for rendering recipient details
using ReportLab's high-level components (Platypus).
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Union

from commons.constants import (
    PDFLineSpacing,
    PDFMargins,
    PDFTextStyles,
    RecipientBlockStyles,
)
from pdf_config import PDFConfig
from reportlab.lib import colors
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.lib.units import inch
from reportlab.platypus import (
    CondPageBreak,
    KeepTogether,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class BlockStyle:
    """Configuration for recipient block styling."""

    font: str
    size: float
    color: Any
    line_spacing: float = 1.2
    space_after: float = 0.25
    alignment: str = TA_LEFT


class RecipientBlockV2:
    """Handles the creation and management of recipient blocks using Platypus."""

    # Default styles for different block elements
    DEFAULT_STYLES = {
        "header": BlockStyle(
            font=RecipientBlockStyles.Header.FONT,
            size=RecipientBlockStyles.Header.SIZE,
            color=RecipientBlockStyles.Header.COLOR,
            alignment=RecipientBlockStyles.Header.ALIGNMENT,
            line_spacing=RecipientBlockStyles.Header.LINE_SPACING,
            space_after=RecipientBlockStyles.Header.SPACE_AFTER,
        ),
        "body": BlockStyle(
            font=RecipientBlockStyles.Body.FONT,
            size=RecipientBlockStyles.Body.SIZE,
            color=RecipientBlockStyles.Body.COLOR,
            alignment=RecipientBlockStyles.Body.ALIGNMENT,
            line_spacing=RecipientBlockStyles.Body.LINE_SPACING,
            space_after=RecipientBlockStyles.Body.SPACE_AFTER,
        ),
    }

    def __init__(self):
        """Initialize the RecipientBlock with default styles."""
        self.stylesheet = self._create_stylesheet()

    def _create_stylesheet(self) -> StyleSheet1:
        """Create a StyleSheet with all recipient block styles."""
        stylesheet = StyleSheet1()

        # Add base styles
        for name, style in self.DEFAULT_STYLES.items():
            stylesheet.add(
                ParagraphStyle(
                    name,
                    fontName=style.font,
                    fontSize=style.size,
                    textColor=style.color,
                    leading=style.size * style.line_spacing,
                    spaceAfter=style.size * style.space_after,
                    alignment=style.alignment,
                )
            )

        # Add left-aligned style for letter info
        stylesheet.add(
            ParagraphStyle(
                "letter_info", parent=stylesheet["body"], alignment=TA_LEFT
            )
        )

        return stylesheet

    def _create_letter_info_table(
        self, letter_no: str, letter_date: str
    ) -> Table:
        """Create a table for letter information.

        Args:
            letter_no: Letter number
            letter_date: Letter date

        Returns:
            Table: Formatted table with letter information
        """
        letter_info = [
            [
                Paragraph(
                    f"Letter No: {letter_no}", self.stylesheet["letter_info"]
                )
            ],
            [
                Paragraph(
                    f"Date: {letter_date}", self.stylesheet["letter_info"]
                )
            ],
        ]

        table = Table(
            letter_info,
            colWidths=[3 * inch],  # Fixed width for right column
            spaceBefore=0,
            spaceAfter=0,
        )

        return table

    def _create_recipient_details(
        self, name: str, father: str, address: str, state: str
    ) -> List[Paragraph]:
        """Create recipient details paragraphs.

        Args:
            name: Recipient name
            father: Recipient's father's name
            address: Recipient address
            state: Recipient state

        Returns:
            List[Paragraph]: List of formatted paragraphs
        """
        details = ["To,", name, father, address, state]

        return [Paragraph(line, self.stylesheet["body"]) for line in details]

    def create_recipient_flowables(
        self, data: Dict[str, Any]
    ) -> List[Union[Table, Paragraph, Spacer]]:
        """Create recipient block flowables.

        Args:
            data: Dictionary containing recipient details with keys:
                - recipient_name
                - recipient_father
                - recipient_address
                - recipient_state
                - letter_no
                - letter_date

        Returns:
            List[Union[Table, Paragraph, Spacer]]: List of flowable objects

        Raises:
            KeyError: If required fields are missing from data
        """
        try:
            # Validate required fields
            required_fields = [
                "recipient_name",
                "recipient_father",
                "recipient_address",
                "recipient_state",
                "letter_no",
                "letter_date",
            ]

            missing_fields = [
                field for field in required_fields if field not in data
            ]
            if missing_fields:
                raise KeyError(
                    f"Missing required fields: {', '.join(missing_fields)}"
                )

            flowables = []

            # Create recipient details
            recipient_paras = self._create_recipient_details(
                data["recipient_name"],
                data["recipient_father"],
                data["recipient_address"],
                data["recipient_state"],
            )

            # Create letter info
            letter_info = self._create_letter_info_table(
                data["letter_no"], data["letter_date"]
            )

            # Create two-column layout
            available_width = PDFConfig.get_page_width() - (
                2 * PDFConfig.MARGIN
            )
            col_width = available_width / 2

            # Create recipient table
            recipient_table = Table(
                [[para] for para in recipient_paras],
                colWidths=[col_width - 0.1 * inch],
                spaceBefore=0,
                spaceAfter=0,
            )

            # Create letter info with padding
            padding = 0.2 * col_width  # 20% padding
            letter_info_with_padding = Table(
                [[Spacer(1, padding), letter_info]],  # Add padding as a cell
                colWidths=[padding, col_width - padding],
                spaceBefore=0,
                spaceAfter=0,
            )

            two_col_data = [
                [
                    recipient_table,  # Left column: Recipient details
                    letter_info_with_padding,  # Right column: Letter info with padding
                ]
            ]

            # Create the final two-column table
            two_col_table = Table(
                two_col_data,
                colWidths=[col_width, col_width],
                spaceBefore=0.2 * inch,
                spaceAfter=0.3 * inch,
            )

            # Add style for alignment
            two_col_table.setStyle(
                TableStyle(
                    [
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "TOP",
                        ),  # Top align vertically
                        (
                            "ALIGN",
                            (0, 0),
                            (-1, -1),
                            "LEFT",
                        ),  # Left align all cells
                    ]
                )
            )

            flowables.append(two_col_table)

            # Add final spacing
            flowables.append(Spacer(1, 0.3 * inch))

            return flowables

        except Exception as e:
            logger.error(f"Error creating recipient flowables: {str(e)}")
            raise
