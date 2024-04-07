import os

from pathlib import PosixPath

from helpers.configuration.yaml_conf_file import read_yaml_conf
from helpers.configuration import logger
from helpers.work_classes.configuration.postgresql import PgConf
from helpers.work_classes import ReturnEntity


def pg_conf(path: PosixPath = None) -> ReturnEntity:
    """
    Method validating the connection configuration to the PostgreSQL database
    :param path: path to configuration file
    :return: helpers.work_classes.ReturnEntity
    """
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
        pg_dict: dict = dict({'rw': {}, 'ro': {}})

    if os.environ.get('DB_NAME') is not None:
        logger.debug("The database name is set from the environment variable")
        pg_dict.update(name=str(os.environ.get('DB_NAME')))
    if os.environ.get('DB_RW_HOST') is not None:
        logger.debug("The database host for writing data is set from an environment variable")
        pg_dict['rw'].update(host=str(os.environ.get('DB_RW_HOST')))
    if os.environ.get('DB_RW_PORT') is not None:
        logger.debug("The database port for writing data is set from an environment variable")
        pg_dict['rw'].update(port=int(os.environ.get('DB_RW_PORT')))
    if os.environ.get('DB_RW_USER') is not None:
        logger.debug("The database user for writing data is set from an environment variable")
        pg_dict['rw'].update(user=str(os.environ.get('DB_RW_USER')))
    if os.environ.get('DB_RW_PAS') is not None:
        logger.debug("The database password for writing data is set from an environment variable")
        pg_dict['rw'].update(password=str(os.environ.get('DB_RW_PAS')))
    if os.environ.get('DB_RO_HOST') is not None:
        logger.debug("The database host for reading data is set from an environment variable")
        pg_dict['ro'].update(host=str(os.environ.get('DB_RO_HOST')))
    if os.environ.get('DB_RO_PORT') is not None:
        logger.debug("The database port for reading data is set from an environment variable")
        pg_dict['ro'].update(port=int(os.environ.get('DB_RO_PORT')))
    if os.environ.get('DB_RO_USER') is not None:
        logger.debug("The database user for reading data is set from an environment variable")
        pg_dict['ro'].update(user=str(os.environ.get('DB_RO_USER')))
    if os.environ.get('DB_RO_PAS') is not None:
        logger.debug("The database password for reading data is set from an environment variable")
        pg_dict['ro'].update(password=str(os.environ.get('DB_RO_PAS')))

    result: ReturnEntity = ReturnEntity(False)
    if pg_dict.get('name') is None:
        result.error = True
        result.errorText = 'Database name not configured'
    elif len(pg_dict['rw']) == 0:
        result.error = True
        result.errorText = 'The database connection section for writing and reading is not configured'
    elif pg_dict['rw'].get('host') is None:
        result.error = True
        result.errorText = 'The database connection host is not configured for writing and reading'
    elif pg_dict['rw'].get('port') is None:
        result.error = True
        result.errorText = 'The port for connecting to the database for writing and reading is not configured'
    elif pg_dict['rw'].get('user') is None:
        result.error = True
        result.errorText = 'The user for connecting to the database for writing and reading is not configured'
    elif pg_dict['rw'].get('password') is None:
        result.error = True
        result.errorText = 'The password for connecting to the database for writing and reading is not configured'
    else:
        if len(pg_dict['ro']) == 0:
            logger.debug('Connections to the database for reading are not configured')
            pg_dict.update(ro=pg_dict['rw'])

    if not result.error:
        if pg_dict['ro'].get('host') is None:
            logger.debug('The database connection host is not configured for reading')
            pg_dict['ro'].update(host=pg_dict['rw']['host'])
        if pg_dict['ro'].get('port') is None:
            logger.debug('The port for connecting to the database for reading is not configured')
            pg_dict['ro'].update(port=pg_dict['rw']['port'])
        if pg_dict['ro'].get('user') is None:
            logger.debug('The database connection user for reading is not configured')
            pg_dict['ro'].update(user=pg_dict['rw']['user'])
        if pg_dict['ro'].get('password') is None:
            logger.debug('The password for connecting to the database for reading is not configured')
            pg_dict['ro'].update(password=pg_dict['rw']['password'])
        result.entity = PgConf.from_dict(pg_dict)
    else:
        logger.debug(result.errorText)
    del pg_dict
    return result


__all__ = 'pg_conf'
