"""
Header Block Module V2 for PDF Generation

This module handles the creation and formatting of the header block
using ReportLab's high-level components (Platypus).
"""

import logging
from typing import List, Optional

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.platypus import (
    Flowable,
    Image,
    KeepTogether,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from pdf_letter_generator.pdf_blocks.pdf_config import PDFConfig
from pdf_letter_generator.commons import (
    PDFLineSpacing,
    PDFTableSpacing,
    PDFTextStyles,
)
from pdf_letter_generator.commons.logo_handler import LogoHandler
from reportlab.lib import colors

# Configure logging
logger = logging.getLogger(__name__)


class HeaderBlockV2:
    """Class to handle the creation and management of PDF header blocks using Platypus."""

    # Width percentages for different sections
    LOGO_WIDTH_PERCENT = 0.12
    CENTER_WIDTH_PERCENT = 0.68
    RIGHT_WIDTH_PERCENT = 0.20

    # Line spacing between headings
    HEADING_LINE_SPACING = PDFLineSpacing.TEN

    # Center block padding (in inches)
    CENTER_BLOCK_PADDING = PDFTableSpacing.HEADING_BLOCK_SPACING

    def __init__(self):
        """Initialize the HeaderBlock with default styles."""
        self.stylesheet = self._create_stylesheet()
        self._logo_handler = LogoHandler()

    def _create_stylesheet(self) -> StyleSheet1:
        """Create a StyleSheet with all header styles."""
        stylesheet = StyleSheet1()

        stylesheet.add(
            ParagraphStyle(
                "header",
                fontName=PDFTextStyles.Header.FONT,
                fontSize=PDFTextStyles.Header.SIZE,
                textColor=PDFTextStyles.Header.COLOR,
                leading=PDFTextStyles.Header.SIZE * PDFLineSpacing.SINGLE,
                alignment=TA_CENTER,
                # spaceBefore=PDFTextStyles.Header.SPACE_BEFORE,
                # spaceAfter=PDFTextStyles.Header.SPACE_AFTER,
            )
        )

        stylesheet.add(
            ParagraphStyle(
                "subheader",
                fontName=PDFTextStyles.SubHeader.FONT,
                fontSize=PDFTextStyles.SubHeader.SIZE,
                textColor=PDFTextStyles.SubHeader.COLOR,
                leading=PDFTextStyles.SubHeader.SIZE * PDFLineSpacing.SINGLE,
                alignment=TA_CENTER,
                # spaceBefore=PDFTextStyles.SubSubHeader.SPACE_BEFORE,
                # spaceAfter=PDFTextStyles.SubSubHeader.SPACE_AFTER,
            )
        )

        stylesheet.add(
            ParagraphStyle(
                "subsubheader",
                fontName=PDFTextStyles.SubSubHeader.FONT,
                fontSize=PDFTextStyles.SubSubHeader.SIZE,
                textColor=PDFTextStyles.SubSubHeader.COLOR,
                leading=PDFTextStyles.SubSubHeader.SIZE * PDFLineSpacing.SINGLE,
                alignment=TA_CENTER,
                # spaceBefore=PDFTextStyles.Header.SPACE_BEFORE,
                # spaceAfter=PDFTextStyles.Header.SPACE_AFTER,
            )
        )

        stylesheet.add(
            ParagraphStyle(
                "right_block",
                fontName=PDFTextStyles.RightBlock.FONT,
                fontSize=PDFTextStyles.RightBlock.SIZE,
                textColor=PDFTextStyles.RightBlock.COLOR,
                leading=PDFTextStyles.RightBlock.SIZE * PDFLineSpacing.SINGLE,
                alignment=TA_CENTER,
                # spaceBefore=PDFTextStyles.RightBlock.SPACE_BEFORE,
                # spaceAfter=PDFTextStyles.RightBlock.SPACE_AFTER,
            )
        )

        return stylesheet

    def _create_logo_cell(
        self, logo_url: Optional[str], width: float
    ) -> List[Flowable]:
        """Create logo cell content."""
        if not logo_url:
            return [Spacer(1, 1)]

        try:
            # Create Image flowable with proper scaling
            img = Image(logo_url)
            aspect = img.imageHeight / float(img.imageWidth)
            img.drawWidth = width
            img.drawHeight = width * aspect
            return [img]
        except Exception as e:
            logger.error(f"Failed to add logo from {logo_url}: {e}")
            return [Spacer(1, 1)]

    def _create_center_cell(
        self,
        header_text: Optional[str],
        sub_header_text: Optional[str],
        sub_sub_header_text: Optional[str],
    ) -> List[Flowable]:
        """Create center cell content with headers."""
        content = []

        if header_text:
            content.append(Paragraph(header_text, self.stylesheet["header"]))
            content.append(Spacer(1, self.HEADING_LINE_SPACING))

        if sub_header_text:
            content.append(
                Paragraph(sub_header_text, self.stylesheet["subheader"])
            )
            content.append(Spacer(1, self.HEADING_LINE_SPACING))

        if sub_sub_header_text:
            content.append(
                Paragraph(sub_sub_header_text, self.stylesheet["subsubheader"])
            )

        return content or [Spacer(1, 1)]

    def _create_right_cell(self, text: Optional[str]) -> List[Flowable]:
        """Create right cell content."""
        if not text:
            return [Spacer(1, 1)]
        return [Paragraph(text, self.stylesheet["right_block"])]

    def create_header_flowables(
        self,
        logo_url: Optional[str] = None,
        header_text: Optional[str] = None,
        sub_header_text: Optional[str] = None,
        sub_sub_header_text: Optional[str] = None,
        right_block_text: Optional[str] = None,
    ) -> List[Flowable]:
        """Create header block flowables.

        Args:
            logo_url: Optional path to logo image
            header_text: Optional main header text
            sub_header_text: Optional sub-header text
            sub_sub_header_text: Optional sub-sub-header text
            right_block_text: Optional right block text

        Returns:
            List[Flowable]: List of flowable objects for the header
        """
        try:
            # Calculate widths based on percentages
            available_width = PDFConfig.get_page_width() - (
                2 * PDFConfig.MARGIN
            )
            col_widths = [
                available_width * self.LOGO_WIDTH_PERCENT,
                available_width * self.CENTER_WIDTH_PERCENT,
                available_width * self.RIGHT_WIDTH_PERCENT,
            ]

            # Create table data
            table_data = [
                [
                    self._create_logo_cell(logo_url, col_widths[0]),
                    self._create_center_cell(
                        header_text, sub_header_text, sub_sub_header_text
                    ),
                    self._create_right_cell(right_block_text),
                ]
            ]

            # Create table with proper styling
            table_style = TableStyle(
                [
                    # ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    # (
                    #     "LEFTPADDING",
                    #     (0, 0),
                    #     (-1, -1),
                    #     self.CENTER_BLOCK_PADDING,
                    # ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        0,
                    ),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    # ("BACKGROUND", (0,0), (0,0), "RED"),
                    # ("BACKGROUND", (1,0), (1,0), "YELLOW"),
                    # ("BACKGROUND", (2,0),(2,0),"BLUE"),
                ]
            )

            table = Table(table_data, colWidths=col_widths, style=table_style)

            # Wrap table in KeepTogether to prevent page breaks within header
            flowables = [KeepTogether(table), Spacer(1, 24)]

            return flowables

        except Exception as e:
            logger.error(f"Error creating header flowables: {str(e)}")
            raise
