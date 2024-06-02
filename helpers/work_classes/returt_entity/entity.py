from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional, Any


@dataclass_json
@dataclass(slots=True)
class ReturnEntity:
    """
    Class describing return entity.

    Attributes:
        error (bool): Indicates if the action ended in error.
        errorText (Optional[str]): Error text. Default is None.
        entity (Optional[Any]): Return entity. Default is None.

    Methods:
        error_text_append(self, text: str) -> None:
            Adds text to the error text.
    """
    error: bool
    errorText: Optional[str] = None
    entity: Optional[Any] = None

    def error_text_append(self, text: str) -> None:
        """
        Adds text to the error text.

        Args:
            text (str): Added text.

        Returns:
            None
        """
        if self.errorText is None:
            self.errorText = text
        else:
            self.errorText += ' | ' + text
