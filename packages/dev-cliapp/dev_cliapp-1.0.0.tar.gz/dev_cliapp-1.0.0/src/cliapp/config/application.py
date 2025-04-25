from cliapp.config.base import BaseConfig, ConfigValue
from cliapp.config.shell import ShellConfig
from cliapp.config.theme import ThemeConfig
from cliapp.config.version import VersionConfig
from cliapp.util.defaults import SHORTNAME, FULLNAME, AUTHOR


class ApplicationConfig(BaseConfig):
    """
    Root configuration class for the entire application.
    Composes various sub-configurations.
    """
    # Define the expected types for the application attributes, including nested configs
    shortname: str
    fullname: str
    author: str
    version: VersionConfig
    theme: ThemeConfig
    shell: ShellConfig

    # Define the configuration values and their defaults.
    # Nested configs use default instances of their respective classes.
    values = [
        ConfigValue("shortname", SHORTNAME),
        ConfigValue("fullname", FULLNAME),
        ConfigValue("author", AUTHOR),
        ConfigValue("version", VersionConfig()),
        ConfigValue("theme", ThemeConfig()),
        ConfigValue("shell", ShellConfig()),
    ]