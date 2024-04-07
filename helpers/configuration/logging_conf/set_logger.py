import logging
from pythonjsonlogger import jsonlogger

from helpers.configuration.logging_conf.logging_configuration import log_conf
from helpers.work_classes.configuration.logging import LogFormat, LogOutput


logger = logging.getLogger(__name__)

log = log_conf()

if log.entity.output == LogOutput.file:
    handler = logging.FileHandler(log.entity.path)
else:
    handler = logging.StreamHandler()

if log.entity.format == LogFormat.string:
    formatter = logging.Formatter(
        fmt='[%(asctime)s] %(pathname)s-%(lineno)d-%(funcName)s %(levelname)s: %(message)s'
    )
else:
    formatter = jsonlogger.JsonFormatter('%(asctime)%(pathname)%(lineno)%(funcName)%(levelname)%(message)')

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(log.entity.level.value)
if log.error:
    logger.info(log.errorText)

__all__ = logger
