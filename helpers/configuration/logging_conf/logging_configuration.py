import os

from pathlib import PosixPath

from helpers.work_classes import LogConf, ReturnEntity
from helpers.configuration.yaml_conf_file import read_yaml_conf


def log_conf(path: PosixPath = None) -> ReturnEntity:
    """
    Method validating logging configuration
    :param path: path to configuration file
    :return: helpers.work_classes.ReturnEntity
    """
    if path is not None:
        conf_data = read_yaml_conf(path)
    else:
        conf_data = read_yaml_conf()
    result: ReturnEntity = ReturnEntity(conf_data.error, conf_data.errorText)

    if (not conf_data.error) and (conf_data.entity.get('logging') is not None):
        result.entity = conf_data.entity.pop('logging')
    else:
        result.entity = dict()
    del conf_data

    for key, value in os.environ.items():
        match key:
            case 'LOG_LVL':
                result.entity.update(level=str(value))
            case 'LOG_FMT':
                result.entity.update(format=str(value))
            case 'LOG_OUT':
                result.entity.update(output=str(value))
            case 'LOG_PTH':
                result.entity.update(path=str(value))

    if result.entity.get('level') is not None:
        match str(result.entity['level']).lower():
            case 'd' | 'dbg' | 'debug' | '10':
                result.entity.update(level='debug')
            case 'i' | 'inf' | 'info' | '20':
                result.entity.update(level='info')
            case 'w' | 'wrn' | 'warn' | 'warning' | '30':
                result.entity.update(level='warning')
            case 'e' | 'err' | 'error' | '40':
                result.entity.update(level='error')
            case 'c' | 'crt' | 'crit' | 'critical' | '50':
                result.entity.update(level='critical')
            case _:
                result.entity.pop('level')

    if result.entity.get('format') is not None:
        match str(result.entity['format']).lower():
            case 'json' | 'jsn' | 'js' | 'j':
                result.entity.update(format='json')
            case 'string' | 'str' | 'st' | 's':
                result.entity.update(format='string')
            case _:
                result.entity.pop('format')

    if result.entity.get('output') is not None:
        match str(result.entity['output']).lower():
            case 'stream' | 'strm' | 'str' | 'st' | 's':
                result.entity.update(output='stream')
            case 'file' | 'fl' | 'f':
                result.entity.update(output='file')
            case _:
                result.entity.pop('output')

    match result.entity.get('output'):
        case 'file':
            if result.entity.get('path') is not None:
                log_file_path = str(result.entity['path'])
                log_path_list = log_file_path.split('/')
                log_path_list.pop(-1)
                log_path = '/'.join(log_path_list)
                result.entity.pop('path')
                if os.path.exists(log_path):
                    result.entity.update(path=log_file_path)
        case _:
            result.entity.pop('path', None)

    result.entity = LogConf.from_dict(result.entity)
    return result


__all__ = 'log_conf'
