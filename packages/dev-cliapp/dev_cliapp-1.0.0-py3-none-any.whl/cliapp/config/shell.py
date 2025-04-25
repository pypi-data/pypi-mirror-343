from cliapp.config.base import BaseConfig, ConfigValue
from cliapp.util.defaults import PROMPT, INTRO, OUTRO


class ShellConfig(BaseConfig):
    """
    Configuration class for shell-related settings like prompt, intro, and outro messages.
    """
    # Define the expected string types for the shell attributes
    prompt: str
    intro: str
    outro: str

    # Define the configuration values, their defaults, and initialization functions
    values = [
        # 'prompt' value: defaults to PROMPT, ensures it ends with a space
        ConfigValue("prompt", PROMPT, lambda val: f"{val} " if isinstance(val, str) and not val.endswith(" ") else val),
        # 'intro' value: defaults to INTRO
        ConfigValue("intro", INTRO),
        # 'outro' value: defaults to OUTRO
        ConfigValue("outro", OUTRO)
    ]