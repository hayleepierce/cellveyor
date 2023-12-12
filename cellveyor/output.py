"""Perform logging and/or console output."""
from typing import Any

from rich.console import Console

from cellveyor import constants, configuration, debug

# create a default console
console = Console()


def setup(
    debug_level: debug.DebugLevel, debug_destination: debug.DebugDestination
) -> None:
    """Perform the setup steps and return a Console for terminal-based display."""
    global logger
    # configure the use of rich for improved terminal output:
    # --> rich-based tracebacks to enable better debugging on program crash
    configuration.configure_tracebacks()
    # --> logging to keep track of key events during program execution;
    # pass in the actual values as strings instead of using class enums
    logger, _ = configuration.configure_logging(
        debug_level.value, debug_destination.value
    )


def print_header() -> None:
    """Display tool details in the header."""
    global console  # noqa: disable=PLW0603
    console.print()
    console.print(
        constants.cellveyor.Emoji
        + constants.markers.Space
        + constants.cellveyor.Tagline
    )
    console.print(constants.cellveyor.Website)


def print_server() -> None:
    """Display server details in the header."""
    global console  # noqa: disable=PLW0603
    console.print(constants.output.Syslog)
    console.print()


def print_diagnostics(verbose: bool, **configurations: Any) -> None:
    """Display all variables input to the function."""
    global console  # noqa: disable=PLW0603
    # display diagnostic information for each configuration keyword argument
    if verbose:
        console.print(":sparkles: Configured with these parameters:")
        # iterate through each of the configuration keyword arguments
        for configuration_current in configurations:
            # print the name and the value of the keyword argument
            console.print(
                f"{constants.markers.Indent}{configuration_current} = {configurations[configuration_current]}"
            )
