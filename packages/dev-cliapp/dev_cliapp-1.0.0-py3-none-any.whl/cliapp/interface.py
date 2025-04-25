import os
from functools import partial
from typing import Optional, List # Specific imports are preferred

from cmd2 import Cmd, style, DEFAULT_SHORTCUTS
from cmd2.table_creator import Column, SimpleTable
from cmd2.utils import align_center
# Assuming these are local/project imports
from cliapp.config import ApplicationConfig
from cliapp.util.tools import asciiArt


class Interface(Cmd):
    """
    Custom command-line interface inheriting from cmd2.Cmd.
    Manages the application's shell environment, prompts, banners, and command execution.
    """
    def __init__(self, config: ApplicationConfig):
        """
        Initializes the custom interface with application configuration.
        """
        # Copy default shortcuts and remove specific ones (@, @@)
        shortcuts = dict(DEFAULT_SHORTCUTS)
        shortcuts.pop("@")
        shortcuts.pop("@@")

        # Initialize cmd2.Cmd base class
        # auto_load_commands=False is set to manually manage commands if needed
        super().__init__(shortcuts=shortcuts, auto_load_commands=False)

        # Manually remove certain default cmd2 commands by deleting their do_* methods
        del Cmd.do_alias
        del Cmd.do_macro
        del Cmd.do_run_pyscript
        del Cmd.do_run_script
        del Cmd.do_set

        # Store the application configuration
        self.config = config

        # Configure cmd2 attributes using values from the config and helper methods
        self.intro = self.__introBanner()
        self.prompt = f"{style(self.config.shortname, fg=self.config.theme.color.primary)} {style(self.config.shell.prompt, fg=self.config.theme.color.text)}"
        self.editor = "code" # Default editor
        self.debug = True # Debug mode enabled
        self.continuation_prompt = "> "
        self.default_category = 'Default Commands'
        self.default_error = "Unknown command: {}."

    def poutput(self, msg: str = '', *, end: str = '\n') -> None:
        """
        Hook method to print output. Overrides cmd2's poutput to apply default text styling.
        """
        # Create a partial function for styling with the default text color
        style_text = partial(style, fg=self.config.theme.color.text)
        # Use cmd2's internal print_to method with the styled partial
        return self.print_to(self.stdout, msg, end=end, style=style_text)

    def __introBanner(self) -> str:
        """
        Generates the application's introductory banner.
        """
        # Generate ASCII art for the short name
        banner = asciiArt(self.config.shortname, self.config.theme.font)
        # Center and style the banner
        banner = align_center(banner)
        banner = style(banner, fg=self.config.theme.color.primary)

        # Create welcome messages
        title = f"Welcome to {self.config.fullname}!"
        subtitle = f"Version {self.config.version.string}. Created by {self.config.author}."
        message = "\n".join([title, subtitle]) + "\n"
        # Center and style the welcome messages
        message = align_center(message)
        message = style(message, fg=self.config.theme.color.text)

        # Style the shell intro message
        intro_msg = "\n" + style(self.config.shell.intro, fg=self.config.theme.color.secondary)

        # Combine all parts of the intro banner
        return "\n".join([banner, message, intro_msg])

    def __helpBanner(self) -> str:
        """
        Generates the header banner for the help output.
        """
        # Generate ASCII art for "Help"
        banner = asciiArt("Help", self.config.theme.font)
        # Center and style the help banner
        banner = align_center(banner)
        banner = style(banner, fg=self.config.theme.color.secondary)

        # Help message text
        message = "Documented commands (use 'help -v' for verbose/'help <topic>' for details)"
        # Center and style the help message
        message = align_center(message)
        message = style(message, fg=self.config.theme.color.text)

        # Combine banner and message for the help header
        return "\n".join([banner, message])

    def do_quit(self, statement: str) -> bool:
        """Exit this application"""
        print() # Print a blank line before the outro
        # Style and print the outro message
        outro = style(self.config.shell.outro, fg=self.config.theme.color.secondary)
        print(outro)
        # Call the superclass do_quit to handle the actual exit
        return super().do_quit(statement)

    def do_exit(self, statement: str) -> bool:
        """Exit this application"""
        # Simply delegate to do_quit
        return self.do_quit(statement)

    def do_clear(self, _: str) -> None:
        'Clear the terminal screen'
        # WARNING: os.system('clear') is Unix-specific.
        # Consider cross-platform alternatives (e.g., 'cls' on Windows, libraries like colorama).
        os.system('clear')

    def do_help(self, statement: str) -> None:
        """
        Displays help for commands.
        Overrides cmd2's do_help to set a custom help banner.
        """
        # Set the custom help banner before calling the superclass help method
        self.doc_header = self.__helpBanner()
        # Call the base class do_help to handle parsing and displaying help
        super().do_help(statement)
    
    #
    # Manipulate the help-menu table by overriding the original functionality
    #
            
    def print_topics(self, header: str, cmds: Optional[List[str]], _: int, maxcol: int) -> None:
        """
        Print groups of commands and topics in columns and an optional header
        Override of cmd's print_topics() to handle headers with newlines, ANSI style sequences, and wide characters

        :param header: string to print above commands being printed
        :param cmds: list of topics to print
        :param cmdlen: unused, even by cmd's version
        :param maxcol: max number of display columns to fit into
        """
        from cmd2.utils import align_left
        from cliapp.util.tools import terminalWidth
        
        if cmds:
            header = style(header, fg=self.config.theme.color.secondary)
            self.poutput(header)
            if self.ruler:
                divider = align_left('', fill_char=self.ruler, width=terminalWidth())
                divider = style(divider, fg=self.config.theme.color.primary)
                self.poutput(divider)
            self.columnize(cmds, maxcol - 1)
            self.poutput()
        
    
    def _print_topics(self, header: str, cmds: List[str], verbose: bool) -> None:
        """Customized version of print_topics that can switch between verbose or traditional output"""
        import io
        from typing import TextIO, cast
        from contextlib import redirect_stdout
        from cmd2 import constants, ansi
        from cmd2.utils import strip_doc_annotations
        from cliapp.util.tools import terminalWidth

        if cmds:
            if not verbose:
                self.print_topics(header, cmds, 15, 80)
            else:
                # Find the widest command
                widest = max([ansi.style_aware_wcswidth(command) for command in cmds])
                
                column_spacing = 2
                name_column_width = max(widest, 20)
                desc_column_width = terminalWidth() - name_column_width - column_spacing

                # Define the table structure
                name_column = Column('', width=name_column_width)
                desc_column = Column('', width=desc_column_width)

                topic_table = SimpleTable([name_column, desc_column], column_spacing=column_spacing, divider_char=self.ruler)

                # Build the topic table
                table_str_buf = io.StringIO()
                if header:
                    header = style(header, fg=self.config.theme.color.secondary)
                    table_str_buf.write(header + "\n")

                divider = topic_table.generate_divider()
                divider = style(divider, fg=self.config.theme.color.primary)
                if divider:
                    table_str_buf.write(divider + "\n")

                # Try to get the documentation string for each command
                topics = self.get_help_topics()
                for command in cmds:
                    if (cmd_func := self.cmd_func(command)) is None:
                        continue

                    doc: Optional[str]

                    # If this is an argparse command, use its description.
                    if (cmd_parser := self._command_parsers.get(cmd_func)) is not None:
                        doc = cmd_parser.description

                    # Non-argparse commands can have help_functions for their documentation
                    elif command in topics:
                        help_func = getattr(self, constants.HELP_FUNC_PREFIX + command)
                        result = io.StringIO()

                        # try to redirect system stdout
                        with redirect_stdout(result):
                            # save our internal stdout
                            stdout_orig = self.stdout
                            try:
                                # redirect our internal stdout
                                self.stdout = cast(TextIO, result)
                                help_func()
                            finally:
                                # restore internal stdout
                                self.stdout = stdout_orig
                        doc = result.getvalue()

                    else:
                        doc = cmd_func.__doc__

                    # Attempt to locate the first documentation block
                    cmd_desc = strip_doc_annotations(doc) if doc else ''

                    # Add this command to the table
                    table_row = topic_table.generate_data_row([command, cmd_desc])
                    table_str_buf.write(table_row + '\n')

                self.poutput(table_str_buf.getvalue())
    