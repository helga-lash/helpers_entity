from helpers.configuration import logger


def positive_int_check(verifiable: str or float) -> bool:
    """
    A function that checks that the resulting string is a positive integer.
    Args:
        verifiable: string or float to be checked

    Returns: True if verifiable string is positive integer

    """
    if type(verifiable) is float:
        logger.debug(f'{verifiable} - float')
        return False
    elif type(verifiable) is bool:
        logger.debug(f'{verifiable} - boolean')
        return False
    else:
        try:
            ver_to_int = int(verifiable)
            if ver_to_int <= 0:
                logger.debug(f'{verifiable} - negative number or zero')
                return False
        except Exception as error:
            logger.debug(error)
            return False
    return True


__all__ = 'positive_int_check'
