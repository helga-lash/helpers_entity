import yaml
import os

from pathlib import Path

from helpers.work_classes import ReturnEntity


cfg_path = Path(os.environ.get('CFG_PTH', '/conf/example.yaml'))


def read_yaml_conf(path: Path = cfg_path) -> ReturnEntity:
    """
    Method reading configuration from file.

    This function opens a YAML file at the specified path, reads its content, and returns it as a Python dictionary.
    If the file does not exist or cannot be opened, an error message is returned.

    Parameters:
        path (Path, optional): The path to the YAML configuration file.
         Defaults to the value of the `cfg_path` variable.

    Returns:
        ReturnEntity: An instance of the `ReturnEntity` class.
         If the file is successfully read, the `success` attribute is False,
         and the `data` attribute contains the loaded YAML data. If an error occurs, the `success` attribute is True,
         and the `error` attribute contains an error message.

    Raises:
        Exception: If an error occurs while reading the file.
    """
    if not (os.path.exists(path) and os.path.isfile(path)):
        return ReturnEntity(True, f'Configuration file {str(path)} is missing')
    try:
        with open(path, 'r') as yaml_file:
            return ReturnEntity(False, None, yaml.load(yaml_file, Loader=yaml.FullLoader))
    except Exception as error:
        return ReturnEntity(True, f"Error reading configuration file {str(path)}. Exception: {error}\n")


__all__ = 'read_yaml_conf'
