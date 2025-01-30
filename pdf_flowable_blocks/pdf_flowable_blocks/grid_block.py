"""
Grid Block Module V2 for PDF Generation

This module provides functionality for creating grid layouts as flowables
with multiple columns containing paragraph blocks with consistent formatting.
"""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from pdf_letter_generator.commons.constants import GridBlockStyles

logger = logging.getLogger(__name__)


class TextAlignment(str, Enum):
    """Enum for text alignment options."""

    LEFT = "LEFT"
    RIGHT = "RIGHT"
    CENTER = "CENTER"


ALIGNMENT_MAP = {
    TextAlignment.LEFT: TA_LEFT,
    TextAlignment.RIGHT: TA_RIGHT,
    TextAlignment.CENTER: TA_CENTER,
}


@dataclass
class BlockStyle:
    """Configuration for text block styling."""

    font: str
    size: float
    color: Any
    line_spacing: float = 1.5
    space_after: float = 0
    alignment: str = TA_LEFT


class GridBlockV2:
    """Handles the creation and management of grid layouts as flowables."""

    DEFAULT_STYLES = {
        "header": BlockStyle(
            font=GridBlockStyles.Header.FONT,
            size=GridBlockStyles.Header.SIZE,
            color=GridBlockStyles.Header.COLOR,
            alignment=GridBlockStyles.Header.ALIGNMENT,
            line_spacing=GridBlockStyles.Header.LINE_SPACING,
            space_after=GridBlockStyles.Header.SPACE_AFTER,
        ),
        "grid": BlockStyle(
            font=GridBlockStyles.Body.FONT,
            size=GridBlockStyles.Body.SIZE,
            color=GridBlockStyles.Body.COLOR,
            alignment=GridBlockStyles.Body.ALIGNMENT,
            line_spacing=GridBlockStyles.Body.LINE_SPACING,
            space_after=GridBlockStyles.Body.SPACE_AFTER,
        ),
    }

    def __init__(self):
        """Initialize the GridBlock with default styles."""
        self.stylesheet = self._create_stylesheet()

    def _create_stylesheet(self) -> StyleSheet1:
        """Create a StyleSheet with all grid styles."""
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
                    line_spacing=style.line_spacing,
                    wordWrap=GridBlockStyles.Header.WORD_WRAP,
                    # leftIndent=GridBlockStyles.INDENT_LEVELS[0]
                    # if name == "grid"
                    # else 0,
                    # firstLineIndent=GridBlockStyles.Body.FIRST_LINE_INDENT
                    # if name == "grid"
                    # else 0,
                    # allowWidows=0,
                    # allowOrphans=0,
                )
            )

        return stylesheet

    def _validate_grid_units(self, grid_units: List[Dict]) -> None:
        """Validate grid unit configurations."""
        if not isinstance(grid_units, list):
            raise ValueError("Grid units must be a list")

        total_width = 0
        for unit in grid_units:
            if not isinstance(unit, dict):
                raise ValueError("Each grid unit must be a dictionary")

            required_keys = {"text_lines", "unit_width"}
            if not all(key in unit for key in required_keys):
                raise ValueError(
                    f"Grid unit missing required keys: {required_keys}"
                )

            width = unit["unit_width"]
            if (
                not isinstance(width, (int, float))
                or width <= 0
                or width > 100
            ):
                raise ValueError("unit_width must be between 1 and 100")

            total_width += width

        if not 99 <= total_width <= 101:
            raise ValueError("Grid unit widths must sum to approximately 100%")

    def _create_grid_cells(
        self, grid_units: List[Dict]
    ) -> List[List[Paragraph]]:
        """Create grid cells from text lines."""
        cells = []
        max_lines = max(len(unit["text_lines"]) for unit in grid_units)

        for i in range(max_lines):
            row = []
            for unit in grid_units:
                text = (
                    unit["text_lines"][i]
                    if i < len(unit["text_lines"])
                    else ""
                )
                alignment = ALIGNMENT_MAP[
                    TextAlignment(unit.get("alignment", "LEFT"))
                ]
                style = ParagraphStyle(
                    f"grid_{i}",
                    parent=self.stylesheet["grid"],
                    alignment=alignment,
                )
                row.append(Paragraph(text, style))
            cells.append(row)

        return cells

    def create_grid_flowables(
        self,
        heading: Optional[str] = None,
        grid_units: Optional[List[Dict]] = None,
        heading_spacing: float = GridBlockStyles.DEFAULT_HEADING_SPACING,
        grid_spacing: float = GridBlockStyles.GRID_SPACING["DEFAULT"],
    ) -> List[Union[Paragraph, Spacer, Table]]:
        """Create grid block flowables.

        Args:
            heading: Optional heading text
            grid_units: List of grid unit configurations
            heading_spacing: Space between heading and grid
            grid_spacing: Space between grid rows

        Returns:
            List[Union[Paragraph, Spacer, Table]]: List of flowable objects
        """
        try:
            flowables = []

            if heading:
                header_para = Paragraph(heading, self.stylesheet["header"])
                flowables.append(header_para)
                flowables.append(Spacer(1, heading_spacing))

            if grid_units:
                self._validate_grid_units(grid_units)

                # Create grid cells
                cells = self._create_grid_cells(grid_units)

                # Calculate column widths as percentages
                col_widths = [
                    "{}%".format(unit["unit_width"]) for unit in grid_units
                ]

                # Create table with proper styling
                table = Table(cells, colWidths=col_widths)
                table.setStyle(
                    TableStyle(
                        [
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), grid_spacing)
                        ]
                    )
                )

                flowables.append(table)
            flowables.append(Spacer(1, 24))

            return flowables

        except Exception as e:
            logger.error(f"Error creating grid flowables: {str(e)}")
            raise
