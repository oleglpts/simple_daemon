import logging
from utils.common.flags import DEBUG

########################################################################################################################
#                                               Logger definition                                                      #
########################################################################################################################


def get_logger(logger_name, logging_format, file_name):
    """

    Get logger

    :param logger_name: logger name
    :type logger_name: str
    :param logging_format: log format
    :type logging_format: str
    :param file_name: log file name
    :type file_name: str
    :return: logger
    :rtype: logging.Logger

    """
    logging.basicConfig(level=logging.INFO, format=logging_format)
    log = logging.getLogger(logger_name)
    handler = logging.FileHandler(file_name, encoding='utf8')
    handler.setFormatter(logging.Formatter(logging_format))
    log.addHandler(handler)
    log.setLevel(level=logging.INFO)
    return log

# ----------------------------------------------------------------------------------------------------------------------


logger = get_logger(
    'simple_daemon',
    '%(levelname)-10s|%(asctime)s|%(process)d|%(thread)d| %(name)s --- %(message)s (%(filename)s:%(lineno)d)',
    '/var/log/simple_daemon/simple_daemon.log' if not DEBUG else 'simple_daemon.log'
)
