"""Define constants with dataclasses for use in cellveyor."""

from dataclasses import dataclass
from pathlib import Path


# Cellveyor constant
@dataclass(frozen=True)
class Cellveyor:
    """Define the Cellveyor dataclass for constant(s)."""

    Emoji: str
    Server_Shutdown: str
    Tagline: str
    Website: str


cellveyor = Cellveyor(
    Emoji=":dizzy:",
    Server_Shutdown=":person_shrugging: Shut down cellveyor's sylog server",
    Tagline="cellveyor: Analyze the AST of Python Source Code",
    Website=":link: GitHub: https://github.com/GatorEducator/cellveyor",
)


# logger constant
@dataclass(frozen=True)
class Logger:
    """Define the Logger dataclass for constant(s)."""

    Function_Prefix: str
    Richlog: str
    Syslog: str


logger = Logger(
    Function_Prefix="configure_logging_",
    Richlog="cellveyor-richlog",
    Syslog="cellveyor-syslog",
)


# logging constant
@dataclass(frozen=True)
class Logging:
    """Define the Logging dataclass for constant(s)."""

    Debug: str
    Info: str
    Warning: str
    Error: str
    Critical: str
    Console_Logging_Destination: str
    Syslog_Logging_Destination: str
    Default_Logging_Destination: str
    Default_Logging_Level: str
    Format: str
    Rich: str


logging = Logging(
    Debug="DEBUG",
    Info="INFO",
    Warning="WARNING",
    Error="ERROR",
    Critical="CRITICAL",
    Console_Logging_Destination="CONSOLE",
    Syslog_Logging_Destination="syslog",
    Default_Logging_Destination="console",
    Default_Logging_Level="ERROR",
    Format="%(message)s",
    Rich="Rich",
)


# markers constant
@dataclass(frozen=True)
class Markers:
    """Define the Markers dataclass for constant(s)."""

    Bad_Fifteen: str
    Bad_Zero_Zero: str
    Empty_String: str
    Indent: str
    Space: str


markers = Markers(
    Bad_Fifteen="<15>", Bad_Zero_Zero="", Empty_String="", Indent="   ", Space=" "
)


# output constant
@dataclass(frozen=True)
class Output:
    """Define the Output dataclass for constant(s)."""

    Syslog: str


output = Output(Syslog=":sparkles: Syslog server for receiving debugging information")


# server constant
@dataclass(frozen=True)
class Server:
    """Define the Server dataclass for constant(s)."""

    Backup_Count: int
    Localhost: str
    Log_File: str
    Max_Log_Size: int
    Poll_Interval: float
    Port: int
    Utf8_Encoding: str


server = Server(
    Backup_Count=1,
    Localhost="127.0.0.1",
    Log_File=".discover.log",
    Max_Log_Size=1048576,
    Poll_Interval=0.5,
    Port=2525,
    Utf8_Encoding="utf-8",
)
