import json
from typing import TypeVar, Generic, Callable, Any, Dict, Optional, List, Self

# Define a type variable for generic use
T = TypeVar('T')

class ConfigValue(Generic[T]):
    """
    Represents a single configuration value with a key, default value,
    and an optional initialization function.
    """
    def __init__(self, key: str, default: T, init: Callable[[T], Any] = lambda x: x):
        self.key = key
        self.default = default
        self.init = init

    def parse(self, data: Dict[str, T]) -> T:
        """
        Parses the value from a dictionary. Returns the default if the key is not found.
        Handles nested BaseConfig objects.
        """
        if self.key in data:
            rawValue = data[self.key]

            # If the default is a BaseConfig instance, recursively parse the nested data
            if isinstance(self.default, BaseConfig):
                return self.default.fromData(rawValue) # type: ignore # Assuming rawValue is a dict if default is BaseConfig

            return rawValue

        return self.default

class BaseConfig():
    """
    Base class for configuration objects. Defines how to load and parse configuration values.
    """
    # List of ConfigValue objects defining the configuration structure
    values: List[ConfigValue] = []

    @classmethod
    def fromPath(clx: Self, path: Optional[str]) -> Self:
        """
        Loads configuration from a JSON file at the given path.
        Returns a default instance if the path is None or loading fails.
        """
        if path is None:
            print("Warning: Configuration path not provided. Using default configuration.")
            return clx()

        try:
            with open(path, 'r') as f:
                data = json.load(f)
            return clx.fromData(data)
        except FileNotFoundError:
            print(f"Warning: Configuration file not found at {path}. Using default configuration.")
            return clx()
        except json.JSONDecodeError:
             print(f"Error: Could not decode JSON from {path}. Using default configuration.")
             return clx()
        except Exception as e:
            print(f"An unexpected error occurred while loading configuration from {path}: {e}")
            return clx()


    @classmethod
    def fromData(clx: Self, data: Dict[str, Any]) -> Self:
        """
        Creates a configuration instance from a dictionary of data.
        """
        # Parse each defined configuration value from the provided data
        config_data = { value.key : value.parse(data) for value in clx.values }
        
        # Create an instance of the config class with the parsed data
        return clx(**config_data)

    def __init__(self, **kwargs):
        """
        Initializes the configuration object with provided keyword arguments,
        applying initialization functions and using defaults where necessary.
        """
        for config_value_def in self.values:
            key = config_value_def.key
            
            # Get the raw value from kwargs or use the default
            rawValue = kwargs.get(key, config_value_def.default)
            
            # Apply the initialization function to the value
            value = config_value_def.init(rawValue)
            
            # Set the attribute on the instance
            setattr(self, key, value)