import os

from pathlib import Path

from helpers.configuration.yaml_conf_file import read_yaml_conf
from helpers.configuration import logger
from helpers.work_classes.configuration import MinioClientConf
from helpers.work_classes import ReturnEntity
from helpers.configuration.help_functions import positive_int_check


def minio_conf(path: Path = None) -> ReturnEntity:
    """
    This function reads and processes the Minio configuration from a YAML file and environment variables.

    Parameters:
        path (Path, optional): The path to the YAML configuration file. If not provided, the function will attempt
         to read the configuration from the default location.

    Returns:
        ReturnEntity: An object containing the processed Minio configuration and any errors encountered during
        the process.
    """
    if path is not None:
        conf_data = read_yaml_conf(path)
    else:
        conf_data = read_yaml_conf()
    result: ReturnEntity = ReturnEntity(conf_data.error, conf_data.errorText)

    if (not conf_data.error) and (conf_data.entity.get('minio') is not None):
        result.entity = conf_data.entity.pop('minio')
        logger.debug("Minio configuration read from configuration file")
    else:
        result.error = False
        result.entity = dict()
        logger.debug("Minio configuration not set in config file")
    del conf_data

    for key, value in os.environ.items():
        match key:
            case 'MN_HOST':
                logger.debug("The minio host is set from the environment variable")
                result.entity.update(host=str(value))
            case 'MN_PORT':
                logger.debug("The minio port is set from the environment variable")
                result.entity.update(port=str(value))
            case 'MN_SECURE':
                logger.debug("The minio secure is set from the environment variable")
                result.entity.update(secure=str(value))
            case 'MN_REGION':
                logger.debug("The minio region is set from the environment variable")
                result.entity.update(region=str(value))
            case 'MN_ACCESS_KEY':
                logger.debug("The minio access key is set from the environment variable")
                result.entity.update(accessKey=str(value))
            case 'MN_SECRET_KEY':
                logger.debug("The minio secret key is set from the environment variable")
                result.entity.update(secretKey=str(value))

    if result.entity.get('host') is None:
        logger.debug('Minio host not configured')
        result.error = True
        result.error_text_append('Minio host not configured')
    if result.entity.get('accessKey') is None:
        logger.debug('Minio access key not configured')
        result.error = True
        result.error_text_append('Minio access key not configured')
    if result.entity.get('secretKey') is None:
        logger.debug('Minio secret key not configured')
        result.error = True
        result.error_text_append('Minio secret key not configured')
    if result.entity.get('port') is not None:
        if positive_int_check(result.entity.get('port')):
            logger.debug('The minio port is positive integer and not zero')
            result.entity.update(port=int(result.entity.get('port')))
        else:
            logger.debug('The minio port must be a positive integer')
            result.error = True
            result.error_text_append('The minio port must be a positive integer')

    if not result.error:
        result.entity = MinioClientConf.from_dict(result.entity)
        if result.entity.port is None:
            if result.entity.secure:
                result.entity.port = 443
            else:
                result.entity.port = 80

    return result


__all__ = 'minio_conf'
