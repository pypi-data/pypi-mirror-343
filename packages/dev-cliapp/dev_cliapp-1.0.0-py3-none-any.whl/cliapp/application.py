from typing import Optional, List, Callable, Any

# Third-party libraries
from cmd2 import CommandSet, categorize
from cmd2.constants import HELP_FUNC_PREFIX, COMMAND_FUNC_PREFIX

# Local/project imports
from cliapp.config import ApplicationConfig
from cliapp.interface import Interface
from cliapp.command import Command

class Application:
    """
    Main application class that loads configuration, initializes the interface,
    manages commands, and runs the command loop.
    """
    def __init__(self, config: Optional[str] = None):
        """
        Initializes the application.

        Args:
            config_path: Optional path to the application configuration file.
        """
        # Load application configuration from the specified path
        self.__config: ApplicationConfig = ApplicationConfig.fromPath(config)
        # Initialize the cmd2 interface with the loaded configuration
        self.__interface = Interface(self.__config)

        # List to hold Command objects
        self.commands: List[Command] = []

    def __setMethod(self, name: str, exec: Callable[..., Any]):
        """
        Helper method to dynamically set a method (do_* or help_*) on the interface.
        """
        # Set the callable as an attribute on the interface instance
        setattr(self.__interface, name, exec)
        # Categorize the method for help output
        
        # Retrieve the function just set (setattr doesn't return the object)
        func = getattr(self.__interface, name)
        categorize(func, f"{self.__config.shortname} Commands")

    def add(self, command: Command) -> None:
        """
        Adds a Command object to the application and registers its methods with the interface.

        Args:
            command: The Command instance to add.
        """
        self.commands.append(command)
        # Set the new command's methods
        exec = lambda statement: command.exec(self.__interface, statement)
        
        self.__setMethod(COMMAND_FUNC_PREFIX + command.name, exec)
        self.__setMethod(HELP_FUNC_PREFIX + command.name, command.help)

    def run(self) -> None:
        """
        Starts the command loop of the interface.
        """
        self.__interface.cmdloop()