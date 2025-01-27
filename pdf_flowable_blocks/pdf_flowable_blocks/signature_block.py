"""
Signature Block Module V2 for PDF Generation

This module provides functionality for adding signature blocks to PDFs
using ReportLab's high-level components.
"""

import logging
from typing import List, Optional

from commons.constants import PDFLineSpacing, PDFTextStyles
from commons.text_utils import sanitize
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.lib.units import inch
from reportlab.platypus import KeepTogether, Paragraph, Spacer

# Configure logging
logger = logging.getLogger(__name__)


class SignatureBlockV2:
    """Class to handle the creation and management of signature blocks in PDFs."""

    def __init__(self):
        """Initialize SignatureBlock with default styles."""
        self.stylesheet = self._create_stylesheet()

    def _create_stylesheet(self) -> StyleSheet1:
        """Create a StyleSheet with signature styles."""
        stylesheet = StyleSheet1()

        # Add signature style
        stylesheet.add(
            ParagraphStyle(
                "signature",
                fontName=PDFTextStyles.Body.FONT,
                fontSize=PDFTextStyles.Body.SIZE,
                textColor=PDFTextStyles.Body.COLOR,
                leading=PDFTextStyles.Body.SIZE * PDFLineSpacing.SINGLE,
                alignment=TA_RIGHT,
                spaceBefore=PDFLineSpacing.VERTICAL_SPACING * inch,
                spaceAfter=PDFLineSpacing.VERTICAL_SPACING * inch / 2,
            )
        )

        return stylesheet

    def create_signature_flowables(
        self, lines: List[str], style: Optional[ParagraphStyle] = None
    ) -> List[KeepTogether]:
        """Create signature block flowables.

        Args:
            lines: List of signature lines (name, designation, etc.)
            style: Optional custom style

        Returns:
            List[KeepTogether]: List of signature flowables
        """
        try:
            if not lines:
                logger.warning("No signature lines provided")
                return []

            flowables = []
            style = style or self.stylesheet["signature"]

            # Add signature lines
            for line in lines:
                para = Paragraph(sanitize(line), style)
                flowables.append(para)

            # Add spacing after signature
            flowables.append(Spacer(1, PDFLineSpacing.VERTICAL_SPACING * inch))

            # Keep all signature elements together
            return [KeepTogether(flowables)]

        except Exception as e:
            logger.error(f"Error creating signature flowables: {str(e)}")
            raise
