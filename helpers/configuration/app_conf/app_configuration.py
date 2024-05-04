from pathlib import Path

from helpers.configuration.yaml_conf_file import read_yaml_conf
from helpers.configuration import logger
from helpers.work_classes.configuration import AppConf
from helpers.configuration.app_conf.tg_bot_conf import tg_bot_conf
from helpers.work_classes import ReturnEntity


def app_conf(path: Path = None) -> ReturnEntity:
    """
    Method validating the configuration from app
    :param path: path to configuration file
    :return: helpers.work_classes.ReturnEntity
    """
    result: ReturnEntity = ReturnEntity(error=False, entity=AppConf())

    config_data: ReturnEntity = read_yaml_conf(path)

    if (not config_data.error) and (config_data.entity.get('app') is not None):
        logger.debug("App configuration read from configuration file")
        app_dict: dict = config_data.entity.pop('app')
    else:
        logger.debug("App configuration not set in config file")
        result.error_text_append(config_data.errorText)
        app_dict: dict = dict()

    tg_conf = tg_bot_conf(app_dict.get('tgBot'))
    if tg_conf.error:
        result.error_text_append(tg_conf.errorText)
    else:
        result.entity.tgBot = tg_conf.entity

    if result.entity.tgBot is None:
        result.error = True
        logger.info(result.errorText)

    return result


__all__ = 'app_conf'
