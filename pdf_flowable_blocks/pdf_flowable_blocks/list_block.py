"""
List Block Module V2 for PDF Generation

This module provides functionality for rendering list-style text blocks
(ordered and unordered) using ReportLab's high-level components (Platypus).
"""

import logging
from dataclasses import dataclass
from typing import Any, List, Optional, Union

from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ListStyle, ParagraphStyle, StyleSheet1
from reportlab.platypus import ListFlowable, ListItem, Paragraph, Spacer

from pdf_letter_generator.commons.constants import (
    ListBlockStyles,
    PresentationType,
)

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
    alignment: str = TA_LEFT


class ListBlockV2:
    """Handles the creation and management of list text blocks using Platypus."""

    # Default styles for different block elements
    DEFAULT_STYLES = {
        "header": BlockStyle(
            font=ListBlockStyles.Header.FONT,
            size=ListBlockStyles.Header.SIZE,
            color=ListBlockStyles.Header.COLOR,
            alignment=ListBlockStyles.Header.ALIGNMENT,
            line_spacing=ListBlockStyles.Header.LINE_SPACING,
            space_after=ListBlockStyles.Header.SPACE_AFTER,
        ),
        "list": BlockStyle(
            font=ListBlockStyles.ListItem.FONT,
            size=ListBlockStyles.ListItem.SIZE,
            color=ListBlockStyles.ListItem.COLOR,
            alignment=ListBlockStyles.ListItem.ALIGNMENT,
            line_spacing=ListBlockStyles.ListItem.LINE_SPACING,
            space_after=ListBlockStyles.ListItem.SPACE_AFTER,
        ),
    }

    def __init__(self):
        """Initialize the ListBlock with default styles."""
        self.stylesheet = self._create_stylesheet()

    def _create_stylesheet(self) -> StyleSheet1:
        """Create a StyleSheet with all list styles."""
        stylesheet = StyleSheet1()

        # Add styles for header and list items
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
                    wordWrap=ListBlockStyles.Header.WORD_WRAP,
                    leftIndent=ListBlockStyles.INDENT_LEVELS[0]
                    if name == "list"
                    else 0,
                    firstLineIndent=ListBlockStyles.ListItem.FIRST_LINE_INDENT
                    if name == "list"
                    else 0,
                    allowWidows=0,
                    allowOrphans=0,
                )
            )

        # Add specific list styles for ordered and unordered lists
        stylesheet.add(
            ListStyle(
                "unordered",
                bulletFontName=ListBlockStyles.ListItem.BULLET_FONT,
                bulletFontSize=ListBlockStyles.ListItem.BULLET_SIZE,
                leftIndent=ListBlockStyles.ListItem.BULLET_INDENT,
                bulletDedent="auto",
                spaceBefore=0,
                spaceAfter=ListBlockStyles.LIST_ITEM_SPACING["DEFAULT"],
            )
        )

        stylesheet.add(
            ListStyle(
                "ordered",
                bulletFontName=ListBlockStyles.ListItem.BULLET_FONT,
                bulletFontSize=ListBlockStyles.ListItem.BULLET_SIZE,
                leftIndent=ListBlockStyles.ListItem.BULLET_INDENT,
                bulletDedent="auto",
                bulletFormat="%s.",
                spaceBefore=0,
                spaceAfter=ListBlockStyles.LIST_ITEM_SPACING["DEFAULT"],
            )
        )

        return stylesheet

    def _create_list_items(
        self, lines: List[str]
    ) -> List[ListItem]:
        """Create a list of ListItem flowables from text lines.

        Args:
            lines: List of text strings to convert to list items

        Returns:
            List[ListItem]: List of formatted list items
        """
        items = []
        for i, line in enumerate(lines, 1):
            para = Paragraph(line, self.stylesheet["list"])
            items.append(ListItem(para))
        return items

    def create_list_flowables(
        self,
        heading: Optional[str] = None,
        lines: Optional[List[str]] = None,
        presentation_type: PresentationType = PresentationType.UNORDERED_LIST.value,
        heading_spacing: float = ListBlockStyles.DEFAULT_HEADING_SPACING,
        item_spacing: float = ListBlockStyles.LIST_ITEM_SPACING["DEFAULT"],
    ) -> List[Union[Paragraph, Spacer, ListFlowable]]:
        """Create list block flowables.

        Args:
            heading: Optional heading text
            lines: List of text lines for list items
            presentation_type: Type of list (ordered_list or unordered_list)
            heading_spacing: Space between heading and list
            item_spacing: Space between list items

        Returns:
            List[Union[Paragraph, Spacer, ListFlowable]]: List of flowable objects
        """
        try:
            flowables = []
            lines = [line for line in lines if line]

            # Add header if present
            if heading:
                header_para = Paragraph(heading, self.stylesheet["header"])
                flowables.append(header_para)
                flowables.append(Spacer(1, heading_spacing))

            # Add list items if present
            if lines:
                is_ordered = (
                    presentation_type == PresentationType.ORDERED_LIST.value
                )
                list_items = self._create_list_items(lines)
                # Create list flowable (always use bullet type for consistent indentation)
                list_flowable = ListFlowable(
                    list_items,
                    bulletType="1" if is_ordered else "bullet",
                    style=self.stylesheet[
                        "ordered" if is_ordered else "unordered"
                    ],
                    bulletDedent="auto",
                    bulletFontName=ListBlockStyles.ListItem.BULLET_FONT,
                    bulletFontSize=ListBlockStyles.ListItem.BULLET_SIZE,
                    bulletIndent=ListBlockStyles.ListItem.BULLET_INDENT,
                    spaceBefore=0,
                    spaceAfter=item_spacing,
                )

                # Wrap in KeepTogether to prevent awkward breaks
                flowables.append(list_flowable)
                # flowables.append(Spacer(1, item_spacing))
            flowables.append(Spacer(1, 24))

            return flowables

        except Exception as e:
            logger.error(f"Error creating list flowables: {str(e)}")
            raise