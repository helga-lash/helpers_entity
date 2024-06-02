from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(slots=True)
class Connect:
    """
    Class describing connection to PostgreSQL database settings.

    Attributes:
        host : str
            IP address or DNS database host name.
        port : int
            Port on which the database is running.
        user : str
            User to connect to the database.
        password : str
            Password for connecting to the database.
        maxConn : int, optional
            Maximum number of open connections. Default is 5.
    """
    host: str
    port: int
    user: str
    password: str
    maxConn: int = 5


@dataclass_json
@dataclass(slots=True)
class PgConf:
    """
    Class describing PostgreSQL database settings.

    Attributes:
        name : str
            The name of the database.
        rw : Connect
            Description of the connection to the database for writing data.
        ro : Connect
            Description of the connection to the database for reading data.
    """
    name: str
    rw: Connect
    ro: Connect
