import yaml
import os

from pathlib import Path

from helpers.work_classes import ReturnEntity


cfg_path = Path(os.environ.get('CFG_PTH', '/conf/example.yaml'))


def read_yaml_conf(path: Path = cfg_path) -> ReturnEntity:
    """
    Method reading configuration from file
    :param path: path to configuration file
    :return: helpers.work_classes.ReturnEntity
    """
    if not (os.path.exists(path) and os.path.isfile(path)):
        return ReturnEntity(True, f'Configuration file {str(path)} is missing')
    try:
        with open(path, 'r') as yaml_file:
            return ReturnEntity(False, None, yaml.load(yaml_file, Loader=yaml.FullLoader))
    except Exception as error:
        return ReturnEntity(True, f"Error reading configuration file {str(path)}. Exception: {error}\n")


__all__ = 'read_yaml_conf'
