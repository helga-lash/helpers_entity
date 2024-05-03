from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional


@dataclass_json
@dataclass(slots=True)
class TgBotConf:
    """
    Class describing connection to telegram bot settings

    Attributes:
        token: str
            Token for telegram bot
        admins: list[str]
            (Optional) List of bot admin IDs
    """
    token: str
    admins: Optional[list[str]] = None
