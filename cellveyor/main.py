"""🚚 Cellveyor is a conveyor for the cells in spreadsheets."""

from pathlib import Path
from typing import Dict, List

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from cellveyor import (
    constants,
    data,
    debug,
    filesystem,
    report,
    transfer,
    output,
    server,
)

# create a Typer object to support the command-line interface
cli = typer.Typer(no_args_is_help=True)

# create a default console
console = Console()


def display_reports(reports_dict: Dict[str, str]) -> None:
    """Display all of the reports in the reports dictionary."""
    # iterate through all of the keys
    for current_report_key in reports_dict.keys():
        # extract the report for the current key
        current_report = reports_dict[current_report_key]
        # display the report inside of a rich panel, using
        # a markdown-based formatter for the report's contents
        console.print(
            f"{constants.markers.Indent} {Panel(Markdown(current_report), title='Report', expand=False)} {constants.markers.Newline}"
        )
        console.print()


def output_preamble(
    verbose: bool,
    debug_level: debug.DebugLevel = debug.DebugLevel.ERROR,
    debug_destination: debug.DebugDestination = debug.DebugDestination.CONSOLE,
    **kwargs,
) -> None:
    """Output all of the preamble content."""
    # setup the console and the logger through the output module
    output.setup(debug_level, debug_destination)
    output.logger.debug(f"Display verbose output? {verbose}")
    output.logger.debug(f"Debug level? {debug_level.value}")
    output.logger.debug(f"Debug destination? {debug_destination.value}")
    # display the header
    output.print_header()
    # display details about configuration as
    # long as verbose output was requested;
    # note that passing **kwargs to this function
    # will pass along all of the extra keyword
    # arguments that were input to the function
    output.print_diagnostics(
        verbose,
        debug_level=debug_level.value,
        debug_destination=debug_destination.value,
        **kwargs,
    )


@cli.command()
def transport(  # noqa: PLR0913
    spreadsheet_directory: Path = typer.Option(
        ...,
        "--spreadsheet-directory",
        "-d",
        help="Directory with spreadsheet file(s).",
    ),
    spreadsheet_file: Path = typer.Option(
        ...,
        "--spreadsheet-file",
        "-f",
        help="Spreadsheet file in the specified directory.",
    ),
    sheet_name: str = typer.Option(
        ...,
        "--sheet-name",
        "-s",
        help="Name of specific sheet in spreadsheet file",
    ),
    key_attribute: str = typer.Option(
        ...,
        "--key-attribute",
        "-a",
        help="Name of key attribute in specific sheet of spreadsheet file",
    ),
    column_regexp: str = typer.Option(
        ...,
        "--column-regexp",
        "-c",
        help="Regular expression for matching columns in specific sheet",
    ),
    feedback_regexp: str = typer.Option(
        ...,
        "--feedback-regexp",
        "-f",
        help="Regular expression for matching feedback columns in specific sheet",
    ),
    key_value: str = typer.Option(
        None,
        "--key-value",
        "-v",
        help="Value of key attribute in specific sheet of spreadsheet file",
    ),
    feedback_file: List[Path] = typer.Option(
        None,
        "--feedback-file",
        "-f",
        help="Feedback file(s) in JSON format",
    ),
    github_token: str = typer.Option(
        None,
        "--github-token",
        "-g",
        help="GitHub authorization token",
    ),
    github_organization: str = typer.Option(
        None,
        "--github-organization",
        "-o",
        help="GitHub organization that stores all matching repositories ",
    ),
    github_repository_prefix: str = typer.Option(
        None,
        "--github-repository-prefix",
        "-p",
        help="Prefix for all GitHub repositories used as a destination",
    ),
    transfer_report: bool = typer.Option(
        False,
        help="Transfer a report to GitHub",
    ),
    debug_level: debug.DebugLevel = typer.Option(
        debug.DebugLevel.ERROR.value,
        "--debug-level",
        "-l",
        help="Specify the level of debugging output.",
    ),
    debug_destination: debug.DebugDestination = typer.Option(
        debug.DebugDestination.CONSOLE.value,
        "--debug-dest",
        "-t",
        help="Specify the destination for debugging output.",
    ),
    verbose: bool = typer.Option(False, help="Display verbose debugging output"),
) -> None:
    """Transport a specified spreadsheet."""
    if verbose:
        # output the preamble
        output_preamble(verbose, debug_level, debug_destination)
    # determine if the provided directory and file are valid
    if not filesystem.confirm_valid_file_in_directory(
        spreadsheet_file, spreadsheet_directory
    ):
        console.print(":person_shrugging: Unable to access file and/or directory")
    # access all of the sheets inside of the valid spreadsheet file
    fully_qualified_spreadsheet_file = spreadsheet_directory / spreadsheet_file
    console.print(f":delivery_truck: Accessing: {fully_qualified_spreadsheet_file}")
    # access all of the feedback files and combine them into a single
    # dictionary organized in the following fashion:
    # --> key: label like "header" or "footer" or a label
    #          that is found inside of a Google Sheet like "reassess"
    # --> value: the actual content that will be placed in the location of the final
    #            message in, for instance, the header or the footer or, alternatively,
    #            in the list of extra feedback
    combined_feedback_dict = filesystem.read_feedback_files(feedback_file)
    # access the dictionary of all of the dataframes in the speadsheet;
    # note that each sheet in the spreadsheet can be accessed by:
    # --> name of the sheet: str
    # --> dataframe of the sheet: pandas dataframe
    sheet_dataframe_dict = data.access_dataframes(fully_qualified_spreadsheet_file)
    # console.print(sheet_dataframe_dict.keys())
    # access the requested sheet within the spreadsheet
    sheet_dataframe = sheet_dataframe_dict[sheet_name]
    # access the data for:
    # --> the key attribute
    # --> the column(s) that match the regular expression
    selected_columns, result_df = data.key_attribute_column_filter(
        sheet_dataframe, key_attribute, column_regexp, key_value
    )
    # create a unique message for each row in the dataframe
    per_key_report = report.create_per_key_report(
        key_attribute,
        result_df,
        selected_columns,
        feedback_regexp,
        combined_feedback_dict,
    )
    # display the generated reports
    display_reports(per_key_report)
    # if the --transfer flag was enabled then this means
    # that the generated reports should be uploaded to GitHub
    # as a comment inside of the standard pull request
    if transfer_report:
        transfer.transfer_reports_to_github(
            github_token, github_organization, github_repository_prefix, per_key_report
        )


@cli.command()
def log() -> None:
    """🦚 Start the logging server."""
    # display the header
    output.print_header()
    # display details about the server
    output.print_server()
    # run the server; note that this
    # syslog server receives debugging
    # information from cellveyor.
    # It must be started in a separate process
    # before running any sub-command
    # of the cellveyor tool
    server.start_syslog_server()
