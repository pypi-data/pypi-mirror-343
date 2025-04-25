# CLI App

A simple framework for building command-line interface applications in Python.

## Overview

`cliapp` provides a structured way to create interactive command-line applications with support for configuration loading, command definition, and argument parsing. It leverages `cmd2` for the core interactive shell functionality and `argparse` for command argument handling.

The framework is centered around two key components:

1.  `Application`: The main class that initializes the application, loads configuration, manages commands, and runs the command loop.
2.  `Command`: A class representing a single command within the application, defining its executable function and arguments.

## Installation

Assuming `cliapp` is packaged correctly (e.g., with `setuptools` or `poetry`), you would typically install it using pip:

```bash
pip install cliapp
```

You will also need to install the dependencies used by the framework:

```bash
pip install cmd2 pyfiglet
```

If you plan to use the asynchronous execution features, you'll need an async-compatible environment (like `asyncio`, which is in the standard library).

## Usage

Here's a basic example demonstrating how to create a simple CLI application with a command:

```python
# main.py
from cliapp import Application, Command
import sys

# Define a simple command executable function
def exec(name="World", greeting="Hello"):
    """A command that greets the user."""
    print(f"{greeting}, {name}!")

# Define an async command executable function
async def async_exec(name="World", greeting="Hello"):
    """An async command example."""
    import asyncio
    await asyncio.sleep(2) # Simulate async work
    print(f"Asynchronous {greeting}, {name}!")


if __name__ == "__main__":
    # Create the application instance
    # Configuration path is optional, defaults will be used if None is passed
    # or if the file doesn't exist/fails to load.
    app = Application(config="./config.json")

    # Create Command instances
    command = Command("hello", executable=exec)
    # Add arguments to the command
    command.addOption(full="name", help="an individual's name", default="World")
    command.addOption(short="g", help="a greeting", default="Hello", required=False)

    async_command = Command("asynchello", executable=async_exec)
    async_command.addOption(full="name", help="an individual's name", default="World")
    async_command.addOption(short="g", help="a greeting", default="Hello", required=False)

    # Add commands to the application
    app.add(command)
    app.add(async_command)

    # Run the application command loop
    app.run()
```

Save the above as `main.py` and run it:

```bash
python main.py
```

You will see the intro banner and the command prompt. You can type `help` to see available commands:

```
>> help
```

And run your defined command:

```
>> greet --name Devin -g Hey
Hi, Devin!
>> asyncgreet --name Dev 
Asynchronous Hello, Dev!
```

## Configuration

The application uses a JSON configuration file. The structure is defined by the `ApplicationConfig` class and its nested configuration classes (`VersionConfig`, `ThemeConfig`, `ShellConfig`, `ColorConfig`).

-   The configuration file is in **JSON format**.
-   There is **no default location or name** for the configuration file.
-   You **must provide the path** to the configuration file when creating the `Application` instance using the `config_path` argument, like `Application(config_path="./path/to/your/config.json")`.
-   If no path is provided, or if the file cannot be loaded (e.g., `FileNotFoundError`, `JSONDecodeError`), the application will start with **default values** defined in the `cliapp.util.defaults` module.

Shown below is a sample `config.json` file:

```json
{
    "shortname": "MyApp",
    "fullname": "My Awesome Application",
    "author": "Devin Green",
    "version": {
        "major": 1,
        "minor": 1,
        "patch": 0
    },
    "theme": {
        "color": {
            "primary": "#00FF00",
            "secondary": "#FFFF00",
            "text": "#CCCCCC"
        },
        "font": "ansi_regular"
    },
    "shell": {
        "prompt": "$ ",
        "intro": "Ready to go!",
        "outro": "Goodbye!"
    }
}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome\! Please feel free to open an issue on the repository to discuss bugs or feature requests, or submit a pull request.