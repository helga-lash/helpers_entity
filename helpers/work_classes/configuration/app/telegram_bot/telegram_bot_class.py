from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import Optional
from datetime import time
from pathlib import Path


@dataclass_json
@dataclass(slots=True)
class Contacts:
    """
    Class describing contact information.

    Attributes:
        phone : str, optional
        whatsapp : str, optional
        instagram : str, optional
        vk : str, optional
    """
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    instagram: Optional[str] = None
    vk: Optional[str] = None


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
        photoPath: Path, optional
            Path to the photo directory. Default is /tmp.
    """
    token: str
    recordTime: list[time] = field(metadata=config(encoder=lambda x: [str(i) for i in x]))
    admins: Optional[list[str]] = None
    recordMonth: int = 2
    photoPath: Path = field(metadata=config(encoder=str), default=Path('/tmp'))
    contacts: Contacts = field(default_factory=Contacts)
