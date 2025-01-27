"""
Text utility functions for common text processing tasks.
"""

from textwrap import wrap

from reportlab.pdfbase.pdfmetrics import stringWidth


def sanitize(text: str) -> str:
    """
    Sanitize text content, with specific handling for Rupee symbol.

    Args:
        text (str): Input text to sanitize

    Returns:
        str: Sanitized text
    """
    # Ensure consistent Rupee symbol representation
    if "₹" in text:
        # Replace with standard 'Rs.' and ensure proper spacing
        text = (
            text.replace("₹", "Rs.")
            .replace("Rs.", "Rs. ")
            .replace("Rs.  ", "Rs. ")
        )

    # Strip leading and trailing whitespace
    return text.strip()


def wrap_text_to_width(
    text: str, width: float, font_name: str, font_size: int
) -> list:
    """
    Wrap text to fit within a specified width using the given font settings.

    Args:
        text (str): Text to wrap
        width (float): Maximum width in points
        font_name (str): Font name
        font_size (int): Font size in points

    Returns:
        list: List of wrapped text lines
    """
    if not text:
        return []

    # First try wrapping at word boundaries
    lines = wrap(text, width=max(1, int(width / (font_size * 0.5))))

    # If any line is still too wide, force wrap at character level
    final_lines = []
    for line in lines:
        while stringWidth(line, font_name, font_size) > width:
            # Find the maximum number of characters that can fit
            for i in range(len(line), 0, -1):
                if stringWidth(line[:i], font_name, font_size) <= width:
                    final_lines.append(line[:i])
                    line = line[i:]
                    break
        if line:
            final_lines.append(line)

    return final_lines
