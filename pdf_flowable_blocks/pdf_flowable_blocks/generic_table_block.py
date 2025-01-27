"""
Generic Table Block Module V2 for PDF Generation

This module provides a flexible way to create tables with varying row structures
and column widths using ReportLab's high-level components (Platypus).
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from plugins.interactors.dms.pdf_blocks.pdf_config import PDFConfig
from plugins.interactors.dms.pdf_flowable_blocks.paragraph_block import (
    ParagraphBlockV2,
)
from plugins.pdf_letter_generator.commons import (
    ParagraphBlockStyles,
    PDFLineSpacing,
    PDFTextStyles,
)
from plugins.pdf_letter_generator.commons.text_utils import sanitize

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class CellConfig:
    """Configuration for a table cell"""

    value: Any
    width: float  # Width as percentage (0-100)
    align: str = "LEFT"
    bold: bool = False
    font_size: Optional[float] = None
    background_color: Optional[Any] = None
    text_color: Optional[Any] = None
    colspan: int = 1
    rowspan: int = 1
    pad_right: bool = False
    height: Optional[float] = None


@dataclass
class RowConfig:
    """Configuration for a table row"""

    cells: List[CellConfig]
    height: Optional[float] = None
    style: Optional[Dict[str, Any]] = None
    pad_to_max: bool = True


@dataclass
class BlockStyle:
    """Configuration for table block styling."""

    font: str
    size: float
    color: Any
    line_spacing: float = 1.2
    space_after: float = 0.25
    alignment: str = TA_LEFT


class GenericTableBlockV2:
    DEFAULT_STYLES = {
        "table_cell": BlockStyle(
            font=PDFTextStyles.DEFAULT_FONT,
            size=PDFTextStyles.DEFAULT_FONT_SIZE,
            color=PDFTextStyles.DEFAULT_COLOR,
            alignment=TA_LEFT,
            line_spacing=PDFLineSpacing.SINGLE,
            space_after=0,
        ),
    }

    def __init__(self):
        self.stylesheet = self._create_stylesheet()
        self.alignment_map = {
            "LEFT": TA_LEFT,
            "CENTER": TA_CENTER,
            "RIGHT": TA_RIGHT,
        }

    def _create_stylesheet(self) -> StyleSheet1:
        stylesheet = StyleSheet1()
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
        return stylesheet

    def _format_cell_content(self, cell: CellConfig) -> Union[str, Paragraph]:
        if not cell.value:
            return ""

        text = sanitize(str(cell.value))
        style = ParagraphStyle(
            f"cell_{id(cell)}",
            parent=self.stylesheet["table_cell"],
            alignment=self.alignment_map.get(cell.align.upper(), TA_LEFT),
        )

        if cell.bold:
            style.fontName = PDFTextStyles.DEFAULT_FONT
        if cell.font_size:
            style.fontSize = cell.font_size
            style.leading = cell.font_size * style.leading / style.fontSize
        if cell.text_color:
            style.textColor = cell.text_color

        return Paragraph(text, style)

    @staticmethod
    def _calculate_max_columns(rows: List[RowConfig]) -> int:
        max_cols = 0
        for row in rows:
            current_cols = sum(cell.colspan for cell in row.cells)
            max_cols = max(max_cols, current_cols)
        return max_cols

    @staticmethod
    def _create_row_style(borders: bool) -> TableStyle:
        style_commands = [
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), PDFTextStyles.DEFAULT_PADDING),
            ("BOTTOMPADDING", (0, 0), (-1, -1), PDFTextStyles.DEFAULT_PADDING),
            ("LEFTPADDING", (0, 0), (-1, -1), PDFTextStyles.DEFAULT_PADDING),
            ("RIGHTPADDING", (0, 0), (-1, -1), PDFTextStyles.DEFAULT_PADDING),
            ("TEXTCOLOR", (0, 0), (-1, -1), PDFTextStyles.DEFAULT_COLOR),
            ("FONTNAME", (0, 0), (-1, -1), PDFTextStyles.DEFAULT_FONT),
            ("FONTSIZE", (0, 0), (-1, -1), PDFTextStyles.DEFAULT_FONT_SIZE),
        ]

        if borders:
            style_commands.append(
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey)
            )

        return TableStyle(style_commands)

    def create_generic_table_flowables(
        self,
        rows: List[RowConfig],
        borders: bool = True,
        heading: Optional[str] = None,
        repeat_header: bool = True,
        split_rows: bool = True,
    ) -> List[Union[Table, Spacer]]:
        """Create table flowables from row configurations."""
        try:
            if not rows:
                return []

            flowables = []
            available_width = PDFConfig.get_page_width() - (
                2 * PDFConfig.MARGIN
            )

            # Add heading using ParagraphBlockV2 if present
            if heading:
                paragraph_block = ParagraphBlockV2()
                heading_flowables = paragraph_block.create_flowables(
                    heading=heading,
                    lines=None,
                    header_style=BlockStyle(
                        font=ParagraphBlockStyles.Header.FONT,
                        size=ParagraphBlockStyles.Header.SIZE,
                        color=ParagraphBlockStyles.Header.COLOR,
                        alignment=ParagraphBlockStyles.Header.ALIGNMENT,
                        line_spacing=ParagraphBlockStyles.Header.LINE_SPACING,
                        space_after=ParagraphBlockStyles.Header.SPACE_AFTER,
                    ),
                )
                flowables.extend(heading_flowables)

            # Process rows
            for row in rows:
                row_data = []
                row_widths = []
                total_width = sum(cell.width for cell in row.cells)

                for cell in row.cells:
                    cell_content = self._format_cell_content(cell)
                    row_data.append(cell_content)
                    cell_width = (cell.width / total_width) * available_width
                    row_widths.append(cell_width)

                row_style = self._create_row_style(borders)

                if row.style:
                    if "background_color" in row.style:
                        row_style.add(
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            row.style["background_color"],
                        )
                    if "text_color" in row.style:
                        row_style.add(
                            "TEXTCOLOR",
                            (0, 0),
                            (-1, 0),
                            row.style["text_color"],
                        )

                col_idx = 0
                for cell in row.cells:
                    if cell.background_color:
                        row_style.add(
                            "BACKGROUND",
                            (col_idx, 0),
                            (col_idx + cell.colspan - 1, 0),
                            cell.background_color,
                        )
                    if cell.colspan > 1:
                        row_style.add(
                            "SPAN",
                            (col_idx, 0),
                            (col_idx + cell.colspan - 1, 0),
                        )
                    col_idx += cell.colspan

                row_table = Table(
                    [row_data], colWidths=row_widths, style=row_style
                )

                container_table = Table(
                    [[row_table]],
                    colWidths=[available_width],
                    style=TableStyle(
                        [
                            ("TOPPADDING", (0, 0), (-1, -1), 0),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ]
                    ),
                )

                flowables.append(container_table)

            flowables.append(Spacer(1, 0.2 * inch))
            return flowables

        except Exception as e:
            logger.error(f"Error creating table flowables: {str(e)}")
            raise
