import os

from datetime import time

from helpers.configuration import logger
from helpers.work_classes.configuration import TgBotConf
from helpers.work_classes import ReturnEntity


def tg_bot_conf(conf_dict: dict = None) -> ReturnEntity:
    """
    Method validating the connection configuration to the telegram bot
    :param conf_dict: path to configuration file
    :return: helpers.work_classes.ReturnEntity
    """
    result: ReturnEntity = ReturnEntity(False)

    if conf_dict is not None:
        logger.debug("Telegram bot configuration read from configuration file")
    else:
        logger.debug("Telegram bot configuration not set in config file")
        conf_dict: dict = dict()

    for key, value in os.environ.items():
        match key:
            case 'TG_TOKEN':
                logger.debug("The telegram bot token is set from the environment variable")
                conf_dict.update(token=str(value))
            case 'TG_RD_TM':
                logger.debug("The telegram recording time list is set from the environment variable")
                conf_dict['recordTime'] = list()
                for tm in str(os.environ.get('TG_RD_TM')).split(', '):
                    conf_dict['recordTime'].append(tm)
            case 'TG_ADMINS':
                logger.debug("The telegram admins is set from the environment variable")
                conf_dict['admins'] = list()
                for admin in str(os.environ.get('TG_ADMINS')).split(', '):
                    conf_dict['admins'].append(admin)

    if conf_dict.get('token') is None:
        result.error = True
        result.error_text_append('Telegram bot token not configured')

    if conf_dict.get('recordTime') is None:
        result.error = True
        result.error_text_append('The telegram recording time list not configured')
    else:
        str_list = conf_dict.pop('recordTime')
        conf_dict['recordTime'] = list()
        for item in str_list:
            try:
                conf_dict['recordTime'].append(time(*list(map(int, item.split(':')))))
            except Exception as error:
                logger.debug(error)
                result.error = True
                result.error_text_append(f'Invalid time format ({item}).')

    if not result.error:
        result.entity = TgBotConf.from_dict(conf_dict)

    return result


__all__ = 'tg_bot_conf'
