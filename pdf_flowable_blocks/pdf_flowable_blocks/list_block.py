"""
List Block Module V2 for PDF Generation

This module provides functionality for rendering list-style text blocks
(ordered and unordered) using ReportLab's high-level components (Platypus).
"""

import logging
from dataclasses import dataclass
from typing import Any, List, Optional, Union, Dict

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
                    alignment=style.alignment,
                    wordWrap=ListBlockStyles.Header.WORD_WRAP,
                    # spaceAfter=style.size * style.space_after,
                    # leftIndent=ListBlockStyles.INDENT_LEVELS[0]
                    # if name == "list"
                    # else 0,
                    # firstLineIndent=ListBlockStyles.ListItem.FIRST_LINE_INDENT
                    # if name == "list"
                    # else 0,
                    # allowWidows=0,
                    # allowOrphans=0,
                )
            )

        # Add specific list styles for ordered and unordered lists
        stylesheet.add(
            ListStyle(
                "unordered",
                bulletFontName=ListBlockStyles.ListItem.BULLET_FONT,
                bulletFontSize=ListBlockStyles.ListItem.BULLET_SIZE,
                bulletColor=ListBlockStyles.ListItem.COLOR
            )
        )

        stylesheet.add(
            ListStyle(
                "ordered",
                bulletFontName=ListBlockStyles.ListItem.BULLET_FONT,
                bulletFontSize=ListBlockStyles.ListItem.BULLET_SIZE,
                bulletColor=ListBlockStyles.ListItem.COLOR,
                bulletFormat="%s."
            )
        )

        return stylesheet

    def _create_list_items(self, lines: Dict[str, Any], item_spacing: float) -> List[ListItem]:
        """Returns a list of properly formatted ListItem objects"""
        list_items = []

        for header, sublines in lines.items():
            para = Paragraph(header, self.stylesheet["list"])
            if isinstance(sublines, dict):
                presentation_type = sublines.get("presentation_type", "unordered_list")
                sublist_items = self._create_list_items(lines=sublines, item_spacing=item_spacing)
                is_ordered = (
                        presentation_type == PresentationType.ORDERED_LIST.value
                )
                sublist_flowable = ListFlowable(
                    sublist_items,
                    bulletType="1" if is_ordered else "bullet",
                    style=self.stylesheet["ordered" if is_ordered else "unordered"]
                )
                list_items.append(ListItem([para, Spacer(1, item_spacing), sublist_flowable]))
            elif header != "presentation_type":
                list_items.append(ListItem([para, Spacer(1, item_spacing)]))

        return list_items

    def create_list_flowables(
            self,
            heading: Optional[str] = None,
            lines: Optional[Dict[str, Any]] = None,
            heading_spacing: float = ListBlockStyles.DEFAULT_HEADING_SPACING,
            item_spacing: float = ListBlockStyles.LIST_ITEM_SPACING["DEFAULT"]
    ) -> List[Union[Paragraph, Spacer, ListFlowable]]:
        """Wraps the list items in a ListFlowable"""
        try:
            flowables = []
            if heading:
                header_para = Paragraph(heading, self.stylesheet["header"])
                flowables.append(header_para)
                flowables.append(Spacer(1, heading_spacing))

            if lines:
                presentation_type = lines.get("presentation_type", "unordered")

                list_items = self._create_list_items(lines=lines, item_spacing=item_spacing)  # Ensure proper list items
                is_ordered = (
                        presentation_type == PresentationType.ORDERED_LIST.value
                )

                list_flowable = ListFlowable(
                    list_items,
                    bulletType="1" if is_ordered else "bullet",
                    style=self.stylesheet["ordered" if is_ordered else "unordered"]
                )
                flowables.append(list_flowable)

            flowables.append(Spacer(1, 24))

            return flowables

        except Exception as e:
            logger.error(f"Error creating list flowables: {str(e)}")
            raise
