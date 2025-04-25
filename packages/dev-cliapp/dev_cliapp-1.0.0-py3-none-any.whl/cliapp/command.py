import inspect
import shlex
from argparse import ArgumentParser, ArgumentError
from typing import Callable, Optional, Coroutine, Any, List, Dict, Type, Tuple
from cmd2 import Cmd, style

from cliapp.interface import Interface
from cliapp.util import synchronizer

class Command:
    """
    Represents a single command that can be executed within the CLI application.
    Includes argument parsing capabilities.
    """
    def __init__(self,
                 name: str,
                 executable: Callable[..., Any] | Coroutine[Any, Any, Any] = lambda *args, **kwargs: None,
                 needsInput: bool = False):
        """
        Initializes a Command instance.

        Args:
            name: The name of the command.
            executable: The function or async coroutine to execute when the command is called.
            needsInput: A boolean value indicating whether or not an input should be captured from the command line.
                        Defaults to a no-operation function.
        """
        self.name = name
        self.__executable = executable
        self.selections: Dict[str, Tuple[str, List[str]]] = dict()

        # Initialize an ArgumentParser for this command
        self.__parser = ArgumentParser(prog=name)
        
        # Add a default positional argument to capture command input
        if needsInput:
            self.__parser.add_argument(
                "input",
                nargs="+",  # Capture one or more positional arguments
                help=f"String input for the {name} command."
            )

        # Public methods for execution and help
        self.exec: Callable[[Cmd, str], None] = lambda *args: self.__exec(*args)
        self.help: Callable[[], None] = lambda: self.__parser.print_help()

    def __exec(self, app: Interface, statement: str) -> None:
        """
        Internal method to parse the statement and execute the command's executable.

        Args:
            statement: The raw input string from the command line.
        """
        try:
            # Split the input string into arguments respecting quotes
            argv = shlex.split(statement)
            # Parse arguments using the internal parser
            args = self.__parser.parse_args(argv)
            
            # Convert parsed arguments (excluding 'input') to keyword arguments
            kwargs = vars(args)
            input_args = kwargs.pop('input', [])
            
            # Iterate over provided selections/options
            for name, value in self.selections.items():
                description, options = value
                
                # Express the amount of options as a string
                range = "a number"
                if len(options) == 2: range = "1 or 2"
                elif len(options) > 2: range += f" 1-{len(options)}"
                
                # Create a prompt for the user to input their selection
                message = f"Please enter {range} to select {description} "
                message = style(message, fg=app.config.theme.color.secondary)
                
                prompt = style(app.config.shell.prompt, fg=app.config.theme.color.text)
                prompt = message + prompt
                
                # Prompt the user to make the selection
                result = app.select(options, prompt)
                
                # Add the selection value to the keyword arguments
                kwargs[name] = result

            # Check if the executable is a coroutine and run it accordingly
            if inspect.iscoroutinefunction(self.__executable):
                # Use synchronizer.run for async executables
                synchronizer.run(self.__executable, *input_args, **kwargs)
            else:
                # Directly call synchronous executables
                self.__executable(*input_args, **kwargs)

        except SystemExit:
            # Catch SystemExit specifically, which is raised by parse_args() on error/help
            # Pass or handle as needed (parse_args with exit_on_error=False is an alternative)
            pass
        except Exception as e:
            # Catch other exceptions during execution or parsing (excluding SystemExit)
            print(f"Error executing command '{self.name}': {e}")
            # Consider logging the traceback for debugging
            # import traceback
            # traceback.print_exc()
            return

    def addFlag(self, 
                short: Optional[str] = None, 
                full: Optional[str] = None, 
                help: Optional[str] = None,
                required: bool = False) -> None:
        """
        Adds a boolean flag argument to the command's parser.

        Args:
            short: The short form of the flag (e.g., "v" for -v).
            full: The full form of the flag (e.g., "verbose" for --verbose).
                  If None, only the short form is added.
            help: The help string for the flag. Defaults to a generic description.
            required: If True, the option must be provided on the command line. Defaults to False.
            
        Raises:
            ValueError: If neither short nor full form is provided for the option.
        """
        # Provide a default help string if none is given
        if help is None: # Use 'is None' for checking None
            help_text = f'A flag labeled "-{short}"'
        else:
            help_text = help

        # Ensure name is provided
        if short is None and full is None:
            raise ValueError("A flag must have at least a short or a full form.")

        # Build the list of flags/names for argparse
        flags = []
        if short is not None:
            flags.append(f"-{short}")
        if full is not None:
            flags.append(f"--{full}")

        # Add the argument to the internal parser as a boolean flag
        self.__parser.add_argument(
            *flags, 
            action="store_true",
            required=required,
            help=help_text
        )
        
    def addOption(self,
                  short: Optional[str] = None,
                  full: Optional[str] = None,
                  help: Optional[str] = None,
                  type: Type = str,
                  default: Optional[Any] = None,
                  required: bool = False) -> None:
        """
        Adds an option argument that takes a value to the command's parser.
        An option must have at least a short or a full form.

        Args:
            short: The short form of the option (e.g., "o" for -o value).
            full: The full form of the option (e.g., "output" for --output value).
                  If None, only the short form is added.
            help: The help string for the option.
            type: The data type to convert the option value to (e.g., str, int, float). Defaults to str.
            default: The default value for the option if not provided on the command line.
            required: If True, the option must be provided on the command line. Defaults to False.

        Raises:
            ValueError: If neither short nor full form is provided for the option.
        """
        # Provide a default help string if none is given
        if help is None: # Use 'is None' for checking None
            help_text = f'A flag labeled "-{short}"'
        else:
            help_text = help

        # Ensure name is provided
        if short is None and full is None:
            raise ValueError("An option must have at least a short or a full form.")

        # Build the list of flags/names for argparse
        flags = []
        if short is not None:
            flags.append(f"-{short}")
        if full is not None:
            flags.append(f"--{full}")

        # Add the argument to the internal parser as an option that stores a value
        self.__parser.add_argument(
            *flags,
            type=type,
            default=default,
            required=required,
            help=help_text
        )
        
    def addSelection(self, 
                     name: str, 
                     options: List[str] = [], 
                     description: Optional[str] = None):
        """
        Provides a series of options for the user to select through after the arguments have been parsed.

        Args:
            name: The variable name to encapsulate the selection in for the command executable
            options: The list of options the user may select through.
            description: A description of the selection options to provide the user

        Raises:
            ValueError: If the list of options is empty.
        """
        if len(options) == 0:
            raise ValueError("You must provide at least one option to select from.")
        
        if description is None: description = "an option"
        self.selections[name] = (description, options)
        