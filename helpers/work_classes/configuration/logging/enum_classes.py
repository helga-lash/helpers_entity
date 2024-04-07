from enum import Enum


class LogLevel(Enum):
    """
    Enum class describing logging level

    Attributes:
        debug: int
            debug logging level (10)
        info: int
            info logging level (20)
        warning: int
            warning logging level (30)
        error: int
            error logging level (40)
        critical: int
            critical logging level (50)
    """
    debug: int = 10
    info: int = 20
    warning: int = 30
    error: int = 40
    critical: int = 50


class LogFormat(Enum):
    """
    Enum class describing logging recording format

    Attributes:
        json: str
            json logging recording format
        string: str
            string logging recording format
    """
    json: str = 'json'
    string: str = 'string'


class LogOutput(Enum):
    """
    Enum class describing logging output method

    Attributes:
        file: str
            file logging output method
        stream: str
            stream logging output method
    """
    file: str = 'file'
    stream: str = 'stream'
