from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional

from helpers.work_classes.configuration.app.telegram_bot import TgBotConf


@dataclass_json
@dataclass(slots=True)
class AppConf:
    """
    Class describing application settings

    Attributes:
        tgBot: helpers.work_classes.configuration.app.telegram_bot.TgBotConf
            (Optional) Telegram bot configuration
    """
    tgBot: Optional[TgBotConf] = None
