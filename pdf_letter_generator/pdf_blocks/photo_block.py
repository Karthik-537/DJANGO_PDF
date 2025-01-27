"""
Photo Block Module

This module handles the addition of photos to PDF documents with support for
grid layouts, captions, and proper scaling.
"""

from reportlab.lib import utils
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth

from plugins.interactors.dms.pdf_blocks.pdf_config import PDFConfig


class PhotoBlockValidator:
    """Validator for photo block data"""

    @staticmethod
    def validate(data):
        """
        Validate photo block data

        :param data: Dictionary containing photo data
        :raises ValueError: If required fields are missing or invalid
        """
        if "photos" not in data:
            raise ValueError("Photos data is required")

        photos = data["photos"]
        if not isinstance(photos, list):
            raise ValueError("Photos must be a list")

        for photo in photos:
            if "path" not in photo:
                raise ValueError("Each photo must have a path")
            if "caption" not in photo:
                raise ValueError("Each photo must have a caption")
            if not isinstance(photo["caption"], str):
                raise ValueError("Caption must be a string")


class PhotoBlock:
    """Handles the layout and rendering of photos in a grid format"""

    def __init__(self, canvas, layout_manager):
        """
        Initialize photo block

        :param canvas: ReportLab canvas object
        :param layout_manager: PDF Layout Manager instance
        """
        self.canvas = canvas
        self.layout_manager = layout_manager
        self.margin = PDFConfig.MARGIN
        self.photo_spacing = 0.5 * inch
        self.caption_height = 0.3 * inch

    def get_image_dimensions(self, image_path, desired_width):
        """
        Calculate image dimensions while maintaining aspect ratio

        :param image_path: Path to the image file
        :param desired_width: Desired width in points
        :return: tuple of (width, height) in points
        """
        img = utils.ImageReader(image_path)
        orig_width, orig_height = img.getSize()
        aspect = orig_height / float(orig_width)

        return desired_width, desired_width * aspect

    def add_photo_with_caption(self, x, y, photo_data, width):
        """
        Add a single photo with caption to the PDF

        :param x: X coordinate for photo placement
        :param y: Y coordinate for photo placement
        :param photo_data: Dictionary containing photo path and caption
        :param width: Desired width of the photo
        :return: Height of photo + caption
        """
        # Add photo
        img_width, img_height = self.get_image_dimensions(
            photo_data["path"], width
        )
        self.canvas.drawImage(
            photo_data["path"],
            x,
            y - img_height,
            width=img_width,
            height=img_height,
            preserveAspectRatio=True,
        )

        # Add caption
        caption = photo_data["caption"]
        caption_y = y - img_height - self.caption_height

        # Calculate caption width for wrapping
        available_width = width
        font_name = PDFConfig.FONTS["body"]["name"]
        font_size = PDFConfig.FONTS["body"]["size"]

        self.canvas.setFont(font_name, font_size)

        # Wrap caption if it's too long
        if stringWidth(caption, font_name, font_size) > available_width:
            words = caption.split()
            lines = []
            current_line = []

            for word in words:
                test_line = " ".join(current_line + [word])
                if (
                    stringWidth(test_line, font_name, font_size)
                    <= available_width
                ):
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(" ".join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)

            if current_line:
                lines.append(" ".join(current_line))

            for i, line in enumerate(lines):
                self.canvas.drawString(
                    x, caption_y + (len(lines) - i - 1) * font_size, line
                )
        else:
            self.canvas.drawString(x, caption_y, caption)

        return img_height + self.caption_height

    def add_photos_grid(self, data, photos_per_row=2):
        """
        Add photos in a grid layout

        :param data: Dictionary containing photos data
        :param photos_per_row: Number of photos per row
        :return: Total height used
        """
        PhotoBlockValidator.validate(data)

        # Calculate available width and photo width
        available_width = (
            PDFConfig.get_page_width()
            - 2 * self.margin
            - (photos_per_row - 1) * self.photo_spacing
        )
        photo_width = available_width / photos_per_row

        current_x = self.margin
        current_y = self.layout_manager.get_current_y()
        row_height = 0
        total_height = 0

        for i, photo in enumerate(data["photos"]):
            if i > 0 and i % photos_per_row == 0:
                # Move to next row
                current_x = self.margin
                current_y -= row_height + self.photo_spacing
                total_height += row_height + self.photo_spacing
                row_height = 0

            photo_height = self.add_photo_with_caption(
                current_x, current_y, photo, photo_width
            )
            row_height = max(row_height, photo_height)

            current_x += photo_width + self.photo_spacing

        total_height += row_height

        # Update layout manager's position
        self.layout_manager.move_cursor(total_height)

        return total_height


def add_photo_block(canvas, layout_manager, data):
    """
    Add a photo block to the PDF

    :param canvas: ReportLab canvas object
    :param layout_manager: PDF Layout Manager instance
    :param data: Dictionary containing photos data
    :return: Height of the added block
    """
    photo_block = PhotoBlock(canvas, layout_manager)
    return photo_block.add_photos_grid(data)
