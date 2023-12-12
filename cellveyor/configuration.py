import logging
import logging.handlers
import sys
from typing import Any, Dict, List, Tuple, Union

from rich.logging import RichHandler
from rich.traceback import install

from cellveyor import constants


def configure_tracebacks() -> None:
    """Configure stack tracebacks arising from a crash to use rich."""
    install()


def configure_logging(
    debug_level: str = constants.logging.Default_Logging_Level,
    debug_dest: str = constants.logging.Default_Logging_Destination,
) -> Tuple[logging.Logger, bool]:
    """Configure standard Python logging package."""
    # use the specified logger with the specified destination
    # by dynamically constructing the function to call and then
    # invoking it with the provided debug_dest parameter
    debug_dest = debug_dest.lower()
    function_name = constants.logger.Function_Prefix + debug_dest
    configure_module = sys.modules[__name__]
    # it was possible to create the requested logger, so return it
    try:
        return (getattr(configure_module, function_name)(debug_level), True)
    # it was not possible to create the requested logger, so
    # return the default console logger as a safe alternative
    except AttributeError:
        return (configure_logging_console(debug_level), False)


def configure_logging_console(
    debug_level: str = constants.logging.Default_Logging_Level,
) -> logging.Logger:
    """Configure standard Python logging package to use rich."""
    # use the RichHandler to provide formatted
    # debugging output in the console
    logging.basicConfig(
        level=debug_level,
        format=constants.logging.Format,
        datefmt="[%X]",
        handlers=[RichHandler()],
    )
    # create a logger and then return it
    logger = logging.getLogger()
    return logger


def configure_logging_syslog(
    debug_level: str = constants.logging.Default_Logging_Level,
) -> logging.Logger:
    """Configure standard Python logging package to use syslog."""
    # use the SysLogHandler to send output to a localhost on a port
    syslog_handler = logging.handlers.SysLogHandler(
        address=(constants.server.Localhost, constants.server.Port)
    )
    logging.basicConfig(
        level=debug_level,
        format=constants.logging.Format,
        datefmt="[%X]",
        handlers=[syslog_handler],
    )
    # create a logger and then return it
    logger = logging.getLogger()
    return logger
