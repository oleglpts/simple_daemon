import os
import logging

########################################################################################################################
#                                               Logger definition                                                      #
########################################################################################################################


def get_logger(logger_name, logging_format, file_name):
    """

    Get logger with path 'file name'. If permission error, create log in /tmp

    :param logger_name: logger name
    :type logger_name: str
    :param logging_format: log format
    :type logging_format: str
    :param file_name: log file name
    :type file_name: str
    :return: logger
    :rtype: logging.Logger

    """
    path, prepared = '', True
    for cat in file_name.split('/')[1:-1]:
        path += '/%s' % cat
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except PermissionError:
                prepared = False
                break
    if not prepared:
        file_name = '/tmp/%s' % file_name.split('/')[-1]
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
    '/tmp/simple_daemon.log'
)
