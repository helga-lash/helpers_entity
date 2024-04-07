import yaml
import os

from pathlib import Path, PosixPath

from helpers.work_classes import ReturnEntity


cfg_path = Path(os.environ.get('CFG_PTH', '/conf/example.yaml'))


def read_yaml_conf(path: PosixPath = cfg_path) -> ReturnEntity:
    """
    Method reading configuration from file
    :param path: path to configuration file
    :return: helpers.work_classes.ReturnEntity
    """
    result: ReturnEntity = ReturnEntity(True)
    if os.path.exists(path) and os.path.isfile(path):
        try:
            with open(path, 'r') as yaml_file:
                result.error = False
                result.entity = yaml.load(yaml_file, Loader=yaml.FullLoader)
        except Exception as error:
            result.errorText = f"Error reading configuration file {str(path)}. Exception: {error}\n"
    else:
        result.errorText = f'Configuration file {str(path)} is missing'
    return result


__all__ = 'read_yaml_conf'
