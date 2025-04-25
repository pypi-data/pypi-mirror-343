from cmd2 import RgbFg

from cliapp.config.base import BaseConfig, ConfigValue
from cliapp.util.defaults import PRIMARY_COLOR, SECONDARY_COLOR, TEXT_COLOR


def color(hex_value: str) -> RgbFg:
    """
    Converts a hexadecimal color string (e.g., "#RRGGBB") to an RgbFg object.

    Args:
        hex_value: The hexadecimal color string. Expected format is "#RRGGBB".

    Returns:
        An RgbFg object representing the color.
    """
    # Remove the '#' prefix if present
    value = hex_value.lstrip("#")
    
    # Convert hex pairs to integer RGB values
    r = int(value[0:2], 16)
    g = int(value[2:4], 16)
    b = int(value[4:6], 16)
    return RgbFg(r, g, b)

class ColorConfig(BaseConfig):
    """
    Configuration class for application colors.
    """
    # Define the expected types for the color attributes
    primary: RgbFg
    secondary: RgbFg
    text: RgbFg

    # Define the configuration values, their defaults, and the parsing function
    values = [
        ConfigValue("primary", PRIMARY_COLOR, color),
        ConfigValue("secondary", SECONDARY_COLOR, color),
        ConfigValue("text", TEXT_COLOR, color)
    ]