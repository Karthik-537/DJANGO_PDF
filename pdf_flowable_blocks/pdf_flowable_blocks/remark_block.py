from typing import Dict, List, Optional

from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.colors import Color
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from pdf_flowable_blocks.pdf_flowable_blocks.grid_block import (
    ALIGNMENT_MAP,
    TextAlignment,
)
from pdf_flowable_blocks.pdf_flowable_blocks.paragraph_block import (
    ParagraphBlockV2,
)
from pdf_letter_generator.commons import (
    GridBlockStyles,
    RemarkBlockStyles,
)


class RemarkBlock:
    def create_remark_flowables(
        self,
        header_right_text: str,
        header_left_text: str,
        lines: Optional[list[str]] = None,
        grid_spacing: float = GridBlockStyles.GRID_SPACING["DEFAULT"],
    ):
        grid_units = [
            {
                "text_lines": [header_right_text],
                "unit_width": 55,
                "alignment": "LEFT",
            },
            {
                "text_lines": [header_left_text],
                "unit_width": 45,
                "alignment": "RIGHT",
            },
        ]

        flowables = []

        if grid_units:
            cells = self.create_grid_cells(grid_units)
            col_widths = [
                "{}%".format(unit["unit_width"]) for unit in grid_units
            ]

            table = Table(cells, colWidths=col_widths)
            table.setStyle(
                TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ALIGN", (0, 0), (0, 0), "LEFT"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), grid_spacing),
                    ]
                )
            )
            flowables.append(table)
        flowables.append(Spacer(1, 12))

        line = Drawing(500, 1)
        line_shape = Line(0, 0, 503, 0)
        line_shape.strokeColor = Color(0, 0, 0)
        line.add(line_shape)
        flowables.append(line)
        flowables.append(Spacer(0, 12))

        if lines:
            paragraph_block = ParagraphBlockV2()
            body_para = paragraph_block.create_flowables(lines=lines)
            flowables.extend(body_para)

        return flowables

    def create_grid_cells(
        self, grid_units: List[Dict]
    ) -> List[List[Paragraph]]:
        # TODO: Using in the export remarks also
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
                    parent=self._get_style_sheet("grid"),
                    alignment=alignment,
                )
                row.append(Paragraph(text, style))
            cells.append(row)

        return cells

    @staticmethod
    def _get_style_sheet(style_name):
        return {
            "grid": ParagraphStyle(
                "grid",
                fontName=RemarkBlockStyles.Body.FONT,
                fontSize=RemarkBlockStyles.Body.SIZE,
                textColor=RemarkBlockStyles.Body.COLOR,
                leading=RemarkBlockStyles.Body.SIZE
                * RemarkBlockStyles.Body.LINE_SPACING,
                spaceAfter=RemarkBlockStyles.Body.SIZE
                * RemarkBlockStyles.Body.SPACE_AFTER,
                alignment=RemarkBlockStyles.Body.ALIGNMENT,
                wordWrap=GridBlockStyles.Header.WORD_WRAP,
            )
        }[style_name]
