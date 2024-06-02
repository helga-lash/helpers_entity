from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Optional


@dataclass_json
@dataclass(slots=True)
class MinioClientConf:
    """
    A class representing a Minio client configuration.

    Attributes:
        host (str): The host address of the Minio server.
        accessKey (str): The access key for authentication.
        secretKey (str): The secret key for authentication.
        port (Optional[int]): The port number of the Minio server. Default is None.
        region (str): The region of the Minio server. Default is 'us-east-1'.
        secure (bool): Whether to use a secure connection. Default is False.
    """
    host: str
    accessKey: str
    secretKey: str
    port: Optional[int] = None
    region: str = 'us-east-1'
    secure: bool = False
