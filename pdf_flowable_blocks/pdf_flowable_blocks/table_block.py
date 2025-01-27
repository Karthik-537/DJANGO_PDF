"""
Table Block Module V2 for PDF Generation

This module provides functionality for rendering tables in PDFs
using ReportLab's high-level components (Platypus).
"""

import logging
from dataclasses import dataclass
from typing import Any, List, Optional, Union

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from plugins.interactors.dms.pdf_blocks.pdf_config import PDFConfig
from plugins.pdf_letter_generator.commons.constants import (
    PDFLineSpacing,
    PDFTableSpacing,
    PDFTextStyles,
)
from plugins.pdf_letter_generator.commons.text_utils import sanitize

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class TableBlockStyle:
    """Configuration for table styling."""

    font: str = PDFTextStyles.Body.FONT
    size: float = PDFTextStyles.Body.SIZE
    color: Any = PDFTextStyles.Body.COLOR
    cell_padding: float = 5
    line_spacing: float = PDFLineSpacing.SINGLE
    grid_color: Any = colors.grey
    grid_width: float = 0.5
    header_background: Any = colors.white
    row_background: Any = colors.white
    alternate_row_background: Any = colors.whitesmoke


class TableBlockV2:
    """Class to handle the creation and management of PDF table blocks using Platypus."""

    # Default styles for different table elements
    DEFAULT_STYLES = {
        "header": TableBlockStyle(
            font=PDFTextStyles.TextBlockHeading.FONT,
            size=PDFTextStyles.TextBlockHeading.SIZE,
            color=PDFTextStyles.TextBlockHeading.COLOR,
        ),
        "body": TableBlockStyle(
            font=PDFTextStyles.Body.FONT,
            size=PDFTextStyles.Body.SIZE,
            color=PDFTextStyles.Body.COLOR,
        ),
    }

    def __init__(self):
        """Initialize TableBlock with default styles."""
        self.stylesheet = self._create_stylesheet()

    def _create_stylesheet(self) -> StyleSheet1:
        """Create a StyleSheet with all table styles."""
        stylesheet = StyleSheet1()

        # Add table title style
        stylesheet.add(
            ParagraphStyle(
                "table_title",
                fontName=self.DEFAULT_STYLES["header"].font,
                fontSize=self.DEFAULT_STYLES["header"].size,
                textColor=self.DEFAULT_STYLES["header"].color,
                leading=self.DEFAULT_STYLES["header"].size
                * PDFLineSpacing.SINGLE,
                spaceBefore=PDFTableSpacing.TABLE_BLOCK_SPACING,
                spaceAfter=PDFTableSpacing.TABLE_BLOCK_SPACING,
                alignment=TA_LEFT,
            )
        )

        # Add table header style
        stylesheet.add(
            ParagraphStyle(
                "table_header",
                fontName=self.DEFAULT_STYLES["header"].font,
                fontSize=self.DEFAULT_STYLES["header"].size,
                textColor=self.DEFAULT_STYLES["header"].color,
                leading=self.DEFAULT_STYLES["header"].size
                * PDFLineSpacing.SINGLE,
                alignment=TA_CENTER,
            )
        )

        # Add table cell style
        stylesheet.add(
            ParagraphStyle(
                "table_cell",
                fontName=self.DEFAULT_STYLES["body"].font,
                fontSize=self.DEFAULT_STYLES["body"].size,
                textColor=self.DEFAULT_STYLES["body"].color,
                leading=self.DEFAULT_STYLES["body"].size
                * PDFLineSpacing.SINGLE,
                alignment=TA_LEFT,
            )
        )

        return stylesheet

    def _calculate_column_widths(
        self,
        total_width: float,
        first_row: List[Any],
        percentages: Optional[List[float]] = None,
    ) -> List[float]:
        """Calculate column widths based on percentages or equal distribution.

        Args:
            total_width: Total available width
            first_row: First row of data to determine number of columns
            percentages: Optional list of width percentages

        Returns:
            List[float]: List of column widths

        Raises:
            ValueError: If percentages are invalid
        """
        num_columns = len(first_row)

        if percentages:
            if len(percentages) != num_columns:
                raise ValueError(
                    "Number of percentages must match number of columns"
                )
            if (
                abs(sum(percentages) - 100) > 0.01
            ):  # Allow for floating point imprecision
                raise ValueError("Percentages must sum to 100")
            return [total_width * (pct / 100) for pct in percentages]

        # Default to equal distribution
        return [total_width / num_columns] * num_columns

    def _prepare_table_data(
        self,
        raw_data: List[List[Any]],
        style: Optional[TableBlockStyle] = None,
    ) -> List[List[Paragraph]]:
        """Prepare table data with wrapped paragraphs.

        Args:
            raw_data: Raw table data
            style: Optional custom style

        Returns:
            List[List[Paragraph]]: Processed table data with paragraphs
        """
        style = style or self.DEFAULT_STYLES["body"]
        processed_data = []

        for row_idx, row in enumerate(raw_data):
            processed_row = []
            for cell in row:
                # Use header style for first row, cell style for others
                style_name = "table_cell"
                cell_text = str(cell) if cell is not None else ""
                para = Paragraph(
                    sanitize(cell_text), self.stylesheet[style_name]
                )
                processed_row.append(para)
            processed_data.append(processed_row)

        return processed_data

    def _create_table_style(
        self, style: Optional[TableBlockStyle] = None, row_count: int = 0
    ) -> TableStyle:
        """Create table style with grid lines and formatting.

        Args:
            style: Optional custom style
            row_count: Number of rows in table

        Returns:
            TableStyle: Configured table style
        """
        style = style or self.DEFAULT_STYLES["body"]

        # Basic table style commands
        commands = [
            # Global settings
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTNAME", (0, 0), (-1, -1), style.font),
            ("FONTSIZE", (0, 0), (-1, -1), style.size),
            ("TEXTCOLOR", (0, 0), (-1, -1), style.color),
            ("TOPPADDING", (0, 0), (-1, -1), style.cell_padding),
            ("BOTTOMPADDING", (0, 0), (-1, -1), style.cell_padding),
            ("LEFTPADDING", (0, 0), (-1, -1), style.cell_padding),
            ("RIGHTPADDING", (0, 0), (-1, -1), style.cell_padding),
            # Header row settings
            ("FONTNAME", (0, 0), (-1, 0), self.DEFAULT_STYLES["header"].font),
            ("FONTSIZE", (0, 0), (-1, 0), self.DEFAULT_STYLES["header"].size),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                self.DEFAULT_STYLES["header"].color,
            ),
            ("BACKGROUND", (0, 0), (-1, 0), style.header_background),
            ("ALIGN", (0, 0), (-1, 0), "CENTER"),
            # Grid settings
            ("GRID", (0, 0), (-1, -1), style.grid_width, style.grid_color),
            (
                "INNERGRID",
                (0, 0),
                (-1, -1),
                style.grid_width,
                style.grid_color,
            ),
            ("BOX", (0, 0), (-1, -1), style.grid_width, style.grid_color),
        ]

        # Add alternating row colors if more than one data row
        if row_count > 1:
            for row in range(1, row_count):
                if row % 2 == 0:
                    commands.append(
                        (
                            "BACKGROUND",
                            (0, row),
                            (-1, row),
                            style.row_background,
                        )
                    )
                else:
                    commands.append(
                        (
                            "BACKGROUND",
                            (0, row),
                            (-1, row),
                            style.alternate_row_background,
                        )
                    )

        return TableStyle(commands)

    def create_table_flowables(
        self,
        heading: Optional[str] = None,
        table_data: List[List[Any]] = None,
        column_widths: Optional[List[float]] = None,
        style: Optional[TableBlockStyle] = None,
        repeat_header: bool = True,
        split_rows: bool = True,
    ) -> List[Union[Paragraph, Table, Spacer]]:
        """Create table block flowables.

        Args:
            heading: Optional table title
            table_data: Table data as list of lists
            column_widths: Optional list of column width percentages
            style: Optional custom style
            repeat_header: Whether to repeat header on new pages
            split_rows: Whether to allow row splits across pages

        Returns:
            List[Union[Paragraph, Table, Spacer]]: List of flowable objects

        Raises:
            ValueError: If table_data is empty or invalid
        """
        try:
            # if not table_data or not table_data[0]:
            #     raise ValueError("Table data cannot be empty")

            flowables = []
            available_width = PDFConfig.get_page_width() - (
                2 * PDFConfig.MARGIN
            )

            # Add heading if provided
            if heading:
                flowables.append(
                    Paragraph(heading, self.stylesheet["table_title"])
                )

            if not table_data:
                return flowables

            # Calculate column widths
            col_widths = self._calculate_column_widths(
                available_width, table_data[0], column_widths
            )

            # Prepare table data
            processed_data = self._prepare_table_data(table_data, style)

            # Create table with style
            table = Table(
                processed_data,
                colWidths=col_widths,
                # repeatRows=1 if repeat_header else 0,
                splitByRow=split_rows,
            )
            table.setStyle(
                self._create_table_style(style, len(processed_data))
            )

            flowables.append(table)
            flowables.append(Spacer(1, PDFTableSpacing.TABLE_BLOCK_SPACING))

            return flowables

        except Exception as e:
            logger.error(f"Error creating table flowables: {str(e)}")
            raise
