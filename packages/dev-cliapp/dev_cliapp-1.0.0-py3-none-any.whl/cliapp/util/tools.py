import os
from typing import Optional

from cmd2.ansi import strip_style
from pyfiglet import Figlet, FigletError


def terminalWidth() -> int:
    """
    Gets the current width of the terminal in columns.

    Returns:
        The terminal width as an integer. Returns a default (e.g., 80)
        if the terminal size cannot be determined.
    """
    try:
        # Use os.get_terminal_size() to get terminal dimensions
        return os.get_terminal_size().columns
    except OSError:
        # Handle cases where terminal size cannot be determined (e.g., not in a TTY)
        return 80


def asciiArt(value: str, font: str, width: Optional[int] = None) -> str:
    """
    Generates ASCII art for a given string value using a specified font.
    Adds leading/trailing newlines and removes blank lines from the output.

    Args:
        value: The string to render as ASCII art.
        font: The name of the pyfiglet font to use.
        width: The terminal width for rendering. Defaults to the actual terminal width.

    Returns:
        A string containing the formatted ASCII art.
    """
    # Use actual terminal width if no width is provided
    render_width = width if width is not None else terminalWidth()

    try:
        # Initialize Figlet with the specified font and width
        figlet = Figlet(font=font, width=render_width)
        # Render the text
        render = figlet.renderText(value)
    except FigletError as e:
        # Handle potential errors during figlet rendering (e.g., invalid font)
        print(f"Warning: Could not render ASCII art with font '{font}': {e}")
        return f"\n{value}\n\n" # Return the original value with newlines as a fallback

    lines = render.splitlines()

    # Remove leading blank lines (after stripping potential ANSI styles)
    while lines and not strip_style(lines[0]).strip():
        lines.pop(0)

    # Remove trailing blank lines (after stripping potential ANSI styles)
    while lines and not strip_style(lines[-1]).strip():
        lines.pop()

    NEW_LINE = "\n"
    # Join the remaining lines and add leading/trailing newlines for spacing
    return NEW_LINE + NEW_LINE.join(lines) + NEW_LINE * 2