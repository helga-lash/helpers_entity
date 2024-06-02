from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import Optional
from datetime import time


@dataclass_json
@dataclass(slots=True)
class TgBotConf:
    """
    Class describing connection to telegram bot settings.

    Attributes:
        token : str
            Token for telegram bot.
        recordTime : list[datetime.time], optional
            Recording time list. Default is empty list.
        admins : list[str], optional
            List of bot admin IDs. Default is None.
        recordMonth : int, optional
            Number of months available for recording. Default is 2.
    """
    token: str
    recordTime: list[time] = field(metadata=config(encoder=lambda x: [str(i) for i in x]))
    admins: Optional[list[str]] = None
    recordMonth: int = 2
