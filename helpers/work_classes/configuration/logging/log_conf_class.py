from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import Optional
from pathlib import Path

from helpers.work_classes.configuration.logging.enum_classes import LogLevel, LogFormat, LogOutput


@dataclass_json
@dataclass(slots=True)
class LogConf:
    """
    Class describing logging settings.

    Attributes:
        level: LogLevel
            Logging level. Can take values: debug, info, warning, error, critical. Default: info
        format: LogFormat
            Logging recording format. Can take values: json, string. Default: string
        output: LogOutput
            Logging output. Can take values: stream, file. Default: stream
        path: Optional[Path]
            Logging file path. Used when the output accepts the value file. Default: "/log/app.log"
    """
    level: LogLevel = field(default=LogLevel.info, metadata=config(encoder=lambda x: x.value,
                                                                   decoder=lambda x: LogLevel[x]))
    format: LogFormat = field(default=LogFormat.string, metadata=config(encoder=lambda x: x.value, decoder=LogFormat))
    output: LogOutput = field(default=LogOutput.stream, metadata=config(encoder=lambda x: x.value, decoder=LogOutput))
    path: Optional[Path] = field(default=Path('/log/app.log'),
                                 metadata=config(encoder=str, decoder=lambda x: Path(x)))
