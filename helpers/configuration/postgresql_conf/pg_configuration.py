import os

from pathlib import Path

from helpers.configuration.yaml_conf_file import read_yaml_conf
from helpers.configuration import logger
from helpers.work_classes.configuration.postgresql import PgConf
from helpers.work_classes import ReturnEntity
from helpers.configuration.help_functions import positive_int_check


def pg_conf(path: Path = None) -> ReturnEntity:
    """
    Method validating the connection configuration to the PostgreSQL database
    :param path: path to configuration file
    :return: helpers.work_classes.ReturnEntity
    """
    result: ReturnEntity = ReturnEntity(False)

    if path is not None:
        config_data: ReturnEntity = read_yaml_conf(path)
    else:
        config_data: ReturnEntity = read_yaml_conf()

    if (not config_data.error) and (config_data.entity.get('database') is not None):
        logger.debug("Database configuration read from configuration file")
        pg_dict: dict = config_data.entity.pop('database')
        if pg_dict.get('rw') is None:
            logger.debug("Database configuration rw connect not set in config file")
            pg_dict.update({'rw': {}})
        if pg_dict.get('ro') is None:
            logger.debug("Database configuration ro connect not set in config file")
            pg_dict.update({'ro': {}})
    else:
        logger.debug("Database configuration not set in config file")
        result.error_text_append(config_data.errorText)
        pg_dict: dict = dict({'rw': {}, 'ro': {}})

    for key, value in os.environ.items():
        match key:
            case 'DB_NAME':
                logger.debug("The database name is set from the environment variable")
                pg_dict.update(name=str(value))
            case 'DB_RW_HOST':
                logger.debug("The database host for writing data is set from an environment variable")
                pg_dict['rw'].update(host=str(value))
            case 'DB_RW_PORT':
                logger.debug("The database port for writing data is set from an environment variable")
                pg_dict['rw'].update(port=value)
            case 'DB_RW_USER':
                logger.debug("The database user for writing data is set from an environment variable")
                pg_dict['rw'].update(user=str(value))
            case 'DB_RW_PAS':
                logger.debug("The database password for writing data is set from an environment variable")
                pg_dict['rw'].update(password=str(value))
            case 'DB_RW_CON':
                logger.debug("The database maximum connection for writing data is set from an environment variable")
                pg_dict['rw'].update(maxConn=value)
            case 'DB_RO_HOST':
                logger.debug("The database host for reading data is set from an environment variable")
                pg_dict['ro'].update(host=str(value))
            case 'DB_RO_PORT':
                logger.debug("The database port for reading data is set from an environment variable")
                pg_dict['ro'].update(port=value)
            case 'DB_RO_USER':
                logger.debug("The database user for reading data is set from an environment variable")
                pg_dict['ro'].update(user=str(value))
            case 'DB_RO_PAS':
                logger.debug("The database password for reading data is set from an environment variable")
                pg_dict['ro'].update(password=str(value))
            case 'DB_RO_CON':
                logger.debug("The database maximum connection for reading data is set from an environment variable")
                pg_dict['ro'].update(maxConn=value)

    if pg_dict.get('name') is None:
        result.error = True
        result.error_text_append('Database name not configured')
    if pg_dict['rw'].get('host') is None:
        result.error = True
        result.error_text_append('The database connection host is not configured for writing and reading')
    if pg_dict['rw'].get('port') is None:
        result.error = True
        result.error_text_append('The port for connecting to the database for writing and reading is not configured')
    else:
        if positive_int_check(pg_dict['rw'].get('port')):
            logger.debug('The database connection port for writing and reading is positive integer and not zero')
            pg_dict['rw'].update(port=int(pg_dict['rw'].get('port')))
        else:
            logger.debug('The database connection port for writing and reading is negative or zero')
            result.error = True
            result.error_text_append('Port must be a positive integer')
    if pg_dict['rw'].get('maxConn') is not None:
        if positive_int_check(pg_dict['rw'].get('maxConn')):
            logger.debug('The maximum number of open connections for writing and reading'
                         ' is positive integer and not zero')
            pg_dict['rw'].update(maxConn=int(pg_dict['rw'].get('maxConn')))
        else:
            logger.debug('The maximum number of open connections must be a positive integer')
            pg_dict['rw'].pop('maxConn', None)
    if pg_dict['rw'].get('user') is None:
        result.error = True
        result.error_text_append('The user for connecting to the database for writing and reading is not configured')
    if pg_dict['rw'].get('password') is None:
        result.error = True
        result.error_text_append(
            'The password for connecting to the database for writing and reading is not configured'
        )

    if not result.error:
        if len(pg_dict['ro']) == 0:
            logger.warning('Connections to the database for reading are not configured')
            pg_dict.update(ro=pg_dict['rw'])
        if pg_dict['ro'].get('host') is None:
            logger.warning('The database connection host is not configured for reading')
            pg_dict['ro'].update(host=pg_dict['rw']['host'])
        if pg_dict['ro'].get('port') is None:
            logger.warning('The port for connecting to the database for reading is not configured')
            pg_dict['ro'].update(port=pg_dict['rw']['port'])
        else:
            if positive_int_check(pg_dict['ro'].get('port')):
                logger.debug('The read database connection port is positive integer and not zero')
                pg_dict['ro'].update(port=int(pg_dict['ro'].get('port')))
            else:
                logger.debug('The database connection port for reading is negative or zero')
                pg_dict['ro'].update(port=pg_dict['rw'].get('port'))
        if pg_dict['ro'].get('user') is None:
            logger.warning('The database connection user for reading is not configured')
            pg_dict['ro'].update(user=pg_dict['rw']['user'])
        if pg_dict['ro'].get('password') is None:
            logger.warning('The password for connecting to the database for reading is not configured')
            pg_dict['ro'].update(password=pg_dict['rw']['password'])
        if pg_dict['ro'].get('maxConn') is None:
            logger.warning('The maximum connections for connecting to the database for reading is not configured')
            pg_dict['ro'].update(maxConn=pg_dict['rw'].get('maxConn'))
        else:
            if positive_int_check(pg_dict['ro'].get('maxConn')):
                logger.debug('The maximum number of open connections for reading'
                             ' is positive integer and not zero')
                pg_dict['ro'].update(maxConn=int(pg_dict['ro'].get('maxConn')))
            else:
                logger.debug('The maximum number of open connections must be a positive integer')
                pg_dict['ro'].pop('maxConn', None)
        result.entity = PgConf.from_dict(pg_dict)
    else:
        logger.debug(result.errorText)

    del pg_dict
    return result


__all__ = 'pg_conf'
