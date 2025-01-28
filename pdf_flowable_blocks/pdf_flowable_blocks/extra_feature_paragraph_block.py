from reportlab.platypus import Spacer
from pdf_flowable_blocks.pdf_flowable_blocks.paragraph_block import ParagraphBlockV2
from pdf_letter_generator.commons.constants import GridBlockStyles
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from typing import Any, Dict, List, Optional
from reportlab.graphics.shapes import Drawing, Line
from reportlab.lib.colors import Color
from reportlab.platypus import Paragraph, Table, TableStyle
from dataclasses import dataclass
import logging
from pdf_flowable_blocks.pdf_flowable_blocks.grid_block import GridBlockV2
from pdf_letter_generator.pdf_blocks.pdf_config import PDFConfig
class ExtraFeatureParagraph:
    def create_feature_paragraph_flowables(self,
            lines:list[str],
            heading: Optional[str] = None,
            grid_units: Optional[List[Dict]] = None,
            heading_spacing: float = GridBlockStyles.DEFAULT_HEADING_SPACING,
            grid_spacing: float = GridBlockStyles.GRID_SPACING["DEFAULT"]
            ):
        flowables = []

        grid_block = GridBlockV2()

        if heading:
            header_para = Paragraph(heading, self.stylesheet["header"])
            flowables.append(header_para)
            flowables.append(Spacer(1, heading_spacing))

        if grid_units:

            cells =grid_block._create_grid_cells(grid_units)

            col_widths = [
                "{}%".format(unit["unit_width"]) for unit in grid_units
            ]
            table = Table(cells, colWidths=col_widths)
            table.setStyle(
                TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("ALIGN", (0,0), (0,0), "LEFT"),
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), grid_spacing)
                    ]
                )
            )
        flowables.append(table)

        line = Drawing(500, 1)
        line_shape = Line(0, 0, 500, 0)
        line_shape.strokeColor = Color(0, 0, 0)
        line.add(line_shape)
        flowables.append(line)
        flowables.append(Spacer(0, 12))


        paragraph_block = ParagraphBlockV2()
        body_para = paragraph_block.create_flowables(lines=lines)
        flowables.extend(body_para)

        return flowables