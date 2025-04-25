from cliapp.config.base import BaseConfig, ConfigValue
from cliapp.util.defaults import MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION


class VersionConfig(BaseConfig):
    """
    Configuration class for the application's version number.
    """
    # Define the expected integer types for version components
    major: int
    minor: int
    patch: int

    # Define the configuration values, defaulting to the global VERSION constant
    values = [
        ConfigValue("major", MAJOR_VERSION),
        ConfigValue("minor", MINOR_VERSION),
        ConfigValue("patch", PATCH_VERSION)
    ]

    def __init__(self, **kwargs):
        """
        Initializes the VersionConfig instance and creates a formatted version string.
        """
        # Call the base class initializer to parse config values
        super().__init__(**kwargs)

        # Construct a formatted version string from the parsed components
        self.string = f"{self.major}.{self.minor}.{self.patch}"