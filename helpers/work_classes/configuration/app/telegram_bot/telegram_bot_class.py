from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import Optional
from datetime import time


@dataclass_json
@dataclass(slots=True)
class TgBotConf:
    """
    Class describing connection to telegram bot settings

    Attributes:
        token: str
            Token for telegram bot
        recordTime: list[datetime.time]
            Recording time list
        admins: list[str]
            (Optional) List of bot admin IDs
    """
    token: str
    recordTime: list[time] = field(metadata=config(encoder=lambda x: [str(i) for i in x]))
    admins: Optional[list[str]] = None
