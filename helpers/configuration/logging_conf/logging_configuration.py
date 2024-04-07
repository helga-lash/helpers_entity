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

    if os.environ.get('LOG_LVL') is not None:
        result.entity.update(level=str(os.environ.get('LOG_LVL')))

    if os.environ.get('LOG_FMT') is not None:
        result.entity.update(format=str(os.environ.get('LOG_FMT')))

    if os.environ.get('LOG_OUT') is not None:
        result.entity.update(output=str(os.environ.get('LOG_OUT')))

    if os.environ.get('LOG_PTH') is not None:
        result.entity.update(path=str(os.environ.get('LOG_PTH')))

    if result.entity.get('level') is not None:
        if str(result.entity['level']).lower() in ['d', 'dbg', 'debug', '10']:
            result.entity.update(level='debug')
        elif str(result.entity['level']).lower() in ['i', 'inf', 'info', '20']:
            result.entity.update(level='info')
        elif str(result.entity['level']).lower() in ['w', 'wrn', 'warn', 'warning', '30']:
            result.entity.update(level='warning')
        elif str(result.entity['level']).lower() in ['e', 'err', 'error', '40']:
            result.entity.update(level='error')
        elif str(result.entity['level']).lower() in ['c', 'crt', 'crit', 'critical', '50']:
            result.entity.update(level='critical')
        else:
            result.entity.pop('level')

    if result.entity.get('format') is not None:
        if str(result.entity['format']).lower() in ['json', 'jsn', 'js', 'j']:
            result.entity.update(format='json')
        elif str(result.entity['format']).lower() in ['string', 'str', 'st', 's']:
            result.entity.update(format='string')
        else:
            result.entity.pop('level')

    if result.entity.get('output') is not None:
        if str(result.entity['output']).lower() in ['stream', 'strm', 'str', 'st', 's']:
            result.entity.update(format='stream')
        elif str(result.entity['output']).lower() in ['file', 'fl', 'f']:
            result.entity.update(format='file')
        else:
            result.entity.pop('output')

    if result.entity.get('output') is not None:
        if result.entity['output'] == 'file':
            if result.entity.get('path') is not None:
                log_file_path = str(result.entity['path'])
                log_path_list = log_file_path.split('/')
                log_path_list.pop(-1)
                log_path = '/'.join(log_path_list)
                result.entity.pop('path')
                if os.path.exists(log_path):
                    result.entity.update(path=log_file_path)
        else:
            result.entity.pop('path')
    result.entity = LogConf.from_dict(result.entity)
    return result


__all__ = 'log_conf'
