from enum import Enum


class LogLevel(Enum):
    """
    Enum class describing logging level.

    Attributes:
        debug: int
            Represents debug logging level (10).
        info: int
            Represents info logging level (20).
        warning: int
            Represents warning logging level (30).
        error: int
            Represents error logging level (40).
        critical: int
            Represents critical logging level (50).
    """
    debug: int = 10
    info: int = 20
    warning: int = 30
    error: int = 40
    critical: int = 50


class LogFormat(Enum):
    """
    Enum class describing logging recording format.

    Attributes:
        json: str
            Represents the JSON logging recording format.
        string: str
            Represents the string logging recording format.
    """
    json: str = 'json'
    string: str = 'string'


class LogOutput(Enum):
    """
    Enum class describing logging output method.

    Attributes:
        file: str
            Represents the file logging output method.
        stream: str
            Represents the stream logging output method.
    """
    file: str = 'file'
    stream: str = 'stream'
