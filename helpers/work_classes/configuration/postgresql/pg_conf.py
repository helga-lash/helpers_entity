from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(slots=True)
class Connect:
    """
    Class describing connection to postgresql database settings

    Attributes:
        host: str
            IP address or DNS database host name
        port: int
            port on which the database
        user: str
            user to connect to the database
        password: str
            password for connecting to the database
    """
    host: str
    port: int
    user: str
    password: str


@dataclass_json
@dataclass(slots=True)
class PgConf:
    """
    Class describing postgresql database settings

    Attributes:
        name: str
            database name
        rw: Connect
            description of connecting to the database to record data
        ro: Connect
            description of connecting to the database for reading data
    """
    name: str
    rw: Connect
    ro: Connect
