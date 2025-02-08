"""
Media Block Module for PDF Generation with S3 Support

This module provides functionality for rendering media (images) in a grid layout
using ReportLab's components. Images are arranged in rows of 2. Supports both S3 and HTTP URLs.
"""

import logging
import urllib.request
from dataclasses import dataclass
from io import BytesIO
from typing import List, Optional, Tuple, Union
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Image, Table, TableStyle, Spacer, Paragraph, ParagraphStyle
from reportlab.platypus.flowables import Flowable
from reportlab.lib.styles import StyleSheet1
from pdf_letter_generator.commons import ImageBlockStyles

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class MediaStyle:
    """Configuration for media block styling."""

    max_width: float = 3 * inch  # Maximum width for each image
    max_height: float = 2 * inch  # Maximum height for each image
    spacing: float = 0.25 * inch  # Spacing between images
    cell_padding: float = 0.1 * inch  # Padding inside table cells
    border_color: colors.Color = colors.white  # Border color for table cells
    border_width: float = 0  # Border width for table cells


@dataclass
class ImageDTO:
    url: str
    header: Optional[str] = None
    description: Optional[str] = None


class ImageBlock:
    """Handles the creation and management of media blocks in PDFs using Platypus."""

    def __init__(self, style: Optional[MediaStyle] = None):
        """Initialize the MediaBlock with styling configuration.

        Args:
            style: Optional custom style configuration
        """
        self.style = style or MediaStyle()
        self.stylesheet = self._create_stylesheet()
        self._s3_client = boto3.client("s3")

    def _create_stylesheet(self):

        stylesheet = StyleSheet1()

        stylesheet.add(
            ParagraphStyle(
                name="header",
                fontName=ImageBlockStyles.Header.font,
                fontSize=ImageBlockStyles.Header.size,
                textColor=ImageBlockStyles.Header.color,
                alignment=ImageBlockStyles.Header.alignment,
                leading=ImageBlockStyles.Header.size * ImageBlockStyles.Header.line_spacing
            )
        )

        stylesheet.add(
            ParagraphStyle(
                name="description",
                fontName=ImageBlockStyles.Description.font,
                fontSize=ImageBlockStyles.Description.size,
                textColor=ImageBlockStyles.Description.color,
                alignment=ImageBlockStyles.Description.alignment,
                leading=ImageBlockStyles.Description.size*ImageBlockStyles.Description.line_spacing
            )
        )

        return stylesheet

    def _parse_s3_url(self, url: str) -> Tuple[str, str]:
        """Parse S3 URL to extract bucket and key.

        Args:
            url: S3 URL (s3://bucket/key or https://bucket.s3.amazonaws.com/key)

        Returns:
            Tuple[str, str]: Bucket name and object key
        """
        parsed = urlparse(url)
        if parsed.scheme == "s3":
            # Handle s3:// URLs
            bucket = parsed.netloc
            key = parsed.path.lstrip("/")
        elif "s3.amazonaws.com" in parsed.netloc:
            # Handle https://bucket.s3.amazonaws.com/key URLs
            bucket = parsed.netloc.split(".")[0]
            key = parsed.path.lstrip("/")
        else:
            raise ValueError(f"Invalid S3 URL format: {url}")

        return bucket, key

    def _fetch_image(self, url: str) -> BytesIO:
        """Fetch image from URL (S3 or HTTP) and return as BytesIO object.

        Args:
            url: Image URL (S3 or HTTP)

        Returns:
            BytesIO: Image data

        Raises:
            Exception: If image fetch fails
        """
        try:
            if "s3://" in url or "s3.amazonaws.com" in url:
                # Handle S3 URLs with authentication
                bucket, key = self._parse_s3_url(url)
                response = self._s3_client.get_object(Bucket=bucket, Key=key)
                image_data = response["Body"].read()
            else:
                # Handle regular HTTP URLs
                with urllib.request.urlopen(url) as response:
                    image_data = response.read()

            return BytesIO(image_data)

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "Unknown")
            logger.error(f"S3 error fetching image {url}: {error_code}")
            raise
        except Exception as e:
            logger.error(f"Error fetching image from URL {url}: {str(e)}")
            raise

    def _create_image(self, url: str) -> Image:
        """Create a ReportLab Image object from URL with proper sizing.

        Args:
            url: Image URL (S3 or HTTP)

        Returns:
            Image: ReportLab Image object

        Raises:
            Exception: If image creation fails
        """
        try:
            # Get image data as BytesIO
            image_data = self._fetch_image(url)

            # Create Image directly from BytesIO
            img = Image(image_data)

            # Calculate aspect ratio and resize if needed
            aspect = img.imageWidth / img.imageHeight
            if img.imageWidth > self.style.max_width:
                img.drawWidth = self.style.max_width
                img.drawHeight = self.style.max_width / aspect
            if img.drawHeight > self.style.max_height:
                img.drawHeight = self.style.max_height
                img.drawWidth = self.style.max_height * aspect

            return img
        except Exception as e:
            logger.error(f"Error creating image object: {str(e)}")
            raise

    def _create_image_row(self, images: List[ImageDTO]) -> List[List[Union[Paragraph, Spacer, Image]]]:
        """Create a row of images from URLs.

        Args:
            images: list of imagedtos

        Returns:
            List[Image]: List of ReportLab Image objects
        """
        row_images = []
        for image in images[:2]:  # Limit to 2 images per row
            try:
                image_data = []
                if image.header:
                    image_data.append(Paragraph(image.header, style=self.stylesheet["header"]))
                else:
                    image_data.append(Spacer(1, 17))

                img = self._create_image(image.url)
                image_data.append(img)
                image_data.append(Spacer(1, 5))

                if image.description:
                    image_data.append(Paragraph(image.description, style=self.stylesheet["description"]))
                    image_data.append(Spacer(1, 5))

                row_images.append(image_data)
            except Exception as e:
                logger.error(f"Error creating image for row: {str(e)}")
                # Add a placeholder or empty cell instead of failing
                row_images.append("")

        # Pad row with empty cells if needed
        while len(row_images) < 2:
            row_images.append("")

        return row_images

    def create_flowables(self, image_dtos: List[ImageDTO]) -> List[Flowable]:
        """Create a list of flowables for the media block with 2-column layout.

        Args:
            image_dtos: List of imagedtos

        Returns:
            List[Flowable]: List of flowable objects ready for document

        Raises:
            Exception: If flowable creation fails
        """
        try:
            flowables = []

            # Process URLs in pairs to create rows
            for i in range(0, len(image_dtos), 2):
                images = image_dtos[i: i + 2]
                row_images = self._create_image_row(images)

                # Create table for the row with proper styling
                table = Table(
                    [row_images],
                    colWidths=[self.style.max_width + self.style.spacing] * 2
                )

                # Apply table styling
                table.setStyle(
                    TableStyle(
                        [
                            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ]
                    )
                )

                flowables.append(table)

            flowables.append(Spacer(1, 24))

            return flowables

        except Exception as e:
            logger.error(f"Error creating media flowables: {str(e)}")
            raise

    def get_image_dimensions(self, url: str) -> Tuple[float, float]:
        """Get the dimensions of an image after applying style constraints.
        Args:
            url: Image URL (S3 or HTTP)

        Returns:
            Tuple[float, float]: Width and height in points
        """
        try:
            img = self._create_image(url)
            return img.drawWidth, img.drawHeight
        except Exception as e:
            logger.error(f"Error getting image dimensions: {str(e)}")
            raise
