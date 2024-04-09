from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional, Any


@dataclass_json
@dataclass(slots=True)
class ReturnEntity:
    """
    Class describing return entity

    Attributes:
        error: bool
            did the action end in error
        errorText: str
            (Optional) error text. Default None
        entity: Any
            (Optional) return entity. Default None

    Methods:
        error_text_append
    """
    error: bool
    errorText: Optional[str] = None
    entity: Optional[Any] = None

    def error_text_append(self, text: str) -> None:
        """
        Method that adds text to the error text
        Args:
            text: str, added text

        Returns: None
        """
        if self.errorText is None:
            self.errorText = text
        else:
            self.errorText += ' | ' + text
