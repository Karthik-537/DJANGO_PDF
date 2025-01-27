"""
Logo Handling Utility for PDF Generation with S3 Support
"""

import logging
from io import BytesIO
from typing import Any, Dict, Optional

import requests
from reportlab.lib.units import inch
from reportlab.platypus import Image

# Configure logging
logger = logging.getLogger(__name__)


class LogoHandler:
    """Manages logo loading and positioning for PDF documents."""

    @staticmethod
    def get_logo_from_s3(s3_url: str) -> Optional[BytesIO]:
        """
        Get logo data from S3 URL into memory buffer.

        :param s3_url: S3 URL of the logo
        :return: BytesIO object containing the image data or None
        """
        try:
            response = requests.get(s3_url, stream=True)
            response.raise_for_status()

            # Create in-memory buffer
            image_data = BytesIO(response.content)
            return image_data

        except Exception as e:
            logger.error(f"Error getting logo from S3: {e}")
            return None

    @staticmethod
    def load_logo(
        logo_source: str,
        max_width: float = 3 * inch,
        max_height: float = 0.75 * inch,
        is_url: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """
        Load and resize logo image while maintaining aspect ratio.

        :param logo_source: Path to the logo file or S3 URL
        :param max_width: Maximum allowed width
        :param max_height: Maximum allowed height
        :param is_url: Whether the logo_source is an S3 URL
        :return: Dictionary with logo details or None
        """
        try:
            if is_url:
                image_data = LogoHandler.get_logo_from_s3(logo_source)
                if not image_data:
                    return None
                # Load image directly from BytesIO
                logo = Image(image_data)
            else:
                # Load from local path
                logo = Image(logo_source)

            # Calculate scaling
            img_width = logo.imageWidth
            img_height = logo.imageHeight
            width_ratio = max_width / img_width
            height_ratio = max_height / img_height
            scale_ratio = min(width_ratio, height_ratio)

            # Set new dimensions
            logo.drawWidth = img_width * scale_ratio
            logo.drawHeight = img_height * scale_ratio

            return {
                "image": logo,
                "width": logo.drawWidth,
                "height": logo.drawHeight,
            }

        except Exception as e:
            logger.error(f"Error loading logo: {e}")
            return None

    def add_logo(
        self,
        canvas,
        logo_source: str,
        x: float,
        y: float,
        max_width: float = 1 * inch,
        max_height: float = 1 * inch,
        is_url: bool = True,
    ) -> float:
        """
        Add logo to the PDF canvas at the specified position.

        :param canvas: PDF canvas to draw on
        :param logo_source: Path to the logo file or S3 URL
        :param x: X-coordinate for logo placement
        :param y: Y-coordinate for logo placement
        :param max_width: Maximum allowed width
        :param max_height: Maximum allowed height
        :param is_url: Whether the logo_source is an S3 URL
        :return: Height of the added logo, or 0 if failed
        """
        logo_data = self.load_logo(logo_source, max_width, max_height, is_url)
        if not logo_data:
            return 0

        try:
            logo = logo_data["image"]
            # Draw the logo at the specified position
            logo.drawOn(canvas, x, y - logo_data["height"])
            return logo_data["height"]

        except Exception as e:
            logger.error(f"Error drawing logo: {e}")
            return 0
