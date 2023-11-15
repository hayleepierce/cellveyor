from rich.console import Console

from cellveyor import constants

# create a default console
console = Console()


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
