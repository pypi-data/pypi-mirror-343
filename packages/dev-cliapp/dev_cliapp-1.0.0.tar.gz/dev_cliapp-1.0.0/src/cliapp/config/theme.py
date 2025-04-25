from cliapp.config.base import BaseConfig, ConfigValue
from cliapp.config.color import ColorConfig
from cliapp.util.defaults import FONT

class ThemeConfig(BaseConfig):
    """
    Configuration class for the application's theme settings,
    including colors and font.
    """
    # Define the expected types for the theme attributes
    color: ColorConfig
    font: str

    # Define the configuration values and their defaults
    values = [
        # 'color' value: defaults to a default ColorConfig instance
        ConfigValue("color", ColorConfig()),
        # 'font' value: defaults to the global FONT default
        ConfigValue("font", FONT)
    ]