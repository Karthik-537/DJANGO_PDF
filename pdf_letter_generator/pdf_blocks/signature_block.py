"""
Signature Block Module for PDF Generation

This module provides functionality for rendering signature blocks
with consistent formatting and validation.
"""

import logging
import urllib.request
from dataclasses import dataclass
from io import BytesIO
from typing import Any, List, Optional

from PIL import Image
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image as RLImage
from reportlab.platypus import Paragraph, Spacer
from reportlab.platypus.flowables import Flowable

from plugins.interactors.dms.pdf_blocks.pdf_config import PDFConfig
from plugins.pdf_letter_generator.commons import PDFLineSpacing
from plugins.pdf_letter_generator.commons.constants import REGULAR_FONT

logger = logging.getLogger(__name__)


@dataclass
class BlockStyle:
    """Configuration for signature block styling."""

    font: str
    size: float
    color: Any
    line_spacing: float = PDFLineSpacing.SINGLE
    space_after: float = 0.25
    alignment: str = TA_LEFT


class SignatureBlock:
    """Handles the creation and management of signature blocks in PDFs."""

    # Default styles for different block elements
    DEFAULT_STYLES = {
        "body": BlockStyle(
            font=REGULAR_FONT,
            size=10,
            color=black,
            line_spacing=PDFLineSpacing.COMPACT,
            space_after=0.25,
        )
    }

    def __init__(self):
        """Initialize the SignatureBlock with default styles."""
        self._styles = self.DEFAULT_STYLES
        self._paragraph_style = ParagraphStyle(
            "SignatureStyle",
            fontName=self._styles["body"].font,
            fontSize=self._styles["body"].size,
            leading=self._styles["body"].size
            * self._styles["body"].line_spacing,
            textColor=self._styles["body"].color,
            alignment=self._styles["body"].alignment,
        )

    def add_block(
        self,
        canvas,
        lines: List[str],
        layout,
        signature_image_url: Optional[str] = None,
    ) -> float:
        """
        Add a signature block to the PDF.

        Args:
            canvas: PDF canvas to draw on
            lines: List of strings to be displayed in the signature block
            layout: Layout manager for positioning
            signature_image_url: Optional URL of the signature image

        Returns:
            float: Height of the added block
        """
        if not lines:
            logger.warning("No lines provided for signature block")
            return 0

        # Calculate margins and dimensions
        page_width = PDFConfig.get_page_width()
        page_height = PDFConfig.get_page_height()
        signature_x = (
            PDFConfig.MARGIN + (page_width - 2 * PDFConfig.MARGIN) * 0.7
        )

        # Define signature image dimensions
        signature_width = 2 * inch
        signature_height = 0.75 * inch
        spacing_after_signature = 12  # points

        # Calculate text height
        paragraphs = []
        for line in lines:
            para = Paragraph(line, self._paragraph_style)
            paragraphs.append(para)
            paragraphs.append(Spacer(1, self._styles["body"].size * 0.5))

        text_height = sum(
            p.wrap(page_width - signature_x - PDFConfig.MARGIN, page_height)[1]
            for p in paragraphs
            if isinstance(p, Flowable)
        )

        # Total height calculation
        total_height = (
            signature_height
            + spacing_after_signature
            + text_height
            + 0.3 * inch
        )

        # Check if we need to start on a new page
        if layout.current_y - total_height < PDFConfig.MARGIN:
            canvas.showPage()
            layout.current_y = page_height - PDFConfig.MARGIN

        # Calculate initial Y position
        initial_y = layout.current_y
        layout.current_y = initial_y

        # Handle signature image or draw box
        if signature_image_url:
            signature_img = self._fetch_and_resize_image(
                signature_image_url, signature_width, signature_height
            )
            if signature_img:
                signature_img.drawOn(
                    canvas, signature_x, layout.current_y - signature_height
                )
            else:
                # Fallback to empty box if image fails
                canvas.saveState()
                canvas.setStrokeColor(black)
                canvas.setLineWidth(0.1)
                canvas.rect(
                    signature_x,
                    layout.current_y - signature_height,
                    signature_width,
                    signature_height,
                )
                canvas.restoreState()
        else:
            # Draw empty signature box
            canvas.saveState()
            canvas.setStrokeColor(black)
            canvas.setLineWidth(0.1)
            canvas.rect(
                signature_x,
                layout.current_y - signature_height,
                signature_width,
                signature_height,
            )
            canvas.restoreState()

        # Update Y position after signature
        layout.current_y -= signature_height + spacing_after_signature

        # Draw all paragraphs
        for para in paragraphs:
            if isinstance(para, Paragraph):
                w, h = para.wrap(
                    page_width - signature_x - PDFConfig.MARGIN, page_height
                )
                para.drawOn(canvas, signature_x, layout.current_y - h)
                layout.current_y -= h
            else:  # Spacer
                layout.current_y -= para.height

        # Add final spacing
        layout.current_y -= 0.3 * inch

        return initial_y - layout.current_y

    @staticmethod
    def _fetch_and_resize_image(
        image_url: str, max_width: float, max_height: float
    ) -> RLImage:
        """
        Fetch image from URL and resize it to fit within specified dimensions.

        Args:
            image_url: URL of the signature image
            max_width: Maximum width in points
            max_height: Maximum height in points

        Returns:
            RLImage: ReportLab Image object ready to be drawn
        """
        try:
            # Fetch image from URL
            with urllib.request.urlopen(image_url) as response:
                img_data = response.read()

            # Open image with PIL
            img = Image.open(BytesIO(img_data))

            # Calculate aspect ratio and new dimensions
            aspect = img.width / img.height
            if aspect > max_width / max_height:
                new_width = max_width
                new_height = max_width / aspect
            else:
                new_height = max_height
                new_width = max_height * aspect

            # Create ReportLab image
            rl_img = RLImage(
                BytesIO(img_data), width=new_width, height=new_height
            )
            return rl_img

        except Exception as e:
            logger.error(f"Error processing signature image: {str(e)}")
            return None
