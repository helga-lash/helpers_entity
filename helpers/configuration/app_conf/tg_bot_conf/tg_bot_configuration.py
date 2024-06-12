import os

from datetime import time
from pathlib import Path

from helpers.configuration import logger
from helpers.work_classes.configuration import TgBotConf
from helpers.work_classes import ReturnEntity
from helpers.configuration.help_functions import positive_int_check


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

    if conf_dict.get('contacts') is None:
        logger.debug("Telegram bot contacts not set in config file")
        conf_dict.update(contacts={})

    for key, value in os.environ.items():
        match key:
            case 'TG_TOKEN':
                logger.debug("The telegram bot token is set from the environment variable")
                conf_dict.update(token=str(value))
            case 'TG_RD_TM':
                logger.debug("The telegram recording time list is set from the environment variable")
                conf_dict['recordTime'] = list()
                for tm in str(value).split(', '):
                    conf_dict['recordTime'].append(tm)
            case 'TG_ADMINS':
                logger.debug("The telegram admins is set from the environment variable")
                conf_dict['admins'] = list()
                for admin in str(value).split(', '):
                    conf_dict['admins'].append(admin)
            case 'TG_RD_MT':
                logger.debug("The telegram number of months is set from the environment variable")
                conf_dict.update(recordMonth=str(value))
            case 'TG_PHOTO_PATH':
                logger.debug("The telegram photo path is set from the environment variable")
                conf_dict.update(photoPath=str(value))
            case 'TG_CON_PHONE':
                logger.debug("The telegram contacts phone is set from the environment variable")
                conf_dict['contacts'].update(phone=str(value))
            case 'TG_CON_WHATSAPP':
                logger.debug("The telegram contacts whatsapp is set from the environment variable")
                conf_dict['contacts'].update(whatsapp=str(value))
            case 'TG_CON_INSTAGRAM':
                logger.debug("The telegram contacts instagram is set from the environment variable")
                conf_dict['contacts'].update(instagram=str(value))
            case 'TG_CON_VK':
                logger.debug("The telegram contacts vk is set from the environment variable")
                conf_dict['contacts'].update(vk=str(value))

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

    if conf_dict.get('recordMonth') is not None:
        if positive_int_check(conf_dict['recordMonth']):
            logger.debug('The telegram number of months a positive integer')
            conf_dict.update(recordMonth=int(conf_dict['recordMonth']))
        else:
            logger.debug('The telegram number of months must be a positive integer. The default value will be used')
            conf_dict.pop('recordMonth')

    if type(conf_dict.get('photoPath')) is str:
        conf_dict['photoPath'] = Path(conf_dict['photoPath'])

    if not result.error:
        result.entity = TgBotConf.from_dict(conf_dict)

    return result


__all__ = 'tg_bot_conf'
