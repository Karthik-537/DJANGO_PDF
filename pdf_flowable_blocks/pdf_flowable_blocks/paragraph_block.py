"""
Paragraph Block Module V2 for PDF Generation

This module provides functionality for rendering paragraph-style text blocks
using ReportLab's high-level components (Platypus).
"""

import logging
from dataclasses import dataclass
from typing import Any, List, Optional, Union

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.platypus import Paragraph, Spacer
from reportlab.platypus.flowables import Flowable

from pdf_letter_generator.commons import ParagraphBlockStyles

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class BlockStyle:
    """Configuration for text block styling."""

    font: str
    size: float
    color: Any
    line_spacing: float = 1.2
    space_after: float = 0.25
    alignment: str = TA_JUSTIFY
    left_indent: float = ParagraphBlockStyles.INDENT_LEVELS[0]


class ParagraphBlockV2:
    """Handles the creation and management of paragraph text blocks in PDFs using Platypus."""

    # Default styles for different block elements
    DEFAULT_STYLES = {
        "header": BlockStyle(
            font=ParagraphBlockStyles.Header.FONT,
            size=ParagraphBlockStyles.Header.SIZE,
            color=ParagraphBlockStyles.Header.COLOR,
            alignment=ParagraphBlockStyles.Header.ALIGNMENT,
            line_spacing=ParagraphBlockStyles.Header.LINE_SPACING,
            space_after=ParagraphBlockStyles.Header.SPACE_AFTER,
            left_indent=0,
        ),
        "body": BlockStyle(
            font=ParagraphBlockStyles.Body.FONT,
            size=ParagraphBlockStyles.Body.SIZE,
            color=ParagraphBlockStyles.Body.COLOR,
            alignment=ParagraphBlockStyles.Body.ALIGNMENT,
            line_spacing=ParagraphBlockStyles.Body.LINE_SPACING,
            space_after=ParagraphBlockStyles.Body.SPACE_AFTER,
        ),
        "no_header_body": BlockStyle(
            font=ParagraphBlockStyles.Body.FONT,
            size=ParagraphBlockStyles.Body.SIZE,
            color=ParagraphBlockStyles.Body.COLOR,
            alignment=ParagraphBlockStyles.Body.ALIGNMENT,
            line_spacing=ParagraphBlockStyles.Body.LINE_SPACING,
            space_after=ParagraphBlockStyles.Body.SPACE_AFTER,
            left_indent=0,
        ),
    }

    def __init__(self):
        """Initialize the ParagraphBlock with default styles."""
        self.stylesheet = self._create_stylesheet()

    def _create_stylesheet(self) -> StyleSheet1:
        """Create a StyleSheet with all paragraph styles."""
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
                    wordWrap=ParagraphBlockStyles.Header.WORD_WRAP,
                    leftIndent=ParagraphBlockStyles.INDENT_LEVELS[0]
                    if name == "body"
                    else 0,
                    firstLineIndent=ParagraphBlockStyles.Body.FIRST_LINE_INDENT
                    if name == "body"
                    else 0,
                    allowWidows=0,
                    allowOrphans=0,
                )
            )

        return stylesheet

    def _create_paragraph(self, text: str, style_name: str) -> Paragraph:
        """Create a ReportLab Paragraph object with proper text handling.

        Args:
            text: Text content to format
            style_name: Name of the style to apply

        Returns:
            Paragraph: Formatted paragraph object
        """
        # Clean and normalize the text
        text = text if text else ""
        return Paragraph(text, self.stylesheet[style_name])

    def create_flowables(
        self,
        heading: Optional[str] = None,
        lines: Union[List[str], str] = None,
        name_designation_datetime_text: Optional[str] = None,
        header_style: Optional[BlockStyle] = None,
        body_style: Optional[BlockStyle] = None,
        heading_spacing: float = ParagraphBlockStyles.DEFAULT_HEADING_SPACING,
        paragraph_spacing: float = ParagraphBlockStyles.PARAGRAPH_SPACING[
            "DEFAULT"
        ],
    ) -> List[Flowable]:
        """Create a list of flowables for the paragraph block.

        Args:
            heading: Optional heading text
            lines: Text content as string or list of strings
            header_style: Optional custom style for header
            body_style: Optional custom style for body text
            heading_spacing: Space between heading and body text
            paragraph_spacing: Space between paragraphs

        Returns:
            List[Flowable]: List of flowable objects ready for document
        """
        try:
            flowables = []
            if name_designation_datetime_text:
                name_designation_datetime_para = self._create_paragraph(name_designation_datetime_text,\
                                                                        "header")
                flowables.append(name_designation_datetime_para)

                return flowables

            # Add header if present
            if heading:
                header_para = self._create_paragraph(heading, "header")
                flowables.append(header_para)
                flowables.append(Spacer(1, heading_spacing))

            style_name = "body"
            if not heading:
                style_name = "no_header_body"
            # Process and add main content
            if lines:
                if isinstance(lines, list):
                    for line in lines:
                        line = line if line else ""
                        body_para = self._create_paragraph(
                            str(line), style_name
                        )
                        flowables.append(body_para)
                        flowables.append(Spacer(1, paragraph_spacing))
                else:
                    body_para = self._create_paragraph(str(lines), style_name)
                    flowables.append(body_para)
                flowables.append(Spacer(1, paragraph_spacing))

            return flowables

        except Exception as e:
            logger.error(f"Error creating paragraph flowables: {str(e)}")
            raise
